from fastapi import FastAPI
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from app.routes import auth, apps, resumes, dashboard, match


app = FastAPI(title="ApplyPilot")
@app.get("/")
def root(request: Request):
    return RedirectResponse("/dashboard", status_code=302)


# Templates
templates = Jinja2Templates(directory="app/templates")
app.state.templates = templates

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Routers
app.include_router(auth.router)
app.include_router(apps.router)
app.include_router(resumes.router)
app.include_router(dashboard.router)
app.include_router(match.router)
