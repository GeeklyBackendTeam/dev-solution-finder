import logging
from fastapi import FastAPI
from fastapi.responses import RedirectResponse, JSONResponse
from app.routes import router
from app.services import CompareTechnologiesRunnable
from langserve import add_routes

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app.server")

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

@app.get("/hello")
async def hello_world():
    return JSONResponse(content={"message": "Hello World"})

app.include_router(router)

compare_technologies_runnable = CompareTechnologiesRunnable()
add_routes(app, compare_technologies_runnable, path="/compare-assistant")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
