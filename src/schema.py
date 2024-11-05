from pydantic import BaseModel
from typing import List

class kb_article_schema(BaseModel):
    title: str
    category: str
    content: str
    created: str
    author: str
    status: str

class kb_article_list_schema(BaseModel):
    value: List[kb_article_schema]

class service_request_schema(BaseModel):
    id: int
    title: str
    service: str
    content: str
    created: str
    author: str
    status: str