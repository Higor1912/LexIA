import os
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import traceback

# Carrega variáveis de ambiente
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("A variável de ambiente GOOGLE_API_KEY não está definida")

genai.configure(api_key=api_key)

# Tenta usar gemini-pro, senão usa gemini-pro-vision como fallback
try:
    model = genai.GenerativeModel(model_name="models/gemini-pro")
    # Teste simples para ver se o modelo funciona
    model.generate_content("Teste de conexão com gemini-pro")
except Exception as e:
    print("Falha ao usar gemini-pro, tentando fallback: gemini-pro-vision")
    model = genai.GenerativeModel(model_name="models/gemini-pro-vision")

# Cria o app
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajuste para seu domínio em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo para a pergunta
class Pergunta(BaseModel):
    mensagem: str

@app.post("/pergunta")
async def responder(pergunta: Pergunta):
    try:
        resposta = model.generate_content(pergunta.mensagem)
        return {"resposta": resposta.text}
    except Exception as e:
        print("Erro ao processar a pergunta:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Erro ao processar a pergunta")
