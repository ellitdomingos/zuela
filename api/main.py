from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import logging
from datetime import datetime

# Configurações diretas
OLLAMA_URL = "http://localhost:11434"
API_HOST = "0.0.0.0"
API_PORT = 5001

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

def get_available_model():
    """Detectar primeiro modelo disponível"""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            if models:
                return models[0]['name']
    except:
        pass
    return "llama3.2:1b"  # Default fallback

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verificar saúde da API"""
    try:
        available_model = get_available_model()
        test_response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        ollama_status = test_response.status_code == 200
    except Exception as e:
        logger.error(f"Health check error: {e}")
        ollama_status = False
        available_model = None
    
    return jsonify({
        'status': 'healthy' if ollama_status else 'degraded',
        'ollama_available': ollama_status,
        'available_model': available_model,
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/generate', methods=['POST'])
def generate_response():
    """Endpoint principal para geração de texto"""
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({'error': 'Prompt obrigatório'}), 400
        
        prompt = data.get('prompt')
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens', 1000)
        
        model = get_available_model()
        start_time = datetime.now()
        
        payload = {
            'model': model,
            'messages': [{'role': 'user', 'content': prompt}],
            'stream': False,
            'options': {
                'temperature': temperature,
                'num_predict': max_tokens
            }
        }
        
        response = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=60)
        end_time = datetime.now()
        
        if response.status_code == 200:
            result = response.json()
            return jsonify({
                'prompt': prompt,
                'response': result['message']['content'],
                'processing_time': (end_time - start_time).total_seconds(),
                'timestamp': end_time.isoformat(),
                'model': model
            })
        else:
            logger.error(f"Ollama error: {response.status_code} - {response.text}")
            return jsonify({
                'error': f'Ollama error: {response.status_code}',
                'details': response.text
            }), 500
            
    except Exception as e:
        logger.error(f"Generate error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint para chat com histórico"""
    try:
        data = request.get_json()
        
        if not data or 'messages' not in data:
            return jsonify({'error': 'Messages obrigatório'}), 400
        
        messages = data.get('messages')
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens', 1000)
        
        model = get_available_model()
        start_time = datetime.now()
        
        payload = {
            'model': model,
            'messages': messages,
            'stream': False,
            'options': {
                'temperature': temperature,
                'num_predict': max_tokens
            }
        }
        
        response = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=60)
        end_time = datetime.now()
        
        if response.status_code == 200:
            result = response.json()
            return jsonify({
                'response': result['message']['content'],
                'processing_time': (end_time - start_time).total_seconds(),
                'timestamp': end_time.isoformat(),
                'model': model
            })
        else:
            logger.error(f"Ollama chat error: {response.status_code} - {response.text}")
            return jsonify({
                'error': f'Ollama error: {response.status_code}',
                'details': response.text
            }), 500
            
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logger.info(f"Starting Ollama API on {API_HOST}:{API_PORT}")
    app.run(host=API_HOST, port=API_PORT, debug=True)
