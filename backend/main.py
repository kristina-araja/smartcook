from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from mock_model import detect_ingredients
from fastapi.responses import JSONResponse

app = FastAPI()

# Разрешаем фронту обращаться к бэку
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/detect/")
async def detect(file: UploadFile = File(...)):
    # эмуляция обработки
    contents = await file.read()
    ingredients = detect_ingredients(contents)
    return JSONResponse({"ingredients": ingredients})
