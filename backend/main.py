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
    ),
    "pj": (
        "Para se tornar Pessoa Jurídica (PJ) no Brasil, é necessário abrir uma empresa. "
        "O processo envolve escolher o tipo de empresa (MEI, EI, LTDA, etc.), registrar o CNPJ na Receita Federal, "
        "obter inscrição estadual/municipal, e emitir notas fiscais. Recomenda-se procurar um contador para orientar em cada etapa."
    ),
    "direito trabalhista": (
        "O Direito Trabalhista regula as relações entre empregadores e empregados. "
        "Inclui temas como carteira assinada, férias, 13º salário, FGTS, jornada de trabalho, rescisão e direitos em caso de demissão."
    ),
    "direito civil": (
        "O Direito Civil trata de temas como família, sucessões, contratos, responsabilidade civil, bens e obrigações. "
        "É a área que regula as relações entre pessoas físicas e jurídicas em âmbito privado."
    ),
    "direito do consumidor": (
        "O Direito do Consumidor protege quem adquire produtos ou serviços. "
        "O Código de Defesa do Consumidor garante direitos como troca de produtos com defeito, arrependimento em compras online e proteção contra práticas abusivas."
    ),
    "direito previdenciário": (
        "O Direito Previdenciário trata dos benefícios do INSS, como aposentadoria, auxílio-doença, pensão por morte e salário-maternidade. "
        "Regula quem tem direito, como solicitar e quais os requisitos para cada benefício."
    ),
    "direito tributário": (
        "O Direito Tributário regula a arrecadação de impostos, taxas e contribuições. "
        "Inclui temas como isenção, restituição, obrigações fiscais e planejamento tributário para pessoas físicas e jurídicas."
    ),
}

# Função auxiliar para detectar o contexto
def detectar_contexto(pergunta: str) -> str:
    pergunta_lower = pergunta.lower()
    if "estágio" in pergunta_lower or "estagiário" in pergunta_lower:
        return contextos["estágio"]
    elif any(p in pergunta_lower for p in ["crime", "pena", "prisão", "homicídio", "furto", "roubo", "estelionato", "criminal"]):
        return contextos["direito penal"]
    elif "contrato" in pergunta_lower or "acordo" in pergunta_lower:
        return contextos["contratos"]
    elif any(p in pergunta_lower for p in ["pj", "pessoa jurídica", "abrir empresa", "cnpj", "empresa", "mei", "lt da"]):
        return contextos["pj"]
    elif any(p in pergunta_lower for p in ["trabalho", "emprego", "clt", "demissão", "rescisão", "carteira assinada", "ferias", "13º", "fgts"]):
        return contextos["direito trabalhista"]
    elif any(p in pergunta_lower for p in ["família", "casamento", "divórcio", "herança", "inventário", "união estável", "direito civil"]):
        return contextos["direito civil"]
    elif any(p in pergunta_lower for p in ["consumidor", "compra", "venda", "troca", "garantia", "produto com defeito", "procon"]):
        return contextos["direito do consumidor"]
    elif any(p in pergunta_lower for p in ["inss", "aposentadoria", "auxílio-doença", "pensão", "previdência", "benefício"]):
        return contextos["direito previdenciário"]
    elif any(p in pergunta_lower for p in ["imposto", "tributo", "taxa", "irpf", "iptu", "icms", "tributário", "fiscal"]):
        return contextos["direito tributário"]
    else:
        # Contexto padrão mais neutro
        return (
            "Não foi possível identificar o contexto jurídico exato da sua pergunta. "
            "Por favor, forneça mais detalhes ou utilize termos como 'estágio', 'contrato', 'crime', 'PJ', 'trabalho', 'consumidor', etc."
        )

@app.post("/pergunta")
async def responder(req: Request):
    dados = await req.json()
    pergunta = dados.get("pergunta", "")
    contexto = detectar_contexto(pergunta)
    resposta = qa_pipeline(question=pergunta, context=contexto)
    resposta_completa = (
        f"Resposta: {resposta['answer']}\n\n"
        f"Explicação adicional: {contexto}"
    )
    return {"resposta": resposta_completa}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001)