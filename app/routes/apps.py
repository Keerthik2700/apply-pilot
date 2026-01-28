from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Application, AppStatus
from app.security import decode_token, COOKIE_NAME

router = APIRouter()


def user_id_or_redirect(request: Request):
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        return None
    return decode_token(token)


@router.get("/apps")
def apps_page(request: Request, db: Session = Depends(get_db)):
    uid = user_id_or_redirect(request)
    if not uid:
        return RedirectResponse("/login", status_code=303)

    apps = (
        db.query(Application)
        .filter(Application.user_id == uid)
        .order_by(Application.updated_at.desc())
        .all()
    )
    return request.app.state.templates.TemplateResponse("apps.html", {"request": request, "apps": apps})


@router.get("/apps/new")
def app_new(request: Request):
    uid = user_id_or_redirect(request)
    if not uid:
        return RedirectResponse("/login", status_code=303)
    return request.app.state.templates.TemplateResponse("app_form.html", {"request": request, "app": None})


@router.post("/apps/new")
def app_create(
    request: Request,
    company: str = Form(...),
    role: str = Form(...),
    location: str = Form(""),
    status: str = Form("applied"),
    jd_text: str = Form(""),
    notes: str = Form(""),
    db: Session = Depends(get_db),
):
    uid = user_id_or_redirect(request)
    if not uid:
        return RedirectResponse("/login", status_code=303)

    app = Application(
        user_id=uid,
        company=company.strip(),
        role=role.strip(),
        location=location.strip(),
        status=AppStatus(status),
        jd_text=jd_text,
        notes=notes,
    )
    db.add(app)
    db.commit()
    return RedirectResponse("/apps", status_code=303)


@router.post("/apps/{app_id}/delete")
def app_delete(app_id: int, request: Request, db: Session = Depends(get_db)):
    uid = user_id_or_redirect(request)
    if not uid:
        return RedirectResponse("/login", status_code=303)

    app = db.query(Application).filter(Application.id == app_id, Application.user_id == uid).first()
    if app:
        db.delete(app)
        db.commit()
    return RedirectResponse("/apps", status_code=303)
