from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.mock_model import detect_ingredients_and_save
from fastapi.responses import HTMLResponse
import os

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
    print("📥 File received:", file.filename)
    ingredients, image_url = detect_ingredients_and_save(image_bytes)
    print("🍳 Ingredients found:", ingredients)
    return {"ingredients": ingredients, "image_url": image_url}

from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open(os.path.join("frontend", "index.html"), "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read(), headers={"Content-Type": "text/html; charset=utf-8"})
