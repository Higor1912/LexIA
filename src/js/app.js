import { legalAssistant } from './api.js';

document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    const cards = document.querySelectorAll('.card');
    const chatContainer = document.querySelector('.chat-container');

    // Função para adicionar mensagem no chat
    function addMessageToChat(text, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        messageDiv.textContent = text;
        // Insere a mensagem antes do container de sugestões
        chatContainer.insertBefore(messageDiv, document.querySelector('.suggestion-cards'));
        // Rola para a última mensagem
        messageDiv.scrollIntoView({ behavior: 'smooth' });
    }

    // Event listener para os cards
    cards.forEach(card => {
        card.addEventListener('click', () => {
            const cardContent = card.querySelector('.card-content');
            if (cardContent) {
                const question = cardContent.querySelector('p').textContent;
                userInput.value = question;
                userInput.focus();
            }
        });
    });

    // Função para enviar mensagem
    const sendMessage = async () => {
        const message = userInput.value.trim();
        if (!message) return;

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });

            if (!response.ok) {
                throw new Error('Erro na comunicação com o servidor');
            }

            const data = await response.json();
            console.log('Resposta:', data);
            
            // Limpa o input após envio
            userInput.value = '';
            
        } catch (error) {
            console.error('Erro:', error);
            alert('Erro ao enviar mensagem');
        }
    };

    // Event listeners para envio de mensagem
    sendButton.addEventListener('click', sendMessage);
    
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Log para verificar se o script está carregando
    console.log('Script carregado');

    // Mensagem inicial
    addMessageToChat('Olá! Como posso ajudar você hoje?');
});