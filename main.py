from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from app.api.routes.chat import router as chat_router

app = FastAPI(title="Multi-LLM SQL AI System")

# Serve well-known app-specific files (e.g. Chrome DevTools lookup)
app.mount("/.well-known", StaticFiles(directory="app/static/.well-known"), name="well-known")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(router=chat_router, tags=["Chat API"])


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})