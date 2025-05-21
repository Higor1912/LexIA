from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Middleware de CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Deixe assim por enquanto. Você pode trocar por ["https://lexia-frontend.onrender.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de dados recebido do frontend
class Pergunta(BaseModel):
    pergunta: str

# Endpoint que processa a pergunta
@app.post("/pergunta")
async def responder(pergunta: Pergunta):
    try:
        resposta = f"Você perguntou: {pergunta.pergunta}"  # Aqui você coloca a lógica real depois
        return {"resposta": resposta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
