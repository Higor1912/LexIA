const express = require('express');
const path = require('path');
const app = express();

// Middleware para processar JSON
app.use(express.json());

// Servir arquivos estáticos
app.use(express.static(path.join(__dirname, 'src')));

// Rota para a API de chat
app.post('/api/chat', (req, res) => {
    try {
        const { message } = req.body;
        console.log('Mensagem recebida:', message);
        
        // Aqui você pode adicionar sua lógica de processamento
        res.json({ success: true, reply: 'Mensagem recebida com sucesso!' });
    } catch (error) {
        console.error('Erro:', error);
        res.status(500).json({ success: false, error: 'Erro interno do servidor' });
    }
});

// Rota principal
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'src', 'index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Servidor rodando em http://localhost:${PORT}`);
});