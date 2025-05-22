import os
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import traceback

# Carrega variáveis de ambiente
load_dotenv()

# Chaves de API
api_key_primary = os.getenv("GOOGLE_API_KEY")
api_key_backup = os.getenv("GOOGLE_API_KEY_BACKUP")  # Segunda chave opcional

if not api_key_primary:
    raise ValueError("A variável de ambiente GOOGLE_API_KEY não está definida")

# Inicializa os modelos
def inicializar_modelo(chave):
    genai.configure(api_key=chave)
    return genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

model_primary = inicializar_modelo(api_key_primary)
model_backup = inicializar_modelo(api_key_backup) if api_key_backup else None

# Testa conexão com o modelo primário
try:
    model_primary.generate_content("Teste de conexão com gemini-1.5-pro-latest")
except Exception:
    print("❌ Falha ao configurar o modelo primário:")
    traceback.print_exc()
    raise RuntimeError("Erro ao inicializar o modelo primário")

# Cria o app FastAPI
app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de entrada
class Pergunta(BaseModel):
    mensagem: str

# Função de geração com fallback
def gerar_resposta(pergunta: str):
    try:
        resposta = model_primary.generate_content(pergunta)
        return resposta.text
    except Exception as e:
        print("⚠️ Falha no modelo primário:", e)
        if model_backup:
            try:
                resposta = model_backup.generate_content(pergunta)
                return resposta.text
            except Exception as e2:
                print("❌ Falha no modelo backup também:")
                traceback.print_exc()
                raise RuntimeError("Falha nos dois modelos")
        else:
            traceback.print_exc()
            raise RuntimeError("Falha no modelo primário e não há backup disponível")

# Rota da API
@app.post("/pergunta")
async def responder(pergunta: Pergunta):
    try:
        resposta_texto = gerar_resposta(pergunta.mensagem)
        return {"resposta": resposta_texto}
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao processar a pergunta")
