from fastapi import FastAPI
from app.database import engine, Base
from app.models import user, recipe, favourite

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Recipe Generator API")

@app.get("/")
def root():
    return {"message": "Recipe Generator API is running"}