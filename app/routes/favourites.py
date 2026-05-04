from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.favourite import Favourite
from app.models.recipe import Recipe
import uuid

router = APIRouter(prefix="/favourites", tags=["favourites"])

# --- input schema ---
class FavouriteInput(BaseModel):
    user_id: str
    recipe_id: str

# --- routes ---
@router.post("/save")
def save_favourite(data: FavouriteInput, db: Session = Depends(get_db)):
    # check recipe exists
    recipe = db.query(Recipe).filter(
        Recipe.id == uuid.UUID(data.recipe_id)
    ).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    # check not already saved
    existing = db.query(Favourite).filter(
        Favourite.user_id == uuid.UUID(data.user_id),
        Favourite.recipe_id == uuid.UUID(data.recipe_id)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already saved to favourites")

    favourite = Favourite(
        user_id=uuid.UUID(data.user_id),
        recipe_id=uuid.UUID(data.recipe_id)
    )
    db.add(favourite)
    db.commit()
    return {"message": "Recipe saved to favourites"}

@router.get("/{user_id}")
def get_favourites(user_id: str, db: Session = Depends(get_db)):
    favourites = db.query(Favourite).filter(
        Favourite.user_id == uuid.UUID(user_id)
    ).all()
    return {
        "favourites": [
            {"recipe_id": str(f.recipe_id), "saved_at": str(f.saved_at)}
            for f in favourites
        ]
    }