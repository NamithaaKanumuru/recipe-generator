from fastapi import FastAPI
from app.database import engine, Base
from app.models import user, recipe, favourite
from app.routes import auth, recipes, favourites

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Recipe Generator API")

# register routes
app.include_router(auth.router)
app.include_router(recipes.router)
app.include_router(favourites.router)

@app.get("/")
def root():
    return {"message": "Recipe Generator API is running"}