import requests

from .utils import find_image


def effects():
    try:
        response = requests.get("https://api.apigratis.site/api/effects")
        return response.json()
    except Exception as e:
        return {"status": False, "message": str(e)}


def apply_effect(uuid: str, effect_id):
    image = find_image(uuid)
    if not image:
        return {"status": False, "message": "Image not found"}
    try:
        response = requests.post(
            "https://api.apigratis.site/api/apply_effect",
            files={"image": image},
            data={"effect_id": effect_id},
        )
        return response.json()
    except Exception as e:
        return {"status": False, "message": str(e)}
