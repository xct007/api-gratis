from typing import Optional
from pydantic import BaseModel


class StringValue(BaseModel):
    model_id: str
    scheduler: str


class IntegerValue(StringValue):
    guidance_scale: int
    width: int
    height: int
    seed: int
    num_inference_steps: int
    clip_skip: int


class BooleanValue(IntegerValue):
    highres_fix: bool
    safety_checker: Optional[bool] = None


class Txt2img(BooleanValue):
    prompt: str
    negative_prompt: Optional[str] = None


class Img2Img(Txt2img):
    init_image: str
