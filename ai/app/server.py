import os
import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langserve import add_routes
from research_assistant import chain as research_assistant_chain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.utils.openai_functions import convert_pydantic_to_openai_function

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app.server")

# Load environment variables from .env file
load_dotenv()

class TechnologyComparison(BaseModel):
    DevelopedBy: str = Field(description="The company or individual who developed the technology.")
    InitialRelease: str = Field(description="The initial release date of the technology.")
    CurrentVersion: str = Field(description="The current version of the technology.")
    CurrentVersionReleaseDate: str = Field(description="The release date of the current version.")
    Type: str = Field(description="The type of technology, e.g., library or framework.")
    Language: str = Field(description="The programming language used by the technology.")
    DataBinding: str = Field(description="The type of data binding used.")
    DOM: str = Field(description="The type of DOM used.")
    ComponentBased: str = Field(description="Whether the technology is component-based.")
    LearningCurve: str = Field(description="The learning curve for the technology.")
    Performance: str = Field(description="The performance characteristics of the technology.")
    CommunitySupport: str = Field(description="The level of community support available for the technology.")
    Scalability: str = Field(description="The scalability of the technology.")
    Serverless: str = Field(description="Support for serverless architecture.")
    VirtualDOM: str = Field(description="The use of virtual DOM.")
    RenderingPattern: str = Field(description="The rendering pattern used.")

class ComparisonOutput(BaseModel):
    __root__: dict[str, TechnologyComparison]

frontend_template = PromptTemplate(
    input_variables=["technologies", "relevant_parameters", "output_format"],
    template="""
    Compare the following technologies based on the relevant parameters provided. Ensure the comparison is presented in the specified output format.

    Technologies: {technologies}
    Relevant Parameters: {relevant_parameters}
    Output Format: {output_format}

    Provide a detailed comparison and recommendation for each technology separately in a structured JSON format.
    """
) + "\n Limit each parameter's response to 4-5 words."

openai_functions = [convert_pydantic_to_openai_function(TechnologyComparison)]

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

@app.get("/hello")
async def hello_world():
    return JSONResponse(content={"message": "Hello World"})

@app.post("/compare-frontend-technologies")
async def compare_frontend_technologies(request: Request):
    try:
        data = await request.json()
        technologies = data.get("technologies", [])
        relevant_parameters = data.get("relevant_parameters", [])
        output_format = data.get("output_format", "JSON")

        if len(technologies) > 10:
            raise HTTPException(status_code=400, detail="Maximum limit of 10 technologies exceeded")

        logger.info("Received request for comparison")
        logger.info(f"Technologies: {technologies}")
        logger.info(f"Relevant Parameters: {relevant_parameters}")
        logger.info(f"Output Format: {output_format}")

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found")

        model = ChatOpenAI(api_key=api_key)
        
        # Determine default relevant parameters based on technology types
        if not relevant_parameters:
            if all(tech in ["aws", "GCP", "azure", "Digital Ocean"] for tech in technologies):
                relevant_parameters = ["Scalability", "Serverless", "Performance", "Community Support"]
            elif all(tech in ["React", "Vue", "Angular"] for tech in technologies):
                relevant_parameters = ["VirtualDOM", "RenderingPattern", "ComponentBased", "LearningCurve"]
            else:
                relevant_parameters = ["Performance", "Community Support", "LearningCurve", "DevelopedBy"]

        technologies_str = ', '.join(technologies)
        relevant_parameters_str = ', '.join(relevant_parameters)
        prompt = frontend_template.format(
            technologies=technologies_str,
            relevant_parameters=relevant_parameters_str,
            output_format=output_format
        )
        
        logger.info("Generated prompt")
        logger.info(prompt)

        parser = JsonOutputParser()
        chain = ChatPromptTemplate.from_template(prompt) | model | parser

        logger.info("Invoking the chain")
        response = chain.invoke({})
        
        logger.info("Chain invoked successfully")
        logger.info(f"Response: {response}")

        # Adjust the response to include the technology name within each techN object
        formatted_response = [
            {
                f"tech{i+1}": {"name": tech_name, **details}
                for i, (tech_name, details) in enumerate(response.items())
            }
        ]

        return formatted_response
        
    except Exception as e:
        logger.error(f"Error during request processing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

add_routes(app, research_assistant_chain, path="/research-assistant")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
