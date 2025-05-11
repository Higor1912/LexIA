from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
import uvicorn

app = FastAPI()

# Permitir acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou especifique ['http://localhost']
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carrega o pipeline de perguntas e respostas
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# Dicionário com diferentes contextos jurídicos
contextos = {
    "estágio": (
        "De acordo com a Lei do Estágio (Lei nº 11.788/2008), os estagiários têm os seguintes direitos: "
        "bolsa-auxílio, auxílio-transporte, recesso remunerado proporcional, jornada de até 6 horas diárias, "
        "seguro contra acidentes pessoais, e o contrato pode ter duração de até dois anos."
    ),
    "direito penal": (
        "O Código Penal brasileiro define crimes como ações que violam a lei, como homicídio, roubo, furto e estelionato. "
        "As penas variam conforme a gravidade, podendo incluir reclusão, detenção e multa. "
        "O princípio da presunção de inocência garante que ninguém será considerado culpado até o trânsito em julgado."
    ),
    "contratos": (
        "Um contrato é um acordo entre partes que gera obrigações recíprocas. "
        "Para ser válido, precisa ter: partes capazes, objeto lícito e forma prescrita ou não proibida por lei. "
        "É possível rescindir um contrato por inadimplemento, comum acordo ou cláusulas previamente estipuladas."
    )
}

# Função auxiliar para detectar o contexto
def detectar_contexto(pergunta: str) -> str:
    pergunta_lower = pergunta.lower()
    if "estágio" in pergunta_lower or "estagiário" in pergunta_lower:
        return contextos["estágio"]
    elif "crime" in pergunta_lower or "pena" in pergunta_lower or "prisão" in pergunta_lower:
        return contextos["direito penal"]
    elif "contrato" in pergunta_lower:
        return contextos["contratos"]
    else:
        # Contexto padrão
        return contextos["estágio"]

@app.post("/pergunta")
async def responder(req: Request):
    dados = await req.json()
    pergunta = dados.get("pergunta", "")
    contexto = detectar_contexto(pergunta)
    resposta = qa_pipeline(question=pergunta, context=contexto)
    return {"resposta": resposta["answer"]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001)