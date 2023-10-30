import base64
import imghdr
import uuid
import asyncio

from fastapi import APIRouter, HTTPException

from services.utils import delete_file
from services.effects import effects, apply_effect

routes = APIRouter()


async def apply_effect(uuid: str, effect_id: str, coloration: str):
    """
    Apply an effect to the user's account.

    Returns:
        A dictionary containing a success message.
    """
    try:
        return apply_effect(uuid, effect_id, coloration)
    except Exception as e:
        return {"status": False, "message": str(e)}


async def get_effects():
    """
    Returns a dictionary with a message indicating that the effects have been returned.

    Returns:
    dict: A dictionary with a message indicating that the effects have been returned.
    """

    return {"message": "Effects returned!"}


async def upload_image(image: str):
    """
    Uploads a base64 encoded image and saves it to the tmp folder with a unique filename generated using uuid.

    Args:
        image (str): The base64 encoded image to upload.

    Returns:
        A dictionary containing a success message.
    """
    # Decode the base64 encoded image
    try:
        contents = base64.b64decode(image)
    except:
        raise HTTPException(
            status_code=400, detail="Invalid base64 encoded image.")

    # Check if the decoded contents is a valid image with jpeg/jpg or png extension
    valid_extensions = ["jpeg", "jpg", "png"]
    extension = imghdr.what(None, h=contents)
    if not extension or extension not in valid_extensions:
        raise HTTPException(
            status_code=400, detail="Invalid image file. Only jpeg/jpg and png files are allowed.")

    # Generate a unique filename using uuid
    filename = str(uuid.uuid4())

    # Save the file to the tmp folder with the generated filename
    with open(f"tmp/{filename}.{extension}", "wb") as f:
        f.write(contents)

    # Schedule a task to delete the file after 1 minute
    asyncio.create_task(delete_file(f"tmp/{filename}.{extension}"))

    # Return the filename and the delete time
    return {
        "status": True,
        "result": {
            "uuid": filename,
            "url": routes.url_path_for("get_image", filename=filename),
            "delete_time": "1 minute",
        },
    }

# FastAPI docs spec
routes.add_api_route("/apply_effect", apply_effect, methods=["POST"], responses={
                     200: {
                         "description": "Apply an effect to the user's account.",
                         "content": {
                             "application/json": {
                                 "example": {
                                     "status": True,
                                     "result": {
                                         "corolation_id":
                                         "1234",
                                         "delete_time": "1 minute"
                                     }
                                 }
                             }
                         }
                     },
                     400: {
                         "description": "Invalid base64 encoded image.",
                         "content": {
                             "application/json": {
                                 "example": {
                                        "status": False,
                                        "message": "Invalid base64 encoded image."
                                 }
                             }
                         }
                     },
                     }
                     )
routes.add_api_route("/upload_image", upload_image, methods=["POST"], responses={
                     200: {
                         "description": "Uploads a base64 encoded image and saves it to the tmp folder with a unique filename generated using uuid.",
                         "content": {
                             "application/json": {
                                 "example": {
                                     "status": True,
                                     "result": {
                                         "corolation_id":
                                         "1234",
                                         "delete_time": "1 minute"
                                     }
                                 }
                             }
                         }
                     },
                     400: {
                         "description": "Invalid image file. Only jpeg/jpg and png files are allowed.",
                         "content": {
                             "application/json": {
                                 "example": {
                                        "status": False,
                                        "message": "Invalid image file. Only jpeg/jpg and png files are allowed."
                                 }
                             }
                         }
                     },
                     })
routes.add_api_route("/get_effects", get_effects, methods=["GET"], responses={
    200: {
        "description": "Returns a dictionary with a message indicating that the effects have been returned.",
        "content": {
            "application/json": {
                "example": {
                    "message": "Effects returned!"
                }
            }
        }
    }
})
