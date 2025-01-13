from sqlalchemy import Column, Integer, String, ForeignKey
from ..database import Base

class Element(Base):
    __tablename__ = "elements"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)  # e.g., 'text', 'image', 'button'
    content = Column(String)
    page_id = Column(Integer, ForeignKey("pages.id"))

    def __init__(self, type, content, page_id):
        self.type = type
        self.content = content
        self.page_id = page_id

    def __repr__(self):
        return f"<Element(id={self.id}, type='{self.type}')>"
