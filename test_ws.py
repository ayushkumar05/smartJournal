import websocket
import json

def on_message(ws, message):
    print("Received:", message)

def on_open(ws):
    ws.send(json.dumps({"type": "update", "text": "Testing from Python again!"}))

ws = websocket.WebSocketApp(
    "ws://localhost:8000/ws/user1",
    on_message=on_message,
    on_open=on_open
)
ws.run_forever()
