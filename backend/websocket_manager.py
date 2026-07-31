from fastapi import WebSocket

clients = []

async def connect(websocket: WebSocket):

    await websocket.accept()

    clients.append(websocket)


def disconnect(websocket: WebSocket):

    if websocket in clients:
        clients.remove(websocket)


async def broadcast(data):

    for client in clients:

        await client.send_json(data)