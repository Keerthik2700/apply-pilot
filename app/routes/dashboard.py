from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.db import get_db
from app.security import decode_token, COOKIE_NAME
from app.services.analytics import status_counts, weekly_trend

router = APIRouter()


def get_user_id(request: Request) -> int:
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        return 0
    return decode_token(token)


@router.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):
    user_id = get_user_id(request)
    if not user_id:
        from fastapi.responses import RedirectResponse
        return RedirectResponse("/login", status_code=303)

    counts = status_counts(db, user_id)
    trend = weekly_trend(db, user_id)
    return request.app.state.templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "counts": counts, "trend": trend},
    )
