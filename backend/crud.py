from sqlalchemy.orm import Session
from typing import Optional, List
from . import models

def create_event(db: Session, item) -> models.Detection:
    e = models.Detection(
        timestamp=item.timestamp,
        label=item.label,
        conf=item.conf,
        x1=item.x1, y1=item.y1, x2=item.x2, y2=item.y2,
        cx=item.cx, cy=item.cy,
        evento=item.evento
    )
    db.add(e)
    db.commit()
    db.refresh(e)
    return e

def list_events(db: Session, limit: int = 100, start: Optional[str] = None, end: Optional[str] = None) -> List[models.Detection]:
    q = db.query(models.Detection)
    if start:
        q = q.filter(models.Detection.timestamp >= start)
    if end:
        q = q.filter(models.Detection.timestamp <= end)
    return q.order_by(models.Detection.id.desc()).limit(limit).all()

def stats(db: Session):
    total = db.query(models.Detection).count()
    left = db.query(models.Detection).filter(models.Detection.evento=="moto_esquerda").count()
    right = db.query(models.Detection).filter(models.Detection.evento=="moto_direita").count()
    by_label = {}
    for label, cnt in db.query(models.Detection.label, models.func.count()).group_by(models.Detection.label):
        by_label[label] = cnt
    return {"total": total, "moto_esquerda": left, "moto_direita": right, "por_label": by_label}
