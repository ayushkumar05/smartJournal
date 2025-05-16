from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from journal_state import get_journal, update_journal
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connected_users = []

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    connected_users.append(websocket)

    current_content = await get_journal()
    await websocket.send_json({"type": "init", "text": current_content["text"]})

    try:
        while True:
            data = await websocket.receive_json()
            if data["type"] == "update":
                await update_journal(data["text"])
                for user in connected_users:
                    if user != websocket:
                        await user.send_json({"type": "update", "text": data["text"]})
    except WebSocketDisconnect:
        connected_users.remove(websocket)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
