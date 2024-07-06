import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langserve import add_routes
from research_assistant import chain as research_assistant_chain
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser


from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.utils.openai_functions import (
    convert_pydantic_to_openai_function,
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser

app = FastAPI()

# Load environment variables from .env file
load_dotenv()

class Joke(BaseModel):
    """Give me detail about Performance and learning curve of given technologies"""

    Performance: str = Field(description="tell me about Performance ")
    LearningCurve: str = Field(description="tell me about learning curve")


openai_functions = [convert_pydantic_to_openai_function(Joke)]

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

# New route to return "Hello World" in JSON
@app.get("/hello")
async def hello_world():
    return JSONResponse(content={"message": "Hello World"})

# Route to call OpenAI model
@app.get("/openai/{user_input}")
async def call_openai_model(user_input: str):
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        model = ChatOpenAI(api_key=api_key)

        prompt = ChatPromptTemplate.from_template("Do a detailed analysis of technolgy {topic}")

        chain = prompt | model.bind(functions=openai_functions)  |JsonOutputFunctionsParser()
        response = chain.invoke({"topic": "user_input"})
        
        # Return the raw response
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


add_routes(app, research_assistant_chain, path="/research-assistant")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
