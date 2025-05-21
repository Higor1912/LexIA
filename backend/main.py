import os
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Carrega variáveis do arquivo .env (para uso local)
load_dotenv()

# Configura a chave da API a partir da variável de ambiente
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("A variável de ambiente GOOGLE_API_KEY não está definida")

genai.configure(api_key=api_key)

# Instancia o modelo Gemini-Pro
model = genai.GenerativeModel(model_name="models/gemini-pro")

# Cria app FastAPI
app = FastAPI()

# Configura CORS para permitir acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajuste para seu domínio em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo para receber a pergunta via JSON
class Pergunta(BaseModel):
    mensagem: str

# Endpoint para responder pergunta
@app.post("/pergunta")
async def responder(pergunta: Pergunta):
    try:
        resposta = model.generate_content(pergunta.mensagem)
        return {"resposta": resposta.text}
    except Exception as e:
        print(f"[ERRO GEMINI] {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar a pergunta")
