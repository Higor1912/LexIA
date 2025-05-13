import express from 'express';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import cors from 'cors';
import dotenv from 'dotenv';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const port = process.env.PORT || 3001; // Usa a variável de ambiente ou 3001 como fallback

app.use(cors());
app.use(express.json());
app.use(express.static(join(__dirname, 'src')));

app.listen(port, () => {
    console.log(`Servidor rodando em http://localhost:${port}`);
});