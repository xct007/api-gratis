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

description = """
### API Gratis
This is a free API for testing purposes. It is a RESTful API built on FastAPI and Python.

### Notes
Will be adding more endpoints soon. If you have any suggestions, please let us know.

### Support
If you like this API, please consider supporting us on [Patreon](https://www.patreon.com/apigratis).

### Credits
- [FastAPI](https://fastapi.tiangolo.com/)
- [Python](https://www.python.org/)
- [Uvicorn](https://www.uvicorn.org/)
- [Starlette](https://www.starlette.io/)
- [GitHub](https://github.com/xct007/api-gratis)

### License
MIT License

### Disclaimer
No guarantee of availability or performance is provided. Use at your own risk.
"""

app = FastAPI(
    title="API",
    description=description,
    version="0.1.0",
    contact={
        "name": "ITSROSE APIs",
        "url": "https://devitsrose.com",
        "email": "rose@devitsrose.com"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/license/MIT/"
    },
    openapi_url="/openapi.json",
    docs_url="/",
    redoc_url="/redoc",
    servers=[
        {
            "url": "https://apigratis.site",
            "description": "Production server"
        }
    ]
)

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

app.include_router(api.routes)
app.include_router(socket.routes)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
