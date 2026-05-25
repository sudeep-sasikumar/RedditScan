from __future__ import annotations
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

_REQUIRED_VARS = ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USER_AGENT"]
_missing = [v for v in _REQUIRED_VARS if not os.getenv(v)]
if _missing:
    print("ERROR: Missing required environment variables:")
    for var in _missing:
        print(f"  - {var}")
    print("Copy .env.example to .env and fill in your Reddit credentials.")
    sys.exit(1)

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

import analyzer
import reddit_client
from models import AnalysisResult, ResearchRequest, ResearchResponse

app = FastAPI(title="SubSight")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_FRONTEND = Path(__file__).parent.parent / "frontend" / "index.html"


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "status": "failed"},
    )


@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    return HTMLResponse(content=_FRONTEND.read_text(encoding="utf-8"))


@app.get("/health")
async def health():
    return {"status": "ok", "service": "SubSight"}


@app.post("/api/research", response_model=ResearchResponse)
async def run_research(request: ResearchRequest):
    posts, notes = reddit_client.collect_posts(
        request.subreddits, request.search_queries, request.filters
    )
    analysis_raw = analyzer.analyze(posts)
    analysis_raw["collection_notes"] = notes
    return ResearchResponse(
        label=request.research_label,
        parameters=request.model_dump(),
        analysis=AnalysisResult(**analysis_raw),
        status="success",
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
