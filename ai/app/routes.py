# app/routes.py

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.services import CompareTechnologiesRunnable

router = APIRouter()

@router.post("/compare-assistant")
async def compare_technologies_endpoint(request: Request):
    data = await request.json()
    runnable = CompareTechnologiesRunnable()
    response = await runnable.invoke(data)
    return JSONResponse(content=response)
