from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.recipe import Recipe
import uuid

router = APIRouter(prefix="/recipes", tags=["recipes"])

# --- input schema ---
class GenerateInput(BaseModel):
    ingredients: list[str]
    user_id: str

# --- routes ---
@router.post("/generate")
def generate_recipe(data: GenerateInput, db: Session = Depends(get_db)):
    # step 1 - validate input
    if not data.ingredients:
        raise HTTPException(status_code=400, detail="Ingredients list cannot be empty")

    # step 2 - call Claude API (placeholder for now)
    # we will replace this in milestone 4
    recipe_data = {
        "title": "Placeholder Recipe",
        "ingredients": ", ".join(data.ingredients),
        "steps": "Step 1: Cook everything. Step 2: Enjoy.",
        "nutrition": "Approx 400 calories"
    }

    # step 3 - save to database
    recipe = Recipe(
        user_id=uuid.UUID(data.user_id),
        title=recipe_data["title"],
        ingredients=recipe_data["ingredients"],
        steps=recipe_data["steps"],
        nutrition=recipe_data["nutrition"]
    )
    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    # step 4 - return response
    return {
        "message": "Recipe generated successfully",
        "recipe": {
            "id": str(recipe.id),
            "title": recipe.title,
            "ingredients": recipe.ingredients,
            "steps": recipe.steps,
            "nutrition": recipe.nutrition
        }
    }

@router.get("/history/{user_id}")
def get_history(user_id: str, db: Session = Depends(get_db)):
    recipes = db.query(Recipe).filter(
        Recipe.user_id == uuid.UUID(user_id)
    ).all()
    return {
        "recipes": [
            {
                "id": str(r.id),
                "title": r.title,
                "ingredients": r.ingredients,
                "created_at": str(r.created_at)
            } for r in recipes
        ]
    }