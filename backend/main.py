from fastapi import FastAPI, File, UploadFile, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from backend.mock_model import detect_ingredients_and_save
import os
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/frontend", StaticFiles(directory=os.path.join(os.getcwd(), "frontend")), name="frontend")


@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    image_bytes = await file.read()
    print("📦 File received:", file.filename)
    ingredients, image_url = detect_ingredients_and_save(image_bytes)
    print("🥕 Ingredients detected:", ingredients)
    return {"ingredients": ingredients, "image_url": image_url}


@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open(os.path.join("frontend", "index.html"), "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read(), headers={"Content-Type": "text/html; charset=utf-8"})


@app.get("/get_recipes")
async def get_recipes(ingredients: list[str] = Query(...)):
    api_key = "9232d41ffa00477ca770acf0d0f6206e"  # Replace with your real API key
    url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={','.join(ingredients)}&number=5&apiKey={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        recipes_raw = response.json()

        recipes = []
        for r in recipes_raw:
            recipes.append({
                "id": r["id"],
                "title": r["title"],
                "image": r["image"],
                "usedIngredients": [
                    {"name": ing["name"], "image": ing["image"]} for ing in r.get("usedIngredients", [])
                ],
                "missedIngredients": [
                    {"name": ing["name"], "image": ing["image"]} for ing in r.get("missedIngredients", [])
                ]
            })

        return JSONResponse(content=recipes)

    except requests.RequestException as e:
        print("Error fetching recipes:", str(e))
        return JSONResponse(content={"message": "Failed to fetch recipes"}, status_code=500)
