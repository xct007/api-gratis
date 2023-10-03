from typing import Any
from pydantic import BaseModel


class BaseResponse(BaseModel):
    status: bool


class ErrorResponse(BaseResponse):
    message: str


# TODO: Add response models
class AnyResponse(BaseResponse):
    result: Any
