from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from backend.mock_model import detect_ingredients

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    image_bytes = await file.read()
    print("📥 Received file:", file.filename)
    ingredients = detect_ingredients(image_bytes)
    print("🍳 Detected:", ingredients)
    return {"ingredients": ingredients}
