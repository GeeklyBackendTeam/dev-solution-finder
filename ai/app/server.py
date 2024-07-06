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

app = FastAPI()

# Load environment variables from .env file
load_dotenv()

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
        model = ChatOpenAI(api_key=api_key, temperature=0.9)

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "Answer the user's question in 3 words"),
                ("user", user_input),
            ]
        )
        
        chain = prompt | model | StrOutputParser()
        response = chain.invoke({"query": user_input})
        
        # Return the raw response
        return JSONResponse(content={"response": response})
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


# # Define your desired data structure.
# class Joke(BaseModel):
#     setup: str = Field(description="question to set up a joke")
#     punchline: str = Field(description="answer to resolve the joke")

# # Route to call OpenAI model to tell joke
# @app.get("/openai/{joke}")
# model = ChatOpenAI(temperature=0)
# # And a query intented to prompt a language model to populate the data structure.
# joke_query = "Tell me a joke."

# # Set up a parser + inject instructions into the prompt template.
# parser = JsonOutputParser(pydantic_object=Joke)

# prompt = PromptTemplate(
#     template="Answer the user query.\n{format_instructions}\n{query}\n",
#     input_variables=["query"],
#     partial_variables={"format_instructions": parser.get_format_instructions()},
# )

# chain = prompt | model | parser

# chain.invoke({"query": joke_query})

# Edit this to add the chain you want to add
add_routes(app, research_assistant_chain, path="/research-assistant")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
