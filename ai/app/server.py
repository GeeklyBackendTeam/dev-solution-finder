import os
import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langserve import add_routes
from research_assistant import chain as research_assistant_chain
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.utils.openai_functions import convert_pydantic_to_openai_function
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_community.llms import Ollama

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

class TechnologyComparison(BaseModel):
    DevelopedBy: str = Field(description="Details about the developers")
    InitialRelease: str = Field(description="Initial release date")
    CurrentVersion: str = Field(description="Current version")
    Type: str = Field(description="Type of technology")
    Language: str = Field(description="Programming language used")
    DataBinding: str = Field(description="Data binding method")
    DOM: str = Field(description="DOM handling")
    ComponentBased: str = Field(description="Is it component-based?")
    LearningCurve: str = Field(description="Learning curve")
    Performance: str = Field(description="Performance details")
    CommunitySupport: str = Field(description="Community support and resources")

class ComparisonOutput(BaseModel):
    tech1: TechnologyComparison
    tech2: TechnologyComparison

frontend_template = PromptTemplate(
    input_variables=["technology1", "technology2", "relevant_parameters", "output_format"],
    template="""
    Compare the following two frontend technologies based on the relevant parameters provided. Ensure the comparison is presented in the specified output format.

    Technology 1: {technology1}
    Technology 2: {technology2}
    Relevant Parameters: {relevant_parameters} (Optional)
    Output Format: {output_format}

    Parameters to include:
    - Developed By
    - Initial Release
    - Current Version
    - Type
    - Language
    - Data Binding
    - DOM
    - Component-Based
    - Learning Curve
    - Performance
    - Community Support

    Provide a detailed comparison and recommendation for both technologies separately in a structured JSON format with keys "tech1" and "tech2".
    """
)


openai_functions = [convert_pydantic_to_openai_function(ComparisonOutput)]

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
        technology1 = data.get("technology1")
        technology2 = data.get("technology2")
        relevant_parameters = data.get("relevant_parameters", "")
        output_format = data.get("output_format", "JSON")

        logger.info("Received request for comparison")
        logger.info(f"Technology 1: {technology1}")
        logger.info(f"Technology 2: {technology2}")
        logger.info(f"Relevant Parameters: {relevant_parameters}")
        logger.info(f"Output Format: {output_format}")

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found")

        model = ChatOpenAI(api_key=api_key)
        
        prompt = frontend_template.format(
            technology1=technology1,
            technology2=technology2,
            relevant_parameters=relevant_parameters,
            output_format=output_format
        )
        
        logger.info("Generated prompt")
        logger.info(prompt)

        chain = ChatPromptTemplate.from_template(prompt) | model.bind(functions=openai_functions) | JsonOutputFunctionsParser()

        logger.info("Invoking the chain")
        response = chain.invoke({})
        
        logger.info("Chain invoked successfully")
        return response
        
    except Exception as e:
        logger.error(f"Error during request processing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

add_routes(app, research_assistant_chain, path="/research-assistant")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
