import { LegalAssistantAPI } from './api';

class App {
    private api: LegalAssistantAPI;
    private inputElement: HTMLInputElement | null;
    private sendButton: HTMLButtonElement | null;
    private outputElement: HTMLDivElement | null;

    constructor() {
        // Aguarde o DOM carregar completamente
        window.addEventListener('load', () => {
            this.initialize();
        });
    }

    private initialize(): void {
        console.log('Iniciando App...');
        this.api = new LegalAssistantAPI();
        
        // Buscando elementos
        this.inputElement = document.getElementById('input-message') as HTMLInputElement;
        this.sendButton = document.getElementById('send-btn') as HTMLButtonElement;
        this.outputElement = document.getElementById('output-response') as HTMLDivElement;

        // Verificando se encontrou os elementos
        if (!this.inputElement || !this.sendButton || !this.outputElement) {
            console.error('Elementos não encontrados:', {
                input: !!this.inputElement,
                button: !!this.sendButton,
                output: !!this.outputElement
            });
            return;
        }

        console.log('Elementos encontrados, configurando eventos...');
        this.setupEventListeners();
    }

    private setupEventListeners(): void {
        if (!this.inputElement || !this.sendButton) return;

        // Evento de clique no botão
        this.sendButton.addEventListener('click', async (e: MouseEvent) => {
            e.preventDefault();
            console.log('Botão clicado');
            await this.handleSend();
        });

        // Evento de Enter no input
        this.inputElement.addEventListener('keypress', async (e: KeyboardEvent) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                console.log('Enter pressionado');
                await this.handleSend();
            }
        });
    }

    private async handleSend(): Promise<void> {
        if (!this.inputElement || !this.sendButton || !this.outputElement) return;

        const message = this.inputElement.value.trim();
        if (!message) {
            console.log('Mensagem vazia');
            return;
        }

        try {
            console.log('Enviando mensagem:', message);
            this.sendButton.disabled = true;
            this.outputElement.textContent = 'Processando...';

            const response = await this.api.sendMessageToModel(message);
            console.log('Resposta recebida:', response);
            this.outputElement.textContent = response;
            this.inputElement.value = '';
        } catch (error) {
            console.error('Erro ao enviar mensagem:', error);
            this.outputElement.textContent = 'Erro ao processar mensagem. Tente novamente.';
        } finally {
            this.sendButton.disabled = false;
        }
    }
}

// Criar instância quando o documento estiver pronto
new App();