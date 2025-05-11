#!/bin/bash

# Parar tudo primeiro
pkill -f "ollama serve"
pkill -f "main.py"
pkill -f "streamlit"
sleep 2

# Ir para diretório
cd /home/siaa/ollama-api
source venv/bin/activate

# Iniciar serviços
echo "Iniciando sistema..."

# Ollama
OLLAMA_HOST=0.0.0.0 ollama serve > logs/ollama.log 2>&1 &
sleep 5

# API
python api/main.py > logs/api.log 2>&1 &
sleep 3

# Interface do Cliente
streamlit run api/client_interface.py --server.port 8502 --server.address 0.0.0.0 > logs/client.log 2>&1 &

echo "Sistema iniciado!"
echo "Acesse: http://192.168.1.21:8502"
