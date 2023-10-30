import os
import asyncio


async def delete_file(filepath):
    """
    Deletes a file after 1 minute.

    Args:
        filepath (str): The path to the file to delete.
    """
    await asyncio.sleep(60)
    os.remove(filepath)


def find_image(uuid: str):
    try:
        for ext in ['jpg', 'jpeg', 'png', 'gif']:
            image_path = os.path.join("tmp", f"{uuid}.{ext}")
            if os.path.exists(image_path):
                with open(image_path, "rb") as f:
                    image_data = f.read()
                return image_data
        return False
    except Exception as e:
        print(e)
        return False
