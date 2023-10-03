import logging
import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request


from src.routers.api import router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    logger = logging.getLogger("uvicorn.access")
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    app.state.logger = logger


@app.exception_handler(RequestValidationError)
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger = request.app.state.logger
    logger.error(f"{exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"status": False, "message": str(exc)},
    )


app.add_route("/api", router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000)
