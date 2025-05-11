import streamlit as st
import requests
import json
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Ollama API Test",
    page_icon="🤖",
    layout="centered"
)

# URL da API
API_URL = "http://localhost:5001"

# Título
st.title("🤖 Ollama API Test Interface")

# Verificar conexão com API
@st.cache_data(ttl=60)
def check_api():
    try:
        response = requests.get(f"{API_URL}/api/health", timeout=5)
        return response.status_code == 200, response.json()
    except:
        return False, None

# Status da API
api_status, api_info = check_api()
if api_status:
    st.success(f"✓ API conectada - Modelo: {api_info.get('available_model', 'N/A')}")
    st.json(api_info)
else:
    st.error("✗ API não está disponível")
    st.stop()

# Tabs
tab1, tab2 = st.tabs(["Generate", "Chat"])

# Tab 1: Generate
with tab1:
    st.header("Text Generation")
    
    prompt = st.text_area("Prompt:", value="Explique machine learning em 2 frases", height=100)
    
    col1, col2 = st.columns(2)
    with col1:
        temperature = st.slider("Temperature", 0.1, 2.0, 0.7, 0.1)
    with col2:
        max_tokens = st.number_input("Max Tokens", min_value=10, max_value=2000, value=500)
    
    if st.button("Generate", key="generate"):
        if prompt:
            with st.spinner("Gerando texto..."):
                try:
                    response = requests.post(
                        f"{API_URL}/api/generate",
                        json={
                            "prompt": prompt,
                            "temperature": temperature,
                            "max_tokens": max_tokens
                        },
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.subheader("Resultado:")
                        st.write(result['response'])
                        
                        # Info técnica
                        with st.expander("Detalhes técnicos"):
                            st.write(f"Tempo de processamento: {result.get('processing_time', 'N/A')}s")
                            st.write(f"Modelo: {result.get('model', 'N/A')}")
                            st.write(f"Timestamp: {result.get('timestamp', 'N/A')}")
                    else:
                        st.error(f"Erro: {response.status_code}")
                        st.json(response.json())
                        
                except Exception as e:
                    st.error(f"Erro ao conectar com API: {str(e)}")
        else:
            st.warning("Por favor, digite um prompt")

# Tab 2: Chat
with tab2:
    st.header("Chat Interface")
    
    # Inicializar histórico
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Mostrar histórico
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input do usuário
    if prompt := st.chat_input("Digite sua mensagem..."):
        # Adicionar mensagem do usuário
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Obter resposta da API
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                try:
                    response = requests.post(
                        f"{API_URL}/api/chat",
                        json={
                            "messages": st.session_state.messages,
                            "temperature": temperature,
                            "max_tokens": max_tokens
                        },
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        reply = result.get('response', 'Sem resposta')
                        st.markdown(reply)
                        
                        # Adicionar ao histórico
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": reply
                        })
                        
                        # Info técnica
                        with st.expander("Detalhes"):
                            st.write(f"Tempo: {result.get('processing_time', 'N/A')}s")
                    else:
                        st.error(f"Erro: {response.status_code}")
                        st.json(response.json())
                        
                except Exception as e:
                    st.error(f"Erro: {str(e)}")
    
    # Botão para limpar chat
    if st.button("Limpar Chat"):
        st.session_state.messages = []
        st.rerun()

# Sidebar com informações
with st.sidebar:
    st.header("API Information")
    
    st.write("**Endpoints disponíveis:**")
    st.code("""
GET  /api/health
POST /api/generate
POST /api/chat
    """)
    
    st.write("**Exemplo curl:**")
    st.code("""
curl -X POST http://192.168.1.21:5001/api/generate \\
  -H "Content-Type: application/json" \\
  -d '{"prompt": "Hello", "temperature": 0.7}'
    """)
    
    if st.button("Testar Conectividade"):
        with st.spinner("Testando..."):
            is_connected, info = check_api()
            if is_connected:
                st.success("✓ Conexão OK")
            else:
                st.error("✗ Sem conexão")
