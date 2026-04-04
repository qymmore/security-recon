from fastapi import FastAPI, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from scanner import run_scan

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def process_scan(scan_id: int, target: str):
    db = SessionLocal()
    scan = db.query(models.Scan).filter(models.Scan.id == scan_id).first()

    scan.status = "running"
    db.commit()

    result = run_scan(target)

    scan.status = "completed"
    scan.result = result
    db.commit()
    db.close()

@app.post("/scan")
def create_scan(target: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    scan = models.Scan(target=target, status="pending")
    db.add(scan)
    db.commit()
    db.refresh(scan)

    background_tasks.add_task(process_scan, scan.id, target)

    return {"scan_id": scan.id}

@app.get("/scan/{scan_id}")
def get_scan(scan_id: int, db: Session = Depends(get_db)):
    scan = db.query(models.Scan).filter(models.Scan.id == scan_id).first()
    return scan