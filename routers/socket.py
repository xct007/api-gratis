import websockets
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

routes = APIRouter()


async def socket(websocket: WebSocket):
    """
    WebSocket route that accepts incoming JSON messages
    """
    await websocket.accept()
    try:
        while True:
            str = await websocket.receive_json()
            if "data" in str:
                await websocket.send_json(str)
            else:
                await websocket.send_json({"status": False, "message": "Invalid data"})
    except WebSocketDisconnect:
        pass
    finally:
        await websocket.close()

routes.add_api_websocket_route("/ws_ack", socket, name="ws_ack")
