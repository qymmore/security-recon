from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models
from tasks import run_full_scan
from fastapi import WebSocket
import asyncio
import redis

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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
    print(f"WebSocket connection attempt for scan {scan_id}")

    await websocket.accept()
    print("WebSocket connected")

    try:
        while True:
            await websocket.send_text(f"connected to scan {scan_id}")
            await asyncio.sleep(2)
    except:
        print("WebSocket disconnected")