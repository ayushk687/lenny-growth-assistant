"""
Lenny Growth Assistant — FastAPI application entry point.

Wires together the sessions, messages, and chat API routers, and exposes
a health check endpoint for basic service verification.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import sessions, messages, chat

app = FastAPI(
    title="Lenny Growth Assistant",
    description=(
        "RAG-powered API for querying insights from Lenny's Podcast, "
        "grounded in retrieved transcript excerpts."
    ),
    version="1.0.0",
)

# CORS configuration — adjust allow_origins for your actual frontend origin(s)
# in production. Wildcard is convenient for local development only.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route registration
app.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
app.include_router(messages.router, prefix="/messages", tags=["messages"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])


@app.get("/health", tags=["health"])
def health_check():
    """Basic liveness check — does not verify DB or Ollama connectivity."""
    return {"status": "ok", "service": "lenny-growth-assistant"}


@app.get("/", tags=["health"])
def root():
    return {
        "message": "Lenny Growth Assistant API",
        "docs": "/docs",
    }
