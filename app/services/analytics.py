from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models import Application


def status_counts(db: Session, user_id: int) -> dict:
    rows = (
        db.query(Application.status, func.count(Application.id))
        .filter(Application.user_id == user_id)
        .group_by(Application.status)
        .all()
    )
    return {str(status.value): int(cnt) for status, cnt in rows}


def weekly_trend(db: Session, user_id: int, weeks: int = 8) -> list[dict]:
    start = datetime.utcnow() - timedelta(days=7 * weeks)
    rows = (
        db.query(func.date_trunc("week", Application.created_at).label("wk"), func.count(Application.id))
        .filter(Application.user_id == user_id, Application.created_at >= start)
        .group_by("wk")
        .order_by("wk")
        .all()
    )
    return [{"week": str(wk.date()), "count": int(cnt)} for wk, cnt in rows]
