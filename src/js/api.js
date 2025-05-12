class LegalAssistantAPI {
    constructor() {
        this.API_KEY = process.env.GEMINI_API_KEY;
        this.API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent';
    }

    async sendMessage(userMessage) {
        try {
            const response = await fetch(`${this.API_URL}?key=${this.API_KEY}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    contents: [{
                        parts: [{
                            text: `Você é um assistente jurídico especializado. 
                                  Por favor, responda a seguinte questão de forma 
                                  profissional e precisa: ${userMessage}`
                        }]
                    }],
                    generationConfig: {
                        temperature: 0.7,
                        topK: 40,
                        topP: 0.95,
                        maxOutputTokens: 1024,
                    },
                    safetySettings: [
                        {
                            category: "HARM_CATEGORY_HARASSMENT",
                            threshold: "BLOCK_MEDIUM_AND_ABOVE"
                        },
                        {
                            category: "HARM_CATEGORY_HATE_SPEECH",
                            threshold: "BLOCK_MEDIUM_AND_ABOVE"
                        }
                    ]
                })
            });

            if (!response.ok) {
                throw new Error(`Erro na API: ${response.status}`);
            }

            const data = await response.json();
            return {
                success: true,
                message: data.candidates[0].content.parts[0].text,
                timestamp: new Date().toISOString()
            };

        } catch (error) {
            console.error('Erro ao enviar mensagem:', error);
            return {
                success: false,
                error: error.message,
                timestamp: new Date().toISOString()
            };
        }
    }

    // Método para validar mensagens relacionadas a questões jurídicas
    validateLegalQuery(message) {
        // Implementar validações específicas para consultas jurídicas
        return message.length > 0;
    }

    // Método para formatar a resposta em um formato mais amigável
    formatLegalResponse(response) {
        return {
            answer: response.message,
            disclaimer: "Este é um serviço de assistência jurídica automatizado. Para questões específicas, consulte um advogado.",
            timestamp: response.timestamp
        };
    }
}

export const legalAssistant = new LegalAssistantAPI();