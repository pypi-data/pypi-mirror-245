import argparse

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from jarvis.api.conversation import router as conversation_router
from jarvis.exceptions.api_exceptions import JarvisInternalException, JarvisNotFoundException
from jarvis.api.knowledge import router as knowledge_router
from jarvis.api.memory import router as memory_router
from jarvis.api.tool import router as tool_router

app = FastAPI()
app.include_router(conversation_router)
app.include_router(knowledge_router)
app.include_router(tool_router)
app.include_router(memory_router)


@app.exception_handler(JarvisInternalException)
async def internal_exception_handler(request: Request, exc: JarvisInternalException):
    return JSONResponse(
        status_code=500,
        content={
            "message": exc.message
        }
    )


@app.exception_handler(JarvisNotFoundException)
async def internal_exception_handler(request: Request, exc: JarvisNotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            "message": exc.message
        }
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--log-level", type=str, default="info")
    args = parser.parse_args()
    uvicorn.run(app, host=args.host, port=args.port, log_level=args.log_level)
