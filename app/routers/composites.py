from fastapi import Depends, APIRouter
from starlette.requests import Request
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from .. stylegan import style_transfer
import pickle

router = APIRouter(
    tags = ["Composites"]
)

@router.get('/composite')
def composite_image(request: Request, content_id : int, style_id: int, db : Session = Depends(get_db)):

    #Recieve the latest content and style images
    content_path = f"content.JPEG"
    style_path = f"style.JPEG"

    #Run the ML model and save the composite image
    composite_image = style_transfer(content_path, style_path)
    composite_filepath = "comp.JPEG"
    composite_image.save(composite_filepath)

    #Pickle the image to put in DB
    pickled_comp_image = pickle.dumps(composite_image)

    #Store the image in the database
    new_post = models.Composite(content_id = content_id, style_id = style_id, composite_str = pickled_comp_image)
    db.add(new_post)
    db.commit()
   
    return {"message": "composite image uploaded"}