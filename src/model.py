from sqlalchemy import Column, Integer, String, Boolean
from db_helper import Base

#{
#            "title": "Article title here",
#            "category": "Options are: Users, Admins, Decision Makers",
#            "content": "Article content here. One paragraph only.",
#            "created": "2024-11-05",
#            "author": "admin",
#            "status": "published"
#}

class kb_article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    category = Column(String)
    content = Column(String)
    created = Column(String)
    author = Column(String)
    status = Column(String)

class service_request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    service = Column(String)
    content = Column(String)
    created = Column(String)
    author = Column(String)
    status = Column(String)