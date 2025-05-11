#!/bin/bash

echo "=== Status Completo do Sistema ==="
echo ""

# 1. Verificar Ollama
echo "1. Ollama Status:"
curl -s http://localhost:11434/api/tags | jq '.models | length' 
echo "   Modelos disponíveis: $(ollama list | grep -v "NAME" | wc -l)"
echo ""

# 2. Verificar API
echo "2. API Status:"
curl -s http://localhost:5001/api/health | jq '.'
echo ""

# 3. Verificar Interface
echo "3. Interface de Teste:"
if curl -s http://localhost:5002 > /dev/null; then
    echo "   ✓ Disponível em http://192.168.1.21:5002"
else
    echo "   ✗ Não disponível"
fi
echo ""

# 4. Teste rápido
echo "4. Teste Rápido:"
curl -s -X POST http://localhost:5001/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "teste"}' | jq '.response'
