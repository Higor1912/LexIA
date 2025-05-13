import { LegalAssistantAPI } from './api.js';

class Chat {
    constructor() {
        this.api = new LegalAssistantAPI();
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.chatArea = document.querySelector('.chat-area');
        this.setupEventListeners();
    }

    setupEventListeners() {
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keypress', (event) => {
            if (event.key === 'Enter') {
                event.preventDefault();
                this.sendMessage();
            }
        });
    }

    async sendMessage() {
        const message = this.messageInput.value.trim();
        
        if (message) {
            // Adiciona mensagem do usuário
            this.addMessageToChat(message, true);
            
            // Limpa o input
            this.messageInput.value = '';
            
            // Adiciona indicador de digitação
            const loadingDiv = this.addLoadingIndicator();
            
            try {
                // Chama a API
                const response = await this.api.sendMessage(message);
                loadingDiv.remove();
                this.addMessageToChat(response);
            } catch (error) {
                console.error('Erro:', error);
                loadingDiv.remove();
                this.addMessageToChat('Desculpe, ocorreu um erro ao processar sua mensagem.');
            }
        }
    }

    addMessageToChat(message, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat ${isUser ? 'chat-end' : 'chat-start'} mb-4`;
        
        messageDiv.innerHTML = `
            <div class="chat-bubble ${isUser ? 'bg-primary text-white' : 'bg-base-200'}">
                ${message}
            </div>
        `;
        
        this.chatArea.appendChild(messageDiv);
        this.chatArea.scrollTop = this.chatArea.scrollHeight;
    }

    addLoadingIndicator() {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'chat chat-start mb-4';
        loadingDiv.innerHTML = `
            <div class="chat-bubble bg-base-200">
                <span class="loading loading-dots loading-sm"></span>
            </div>
        `;
        this.chatArea.appendChild(loadingDiv);
        return loadingDiv;
    }
}

export default Chat;