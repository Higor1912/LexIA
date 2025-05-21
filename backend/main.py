from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os

# Configure a chave de API do Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Criação do modelo Gemini
model = genai.GeminiPro()  # Nome correto da classe

app = FastAPI()

# CORS para permitir acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Altere depois para seu domínio exato
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo da pergunta recebida
class Pergunta(BaseModel):
    pergunta: str

# Rota da API que responde com base na Gemini
@app.post("/pergunta")
async def responder(pergunta: Pergunta):
    try:
        response = model.generate_content(pergunta.pergunta)
        resposta = response.text.strip()
        return {"resposta": resposta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar resposta: {e}")
