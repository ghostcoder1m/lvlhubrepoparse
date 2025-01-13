from sqlalchemy import Column, Integer, String, DateTime
from ..database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    sent_at = Column(DateTime)
    status = Column(String)  # e.g., 'sent', 'failed', 'delivered'

    def __init__(self, content, sent_at, status):
        self.content = content
        self.sent_at = sent_at
        self.status = status

    def __repr__(self):
        return f"<Message(id={self.id}, content='{self.content}', status='{self.status}')>"
