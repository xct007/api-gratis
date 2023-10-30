from fastapi import FastAPI, Request, status
import logging
import uvicorn

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from routers import api, socket

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    logger = logging.getLogger("uvicorn")
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    app.state.logger = logger


@app.exception_handler(RequestValidationError)
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Exception handler for FastAPI application.

    Args:
        request (Request): The request object.
        exc (Exception): The exception object.

    Returns:
        JSONResponse: The JSON response object.
    """
    logger = request.app.state.logger
    logger.error(f"{exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"status": False, "message": str(exc)},
    )

# FastAPI docs spec
docs = {
    "info": {
        "title": "API Gratis",
        "description": "A free API for testing purposes.",
        "version": "0.1.0",
    },
    "servers": [{"url": "http://localhost:5000"}],
    "openapi": "3.0.2",
}

app.include_router(api.routes)
app.include_router(socket.routes)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
