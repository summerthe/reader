from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from bs4 import BeautifulSoup
import requests

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/render", response_class=HTMLResponse)
async def render_page(request: Request, url: str = Form(None), html_content: str = Form(None)):
    if url:
        # Fetch the page source if URL is provided
        response = requests.get(url)
        html_content = response.text

    if html_content:
        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script_or_style in soup(["script", "style", "header", "footer", "nav", "img", "svg", "figure", "i"]):
            script_or_style.decompose()
        
        # Get the cleaned HTML content
        cleaned_html = str(soup)
        print("cleaned_html,",cleaned_html)
        return templates.TemplateResponse(
            "rendered.html",
            {"request": request, "cleaned_html": cleaned_html}
        )
    else:
        return "No URL or HTML content provided."
