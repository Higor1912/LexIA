import 'dotenv/config';

export class LegalAssistantAPI {
    constructor() {
        // Chave API diretamente no código (para desenvolvimento)
        this.API_KEY = 'AIzaSyDRMPZ7IBZxemeMv1JaaoGZ_I53y1OpjPI';
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
                            text: `Você é um assistente jurídico especializado em direito brasileiro. 
                                  Responda a seguinte questão: ${userMessage}`
                        }]
                    }]
                })
            });

            if (!response.ok) {
                throw new Error(`Erro na API: ${response.status}`);
            }

            const data = await response.json();
            return data.candidates[0].content.parts[0].text;

        } catch (error) {
            console.error('Erro ao chamar API:', error);
            throw error;
        }
    }
}