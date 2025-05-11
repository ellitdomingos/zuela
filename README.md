# Ollama API Client

🤖 A modern, full-featured client for Ollama API with both chat and text generation capabilities, featuring a beautiful dark-themed interface built with Streamlit.

## 🌟 Features

- **Modern Chat Interface** - Chat with AI using a dark-themed, professional interface
- **Text Generation** - Generate various types of content with predefined templates
- **Multiple Conversations** - Create and manage multiple chat sessions  
- **REST API** - Complete REST API for integration with other applications
- **Docker Support** - Easy deployment with Docker (optional)
- **Persistent Sessions** - Conversations are maintained during your session
- **Responsive Design** - Works seamlessly on desktop and mobile devices

## 🖥️ Screenshots

![image](https://github.com/user-attachments/assets/9cfd206d-f0a8-418b-8ee5-f5eaf339a000)


## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Ollama installed locally
- At least 8GB RAM recommended
- Modern web browser

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/ellitdomingos/zuela.git
cd ollama-api-client
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Start Ollama service**
```bash
ollama serve
```

5. **Download a model** (if not already done)
```bash
ollama pull llama3.2:1b
```

6. **Start the application**
```bash
./start.sh
```

7. **Access the interface**
   - Client Interface: http://localhost:8502
   - API Documentation: http://localhost:5001/api/health

## 📁 Project Structure

```
ollama-api-client/
├── api/
│   ├── main.py                 # REST API server
│   └── client_interface.py     # Streamlit client interface  
├── logs/                       # Application logs
├── venv/                       # Python virtual environment
├── start.sh                    # Start all services
├── stop.sh                     # Stop all services
├── status.sh                   # Check service status
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🔧 Usage

### Chat Interface

1. Visit http://localhost:8502
2. Type your message and press Enter
3. Switch between conversations using the sidebar


### API Usage

The REST API is available at http://localhost:5001

#### Generate Text
```bash
curl -X POST http://localhost:5001/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain machine learning in simple terms",
    "temperature": 0.7,
    "max_tokens": 500
  }'
```

#### Chat
```bash
curl -X POST http://localhost:5001/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Hello!"}
    ],
    "temperature": 0.7
  }'
```

#### Health Check
```bash
curl http://localhost:5001/api/health
```

## 🐳 Docker Deployment (Optional)

### Build and run with Docker

```bash
# Build the image
docker build -t ollama-api-client .

# Run the container
docker run -p 8502:8502 -p 5001:5001 ollama-api-client
```

### Docker Compose

```yaml
version: '3.8'
services:
  ollama-api:
    build: .
    ports:
      - "8502:8502"
      - "5001:5001"
    volumes:
      - ./logs:/app/logs
    environment:
      - OLLAMA_HOST=0.0.0.0
```

## ⚙️ Configuration

### Environment Variables

```bash
export OLLAMA_HOST=0.0.0.0       # Ollama server host
export OLLAMA_PORT=11434         # Ollama server port  
export API_PORT=5001             # API server port
export CLIENT_PORT=8502          # Client interface port
```

### Customizing Models

Edit `api/main.py` to change the default model:

```python
DEFAULT_MODEL = "llama3.2:1b"  # Change to your preferred model
```

## 📚 API Documentation

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Check API status |
| `/api/generate` | POST | Generate text |
| `/api/chat` | POST | Chat with AI |

### Request/Response Examples

See full API documentation at `/api/docs` when running locally.

## 🔍 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   ./stop.sh  # Stop all services
   ./start.sh # Restart
   ```

2. **API not responding**
   ```bash
   ./status.sh  # Check service status
   ```

3. **Model not found**
   ```bash
   ollama list  # List available models
   ollama pull model-name  # Download missing model
   ```

### Logs

Check logs for detailed error information:
```bash
tail -f logs/api.log
tail -f logs/client.log
```

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) first.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) - Amazing local LLM runtime
- [Streamlit](https://streamlit.io/) - Beautiful web framework
- [Flask](https://flask.palletsprojects.com/) - Lightweight API framework

## 📞 Support

- Email: elitdomingos@gmail.com 



---

Made with  by [Eliseu Domingos](https://github.com/your-username)
