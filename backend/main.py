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

# Configura a API Gemini com a chave
genai.configure(api_key=api_key)

# Usa o modelo mais recente compatível
try:
    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
    # Testa conexão com o modelo
    model.generate_content("Teste de conexão com gemini-1.5-pro-latest")
except Exception as e:
    print("❌ Falha ao configurar o modelo Gemini:")
    traceback.print_exc()
    raise RuntimeError("Erro ao inicializar o modelo Gemini")

# Cria o app FastAPI
app = FastAPI()

# Middleware CORS (permite requisições de outros domínios)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Idealmente use seu domínio específico em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de entrada
class Pergunta(BaseModel):
    mensagem: str

# Rota de perguntas
@app.post("/pergunta")
async def responder(pergunta: Pergunta):
    try:
        resposta = model.generate_content(pergunta.mensagem)
        return {"resposta": resposta.text}
    except Exception as e:
        print("❌ Erro ao processar a pergunta:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Erro ao processar a pergunta")
