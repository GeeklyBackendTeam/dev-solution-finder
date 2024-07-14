import logging
import asyncio
import time
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
from app.services import CompareTechnologiesRunnable
from langserve import add_routes
from langchain_openai import ChatOpenAI
from app.config import Config
from langchain_community.retrievers import TavilySearchAPIRetriever
from langgraph.graph import Graph
from langchain.schema import Document
from requests.exceptions import HTTPError
from .prompt_template import graph_prompt  # Use relative import
from langchain.prompts import PromptTemplate
import json
from datetime import datetime    
import uvicorn
import os
# from app.convex_functions import save_context, get_context, delete_context
from app.file_utils import save_context, get_context, delete_context,summarize_contexts

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

api_key = Config.OPENAI_API_KEY
TAVILY_API_KEY = Config.TAVILY_API_KEY

model = ChatOpenAI(api_key=api_key)


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app.server")

class CompareRequest(BaseModel):
    messages: list[str]

def function_1(state):
    messages = state['messages']
    user_input = messages[-1]
    complete_query = f"Extract only the names of the technologies mentioned in the following user query: {user_input}"
    response = model.invoke(complete_query)
    technologies = response.content.split('\n')
    state['technologies'] = [tech.strip() for tech in technologies if tech.strip()]
    logger.info("Received request for comparison: %s", state)
    return state

def function_2(state):
    async def async_retrieve():
        technologies = state['technologies']
        agent2_query = f"Provide detailed information about the following technologies: {', '.join(technologies)}. Include performance, community support, learning curve, and developer information."
        retriever = TavilySearchAPIRetriever(api_key=TAVILY_API_KEY)
        
        retries = 3
        for attempt in range(retries):
            try:
                results = await retriever.ainvoke(agent2_query)
                state['messages'].append(results)
                return state
            except HTTPError as e:
                logger.error(f"Attempt {attempt+1} failed with error: {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                raise

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(async_retrieve())

def function_3(state):
    messages = state['messages']
    user_input = messages[0]
    available_info = messages[-1]
    if isinstance(available_info, list):
        available_info = " ".join(doc.page_content if isinstance(doc, Document) else str(doc) for doc in available_info)
    agent3_query = f"Using the following information, provide a detailed comparison of the technologies mentioned in the user query: {user_input}. Information: {available_info}"
    response = model.invoke(agent3_query)
    return response.content

def create_comparison_response(tech_info):
    response_data = []
    for idx, tech in enumerate(tech_info[:10], start=1):
        response_data.append({
            f"tech{idx}": {
                "name": tech['name'],
                "Performance": tech['performance'],
                "Community Support": tech['community_support'],
                "LearningCurve": tech['learning_curve'],
                "DevelopedBy": tech['developed_by'],
                "Recommendation": tech['recommendation']
            }
        })
    return response_data

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


# Define the initial prompt template for Mermaid diagram generation
prompt_template = """
Your task is to generate the Mermaid.js code based on the given inputs. Ensure the Mermaid.js code is correct and adheres to the standards.

Your job is to write the code to generate a colorful mermaid diagram of {diagram_type}
describing the below
{details} information only, don't use any other information.
Only generate the code as output, nothing extra, and do not use (brackets) or colors.
Each line in the code must be terminated by ;
Code:
"""

graph_prompt = PromptTemplate(template=prompt_template)

# Define the prompt template for extracting additional context with non-technical terms
clarification_prompt_template = """
The user has provided the following details for a {diagram_type} diagram:
{details}

To generate a meaningful diagram, we need more information. Please list the additional details required for a {diagram_type} diagram and formulate clarifying questions to ask the user in simple, non-technical terms.

Example:
- For a Class diagram: "Can you tell me about the main parts or things in your app and how they connect?"
- For a Sequence diagram: "Who is involved and what do they do step by step?"

Questions:
"""

clarification_prompt = PromptTemplate(template=clarification_prompt_template)

def extract_mermaid_code(content):
    # Extract and clean the Mermaid.js code from the response content
    return content.strip()

async def ask_clarifying_questions(model, diagram_type, details):
    # Generate clarifying questions using the model
    formatted_prompt = clarification_prompt.format(
        diagram_type=diagram_type,
        details=details
    )
    try:
        response = model.invoke(formatted_prompt)
        # Log the response for debugging purposes
        print("Clarifying questions response:", response.content)
        return response.content.strip()
    except Exception as e:
        return str(e)

@app.post("/graph")
async def generate_graph(request: Request):
    # Debugging: Log the raw request body
    raw_body = await request.body()
    print("Raw request body:", raw_body.decode())

    try:
        input_data = await request.json()
    except json.JSONDecodeError as e:
        print("JSON decoding error:", e)
        return {"error": "Invalid JSON in request body"}

    diagram_type = input_data.get("diagram_type")
    details = input_data.get("details")
    project_id = input_data.get("project_id")
    conversation_id = input_data.get("conversation_id")
    user_id = input_data.get("user_id")

    # Validate the required fields
    if not diagram_type or not details or not project_id or not conversation_id:
        return {"error": "diagram_type, details, project_id, and conversation_id are required fields"}

    # Summarize existing context for the user and project
    summarized_context = summarize_contexts(project_id, user_id)
    if summarized_context:
        details = summarized_context + " " + details

    # Save the current context
    context = {
        "diagram_type": diagram_type,
        "details": details,
        "timestamp": datetime.now().isoformat()
    }
    save_context(project_id, user_id, conversation_id, context)

    # Check if the details provided are sufficient
    if len(details.split()) < 10:  # Example condition for insufficient details
        clarifying_questions = await ask_clarifying_questions(model, diagram_type, details)
        return {"clarifying_questions": clarifying_questions}

    # Format the prompt with provided data
    formatted_prompt = graph_prompt.format(
        diagram_type=diagram_type,
        details=details
    )

    # Invoke the model
    try:
        response = model.invoke(formatted_prompt)
        response_content = response.content.replace("", "").replace("mermaid", "")
        response_content = extract_mermaid_code(response_content)

        # Debugging: Log the response content
        print("LLM response content:", response_content)

        return {"mermaid_code": response_content}
    except Exception as e:
        return {"error": str(e)}

@app.post("/chat")
async def hello_world(request: Request):
    input_data = await request.json()
    compare_request = CompareRequest(**input_data)
    messages = compare_request.messages
    
    workflow = Graph()

    workflow.add_node("agent", function_1)
    workflow.add_node("tool", function_2)
    workflow.add_node("responder", function_3)

    workflow.add_edge('agent', 'tool')
    workflow.add_edge('tool', 'responder')

    workflow.set_entry_point("agent")
    workflow.set_finish_point("responder")

    appnew = workflow.compile()
    inputs = {"messages": messages}

    result = appnew.invoke(inputs)

    logger.info(f"Result from workflow: {result}")

    # Mocking the result_dict for demonstration purposes
    # This should be replaced with actual parsing logic based on the result returned
    result_dict = {
        'messages': ["I would like to know how is react compared to angular.js"],
        'technologies': ['React', 'AngularJS']
    }
    tech_names = result_dict['technologies']
    
    # Assume `result` is a JSON string containing detailed technology information
    # Here we would parse the `result` to extract the information
    tech_info = [
        {
            "name": "React",
            "performance": "Highly efficient virtual DOM",
            "community_support": "Large active community",
            "learning_curve": "Steep for beginners",
            "developed_by": "Facebook",
            "recommendation": "Ideal for complex applications"
        },
        {
            "name": "AngularJS",
            "performance": "Full-fledged MVC framework",
            "community_support": "Strong community support",
            "learning_curve": "Steep due to complexity",
            "developed_by": "Google",
            "recommendation": "Suitable for large scale applications"
        }
    ]

    # Create a comparison response based on technology information
    formatted_result = create_comparison_response(tech_names)
    
    return JSONResponse(content=formatted_result)


compare_technologies_runnable = CompareTechnologiesRunnable()
add_routes(app, compare_technologies_runnable, path="/compare-assistant")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
