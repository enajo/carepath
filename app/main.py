from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .config import APP_VERSION, ENV
from .models import TriageRequest, TriageResponse
from .rules import DISCLAIMER, evaluate
from .storage import append_event, read_recent

app = FastAPI(title="CarePath", version=APP_VERSION)

BASE_DIR = Path(__file__).resolve().parent

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "env": ENV, "version": APP_VERSION}


@app.get("/favicon.ico")
def favicon() -> Response:
    # Avoid noisy 404s in logs from browsers and scanners.
    # Returning 204 (No Content) is enough for this demo project.
    return Response(status_code=204)


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "version": APP_VERSION,
            "env": ENV,
            "disclaimer": DISCLAIMER,
        },
    )


@app.post("/triage", response_model=TriageResponse)
def triage(payload: TriageRequest):
    result = evaluate(payload)

    now = datetime.now(timezone.utc)
    response = TriageResponse(
        category=result.category,
        reasons=result.reasons,
        disclaimer=DISCLAIMER,
        version=APP_VERSION,
        timestamp=now,
    )

    # Save a compact history entry (optional but nice)
    append_event(
        {
            "category": response.category,
            "reasons": response.reasons,
            "version": response.version,
            "timestamp": response.timestamp.isoformat(),
        }
    )

    return response


@app.get("/triage/history")
def history():
    return JSONResponse({"items": read_recent()})
