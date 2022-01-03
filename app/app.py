from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from .database import engine
from . import models
from .routers import contents, styles, composites
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory = "templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(contents.router)
app.include_router(styles.router)
app.include_router(composites.router)


@app.get("/hello", response_class=HTMLResponse)
def welcome_page(request: Request):
    data = {"page": "Welcome to the Frontend visitor!"}
    return templates.TemplateResponse("page.html", {"request": request, "data": data})
