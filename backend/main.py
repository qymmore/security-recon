from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models
from tasks import run_full_scan
from fastapi import WebSocket
import asyncio
import redis
from redis_client import subscribe
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/scan")
def create_scan(target: str, db: Session = Depends(get_db)):
    scan = models.Scan(target=target, status="pending")
    db.add(scan)
    db.commit()
    db.refresh(scan)

    run_full_scan.delay(scan.id, target)

    return {"scan_id": scan.id}

@app.get("/scan/{scan_id}")
def get_scan(scan_id: int, db: Session = Depends(get_db)):
    return db.query(models.Scan).get(scan_id)

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

@app.websocket("/ws/{scan_id}")
async def websocket_endpoint(websocket: WebSocket, scan_id: int):
    await websocket.accept()

    async for message in subscribe(scan_id):
        await websocket.send_text(message)