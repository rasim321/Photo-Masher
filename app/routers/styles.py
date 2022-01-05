from fastapi import File, UploadFile, Depends, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from PIL import Image as pim
import pickle

router = APIRouter(
    tags = ["Styles"]
)

templates = Jinja2Templates(directory = "templates")


@router.post("/style")
def choose_style_image(db: Session = Depends(get_db), style_file : UploadFile= File(...)):
    
    style_image = pim.open(style_file.file)
    pickled_style_img = pickle.dumps(style_image)

    new_post = models.Style(style_str = pickled_style_img,
    filename = style_file.filename)
    db.add(new_post)
    db.commit()

    return{"message": "style image uploaded"}


@router.get('/get_style/{id}', response_class=HTMLResponse)
def get_content(id : int, request: Request, db: Session = Depends(get_db)):

    last_image = db.query(models.Style).filter(models.Style.id == id).first()
    unpickled_img = pickle.loads(last_image.style_str)
    unpickled_img.save(f"style.JPEG")

    return templates.TemplateResponse('content.html', context={"request": request, "style_id": id})

