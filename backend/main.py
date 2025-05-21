import google.generativeai as genai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Configura a chave da API do Gemini
genai.configure(api_key="SUA_API_KEY")

# Instancia o modelo Gemini-Pro corretamente
model = genai.GenerativeModel(model_name="models/gemini-pro")

# Criação da aplicação FastAPI
app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota principal
@app.post("/pergunta")
async def responder(pergunta: dict):
    resposta = model.generate_content(pergunta["mensagem"])
    return {"resposta": resposta.text}

