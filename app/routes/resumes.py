from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Resume
from app.security import decode_token, COOKIE_NAME

router = APIRouter()


def uid(request: Request) -> int:
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        return 0
    return decode_token(token)


@router.get("/resumes")
def resumes_page(request: Request, db: Session = Depends(get_db)):
    user_id = uid(request)
    if not user_id:
        return RedirectResponse("/login", status_code=303)

    resumes = db.query(Resume).filter(Resume.user_id == user_id).order_by(Resume.created_at.desc()).all()
    return request.app.state.templates.TemplateResponse("resumes.html", {"request": request, "resumes": resumes})


@router.post("/resumes/new")
def resume_create(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db),
):
    user_id = uid(request)
    if not user_id:
        return RedirectResponse("/login", status_code=303)

    r = Resume(user_id=user_id, title=title.strip(), content=content.strip())
    db.add(r)
    db.commit()
    return RedirectResponse("/resumes", status_code=303)
