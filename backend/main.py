from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Allow React frontend to access the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clients = []

# Latest status of every API
latest_data = {}


class ApiStatus(BaseModel):
    page: str
    api_url: str
    status: int
    priority: str
    response_time: float
    action: str


@app.get("/")
def home():
    return {"message": "Backend is running successfully!"}


@app.post("/api/update")
async def update_status(data: ApiStatus):
    latest_data[data.api_url] = data.model_dump()

    return {"success": True}


@app.get("/api/latest")
def get_latest():
    return list(latest_data.values())


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        clients.remove(websocket)