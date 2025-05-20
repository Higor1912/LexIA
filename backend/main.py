from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
import os

# Carrega variáveis do .env na raiz do projeto
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY não configurada no ambiente.")

# Configura o cliente Google Generative AI
genai.configure(api_key=GOOGLE_API_KEY)

app = FastAPI()

# Configuração do CORS (ajuste origins conforme necessidade)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Para produção, especifique as URLs permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Pergunta(BaseModel):
    pergunta: str

@app.post("/pergunta")
async def responder(pergunta: Pergunta):
    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        resposta = model.generate_content(pergunta.pergunta)
        return {"resposta": resposta.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
