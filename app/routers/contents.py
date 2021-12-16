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
    tags = ["Contents"]
)

templates = Jinja2Templates(directory = "templates")

@router.post('/content')
def choose_content_image(db: Session = Depends(get_db), uploaded_file: UploadFile = File(...)):
    
    an_image = pim.open(uploaded_file.file)
    pickled_img = pickle.dumps(an_image)

    new_post = models.Image(image_str = pickled_img,
    filename = uploaded_file.filename)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"message": "content photo uploaded"}



@router.get('/get_content/{id}', response_class=HTMLResponse)
def get_content(id : int, request: Request, db: Session = Depends(get_db)):

    last_image = db.query(models.Image).filter(models.Image.id == id).first()
    unpickled_img = pickle.loads(last_image.image_str)
    unpickled_img.save(f"static\\retrieved\\{id}.JPEG")

    return templates.TemplateResponse('content.html', context={"request": request, "content_id": id})