from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from markdown import markdown

from src.agent import run_research
from src.report import save_report
from src.history import load_history


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


@app.post("/research", response_class=HTMLResponse)
async def research(request: Request, question: str = Form(...)):
    """
    Receives the question from the HTML form.
    Runs the research agent.
    Returns the result page with the report.
    """
    report = run_research(question)
    save_report(question, report)
    
    report_html = markdown(report)
    history = load_history()
    return templates.TemplateResponse(request=request, name="result.html", context={
        "question": question,
        "report": report_html,
        "history": history
    })