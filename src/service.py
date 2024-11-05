from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader
from model import Base, kb_article
from schema import kb_article_schema, kb_article_list_schema
from db_helper import SessionLocal, engine
from sqlalchemy.orm import Session

# define API key, header, and validation
API_KEYS = [
    "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
]
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header is None:
        raise HTTPException(status_code=401, detail="401 Unauthorized: No API Key provided")
    if api_key_header not in API_KEYS:
        raise HTTPException(status_code=403, detail="403 Forbidden: Incorrect API Key")
    return api_key_header

# kick off db
Base.metadata.create_all(bind=engine)

# init FastAPI app
app = FastAPI()

# define db dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# root blurb for tests
@app.get("/")
async def root(api_key: str = Security(get_api_key)):
    return { "message": "Copilot Extensibility Demo API. Use CRUD requests to interact with /kb for Knowledge Base scenario and /requests for Service Requests or Tickets scenario" }

# POST seed kb articles
@app.post("/kb/seed")
async def seed_kb_articles(request: kb_article_list_schema, db: Session = Depends(get_db), api_key: str = Security(get_api_key)):
    for article in request.value:
        new_kb_article = kb_article(title=article.title, category=article.category, content=article.content, created=article.created, author=article.author, status=article.status)
        db.add(new_kb_article)
    db.commit()
    return { "message": "200 SUCCESS: Articles were seeded" }

# DELETE purge all kb articles
@app.delete("/kb/purge")
async def purge_kb_articles(db: Session = Depends(get_db), api_key: str = Security(get_api_key)):
    db.query(kb_article).delete()
    db.commit()
    return { "message": "200 SUCCESS: Articles were purged" }

# POST new kb article
@app.post("/kb")
async def post_kb_article(request: kb_article_schema, db: Session = Depends(get_db), api_key: str = Security(get_api_key)):
    new_kb_article = kb_article(title=request.title, category=request.category, content=request.content, created=request.created, author=request.author, status=request.status)
    db.add(new_kb_article)
    db.commit()
    db.refresh(new_kb_article)
    return new_kb_article

# GET all kb articles
@app.get("/kb")
async def get_kb_articles(db: Session = Depends(get_db), api_key: str = Security(get_api_key)):
    return db.query(kb_article).all()

# GET kb article by id
@app.get("/kb/{id}")
async def get_kb_article(id: int, db: Session = Depends(get_db), api_key: str = Security(get_api_key)):
    result = db.query(kb_article).filter(kb_article.id == id).first()
    if result is None:
        raise HTTPException(status_code=404, detail="404 NOT FOUND: Article not found")
    return result

# PATCH kb article by id (no optional parameters for now)
@app.patch("/kb/{id}")
async def patch_kb_article(id: int, request: kb_article_schema, db: Session = Depends(get_db), api_key: str = Security(get_api_key)):
    result = db.query(kb_article).filter(kb_article.id == id).first()
    if result is None:
        raise HTTPException(status_code=404, detail="404 NOT FOUND: Article not found")
    for key, value in request.model_dump().items():
        setattr(result, key, value)
    db.commit()
    db.refresh(result)
    return result

# DELETE kb article by id
@app.delete("/kb/{id}")
async def delete_kb_article(id: int, db: Session = Depends(get_db), api_key: str = Security(get_api_key)):
    result = db.query(kb_article).filter(kb_article.id == id).first()
    if result is None:
        raise HTTPException(status_code=404, detail="404 NOT FOUND: Article not found")
    db.delete(result)
    db.commit()
    return { "message": "200 SUCCESS: Article was deleted" }