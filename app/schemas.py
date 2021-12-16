from pydantic import BaseModel

class ImageBase(BaseModel):
    image_str: str
    filename:  str

    class Config:
        orm_mode = True

class StyleBase(BaseModel):
    style_str: str
    filename: str

class CompositeBase(BaseModel):
    content_id : int
    style_id: int
    composite_str : str
