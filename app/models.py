from sqlalchemy.sql.schema import ForeignKey
from .database import Base
from sqlalchemy import Column, Integer, LargeBinary, String

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, nullable=False)
    image_str = Column(LargeBinary, nullable=False)
    filename = Column(String, nullable=False)

class Style(Base):
    __tablename__ = "styles"

    id = Column(Integer, primary_key=True, nullable=False)
    style_str = Column(LargeBinary, nullable=False)
    filename = Column(String, nullable = False)

class Composite(Base):
    __tablename__ = "composites"

    content_id = Column(Integer, ForeignKey("images.id", ondelete="CASCADE"), primary_key=True)
    style_id = Column(Integer, ForeignKey("styles.id", ondelete="CASCADE"), primary_key=True)
    composite_str = Column(LargeBinary, nullable=False)

    # class Vote(Base):
    # __tablename__ = "votes"
    # user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    # post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)


