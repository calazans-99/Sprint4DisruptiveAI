from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from . import models, database, crud

app = FastAPI(title="Sprint4-IA Backend", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)

class EventIn(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    label: str
    conf: float
    x1: int; y1: int; x2: int; y2: int
    cx: int; cy: int
    evento: str

class Event(models.EventOut):
    pass

@app.get("/health")
def health():
    return {"status": "ok", "ts": datetime.utcnow().isoformat()}

@app.post("/events", response_model=Event)
def create_event(item: EventIn, db: Session = Depends(database.get_db)):
    return crud.create_event(db, item)

@app.get("/events", response_model=List[Event])
def list_events(limit: int = 100, start: Optional[str] = None, end: Optional[str] = None, db: Session = Depends(database.get_db)):
    return crud.list_events(db, limit=limit, start=start, end=end)

@app.get("/stats")
def stats(db: Session = Depends(database.get_db)):
    return crud.stats(db)
