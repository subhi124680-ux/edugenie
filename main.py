import os

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from dotenv import load_dotenv
from google import genai

load_dotenv()

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
)


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.post("/generate")
async def generate(
    request: Request,
    prompt: str = Form(...)
):

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )

        result = response.text

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "prompt": prompt,
                "result": result
            }
        )

    except Exception as e:

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "prompt": prompt,
                "result": f"Error: {str(e)}"
            }
        )