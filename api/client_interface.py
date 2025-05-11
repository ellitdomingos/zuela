import streamlit as st
import requests
import json
from datetime import datetime

# Configuração inicial do Streamlit
st.set_page_config(page_title="Zuela Chat", layout="wide")

# API Configuration
API_URL = "http://localhost:5001"

# Inicializar session_state para histórico de mensagens
if 'mensagens' not in st.session_state:
    st.session_state.mensagens = []

# Função para adicionar mensagem ao histórico
def adicionar_mensagem(role, content):
    st.session_state.mensagens.append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })

# Título principal
st.title("Zuela Chat")

# Área do chat
chat_container = st.container()

# Exibir histórico de mensagens
with chat_container:
    for msg in st.session_state.mensagens:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.write(f"**Você** ({msg['timestamp']}):")
                st.write(msg["content"])
        else:
            with st.chat_message("assistant"):
                st.write(f"**IA** ({msg['timestamp']}):")
                st.write(msg["content"])

# Input do usuário
pergunta = st.chat_input("Digite sua mensagem...")

if pergunta:
    # Adicionar pergunta do usuário ao histórico
    adicionar_mensagem("user", pergunta)
    
    # Processar resposta da API
    with st.spinner("Processando..."):
        try:
            # Preparar mensagens para API
            api_messages = [{
                "role": msg["role"],
                "content": msg["content"]
            } for msg in st.session_state.mensagens]
            
            # Chamar API
            response = requests.post(
                f"{API_URL}/api/chat",
                json={
                    "messages": api_messages,
                    "temperature": 0.7,
                    "max_tokens": 500
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get("response", "Erro ao processar resposta.")
                adicionar_mensagem("assistant", ai_response)
            else:
                st.error("Erro ao chamar API.")
            
            # Recarregar a página para mostrar a nova mensagem
            st.rerun()
            
        except Exception as e:
            st.error(f"Erro ao processar mensagem: {str(e)}")

# Sidebar com instruções e controles
with st.sidebar:
    st.markdown("### Instruções de Uso")
    
    st.markdown("""
    **Chat de Teste da API:**
    - Digite suas mensagens no campo abaixo
    - Veja as respostas da IA em tempo real
    - Mantenha uma conversa contínua sobre qualquer tópico
    
    **Exemplos:**
    > "Olá, como você pode me ajudar?"
    > "Me fale sobre inteligência artificial"
    > "Que tal uma piada?"
    """)
    
    # Botão para limpar histórico
    if st.button("Limpar Conversa"):
        st.session_state.mensagens = []
        st.rerun()
    
    # Status do sistema
    st.markdown("---")
    st.markdown("### Status do Sistema")
    st.success("Chat ativo")
    st.info(f"Mensagens na conversa: {len(st.session_state.mensagens)}")
    
    # Informações da API
    st.markdown("---")
    st.markdown("### Informações")
    st.markdown(f"""
    **API URL:** `{API_URL}`
    
    **Sobre:**
    - Interface de teste para API Llama
    - Desenvolvido com Streamlit
    - Foco na funcionalidade da API
    """)
    
    st.markdown("---")
    st.markdown("Desenvolvido por [Eliseu Domingos](mailto:elitdomingos@gmail.com)")

if __name__ == "__main__":
    pass
