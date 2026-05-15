from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pydantic import BaseModel
import asyncio

from src.agent import run_research


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    """
    When the browser vistis localhost:8000
    serve the homepage (index.html)
    """
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/chat", response_class=HTMLResponse)
async def chatpage(request: Request):
    """
    When the browser visits localhost:8000/chat
    serve the chat page (chat.html)
    """
    return templates.TemplateResponse(request=request, name="chat.html")


class ResearchRequest(BaseModel):
    """
    This defines what data we expect from the browser
    when it send a research question.
    """
    question: str


def stream_report(question: str):
    """
    Runs the research agent and yields the report
    word by word so it streams in the browser.
    """
    report = run_research(question)
    words = report.split()
    for word in words:
        yield word + " "


@app.post("/research")
async def research(req: ResearchRequest):
    """When the browser sends a research question:
    1. Run the research agent
    2. Stream the report back word by word
    """
    return StreamingResponse(
        stream_report(req.question),
        media_type="text/plain"
    )