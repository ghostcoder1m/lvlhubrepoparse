from sqlalchemy import Column, Integer, String, DateTime
from ..database import Base

class Page(Base):
    __tablename__ = "pages"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    created_at = Column(DateTime)

    def __init__(self, title, content, created_at):
        self.title = title
        self.content = content
        self.created_at = created_at

    def __repr__(self):
        return f"<Page(id={self.id}, title='{self.title}')>"
