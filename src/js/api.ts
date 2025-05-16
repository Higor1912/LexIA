import { OLLAMA_URL } from './config.prod';

interface OllamaResponse {
    model: string;
    created_at: string;
    response: string;
    done: boolean;
    done_reason: string;
}

export class LegalAssistantAPI {
    private API_URL: string;

    constructor() {
        this.API_URL = `${OLLAMA_URL}/api/generate`;
    }

    async sendMessageToModel(userMessage: string): Promise<string> {
        try {
            const response = await fetch(this.API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    model: 'mistral',  // Mudando para o modelo Mistral
                    prompt: `Você é um assistente jurídico especializado em direito trabalhista brasileiro.
                    SEMPRE responda em português do Brasil, de forma clara e direta.

                    CONTEXTO ESPECÍFICO:
                    - CLT (Consolidação das Leis do Trabalho)
                    - Direitos e deveres trabalhistas
                    - Legislação trabalhista atual
                    - Jurisprudência relevante

                    PERGUNTA DO USUÁRIO: "${userMessage}"

                    Responda usando este formato ESPECÍFICO em português:

                    # Título do Tema

                    [Explicação inicial objetiva em 2-3 linhas]

                    ## Principais Direitos e Características
                    1. [Primeiro ponto importante com base legal]
                    2. [Segundo ponto importante com exemplo]
                    3. [Terceiro ponto importante com aplicação prática]

                    ## Legislação Aplicável
                    - Artigo [X] da CLT: [resumo do artigo]
                    - Lei [número]: [ponto relevante]

                    ## Exemplo Prático
                    [Um caso concreto do dia a dia empresarial brasileiro]

                    Lembre-se: Mantenha a resposta 100% em português do Brasil.`,
                    options: {
                        temperature: 0.3,    // Reduzido para respostas mais consistentes
                        top_k: 40,
                        top_p: 0.9,
                        num_predict: 2000
                    },
                    stream: false
                })
            });

            if (!response.ok) {
                throw new Error(`Erro na API: ${response.status}`);
            }

            const data = await response.json() as OllamaResponse;
            
            // Verifica se a resposta está vazia ou muito curta
            if (!data.response || data.response.trim().length < 100) {
                return 'Por favor, reformule sua pergunta. Por exemplo:\n- "Quais são os direitos básicos de um trabalhador CLT?"\n- "Como funciona o contrato PJ?"\n- "Quais as diferenças entre CLT e PJ?"';
            }

            // Limpa a resposta mantendo a formatação markdown
            let cleanResponse = data.response
                .replace(/^\s+|\s+$/g, '')
                .replace(/CONTEXTO ESPECÍFICO:.*?PERGUNTA DO USUÁRIO:/gs, '')
                .replace(/Responda usando este formato.*?português:/gs, '')
                .replace(/Lembre-se:.*$/gs, '')
                .replace(/\n{4,}/g, '\n\n')
                .trim();

            // Verifica conteúdo em inglês
            const englishPatterns = ['hello', 'hi,', 'what is', 'i am', 'example:', 'the', 'this is'];
            if (englishPatterns.some(pattern => cleanResponse.toLowerCase().includes(pattern))) {
                return 'Erro na geração. Por favor, tente novamente com uma pergunta mais específica sobre direito trabalhista brasileiro.';
            }

            return cleanResponse;

        } catch (error) {
            console.error('Erro:', error);
            return 'Ocorreu um erro ao processar sua pergunta. Por favor, tente novamente.';
        }
    }
}