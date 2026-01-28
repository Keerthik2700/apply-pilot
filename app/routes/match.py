from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Resume
from app.security import decode_token, COOKIE_NAME
from app.services.matcher import match_resume_to_jd

router = APIRouter()


def uid(request: Request) -> int:
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        return 0
    return decode_token(token)


@router.get("/match")
def match_page(request: Request, db: Session = Depends(get_db)):
    user_id = uid(request)
    if not user_id:
        return RedirectResponse("/login", status_code=303)

    resumes = db.query(Resume).filter(Resume.user_id == user_id).order_by(Resume.created_at.desc()).all()
    return request.app.state.templates.TemplateResponse("match.html", {"request": request, "resumes": resumes})


@router.post("/match")
def match_run(
    request: Request,
    resume_id: int = Form(...),
    jd_text: str = Form(...),
    db: Session = Depends(get_db),
):
    user_id = uid(request)
    if not user_id:
        return RedirectResponse("/login", status_code=303)

    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == user_id).first()
    if not resume:
        return RedirectResponse("/match?error=Resume+not+found", status_code=303)

    result = match_resume_to_jd(resume.content, jd_text)
    resumes = db.query(Resume).filter(Resume.user_id == user_id).order_by(Resume.created_at.desc()).all()
    return request.app.state.templates.TemplateResponse(
        "match.html",
        {"request": request, "resumes": resumes, "result": result, "jd_text": jd_text, "selected_id": resume_id},
    )
