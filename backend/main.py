from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os

# Configure sua chave de API Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # ou substitua pelo valor diretamente

model = genai.GenerativeModel("gemini-pro")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Pergunta(BaseModel):
    pergunta: str

@app.post("/pergunta")
async def responder(pergunta: Pergunta):
    try:
        response = model.generate_content(pergunta.pergunta)
        resposta = response.text.strip()
        return {"resposta": resposta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
