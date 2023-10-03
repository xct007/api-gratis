from fastapi import APIRouter


from src.models.responses import AnyResponse
from src.models.requests import Txt2img, Img2Img

# TODO: Services
from src.services.txt2img import txt2img
from src.services.img2img import img2img

router = APIRouter()


@router.post("/txt2img", response_model=AnyResponse)
async def txt2img(request: Txt2img):
    try:
        return {"status": True, "result": await txt2img(**request)}
    except Exception as e:
        return {"status": False, "message": str(e)}


@router.post("/img2img", response_model=AnyResponse)
async def img2img(request: Img2Img):
    try:
        return {"status": True, "result": await img2img(**request)}
    except Exception as e:
        return {"status": False, "message": str(e)}
