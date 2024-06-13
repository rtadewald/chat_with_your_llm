import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv, find_dotenv

# Carrega variáveis de ambiente
_ = load_dotenv(find_dotenv())

st.title("Chat com Modelo de Linguagem - LangChain")

# Configuração do prompt e do modelo
system = "You are a helpful assistant."
human = "{text}"
prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
chat = ChatGroq(temperature=0, model_name="llama3-8b-8192")
chain = prompt | chat

if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe mensagens do histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Caixa de entrada para o usuário
if user_input := st.chat_input("Você:"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Adiciona um container para a resposta do modelo
    response_stream = chain.stream({"text": user_input})    
    full_response = ""
    
    response_container = st.chat_message("assistant")
    response_text = response_container.empty()
    
    for partial_response in response_stream:
        full_response += str(partial_response.content)
        response_text.markdown(full_response + "▌")

    # Salva a resposta completa no histórico
    st.session_state.messages.append({"role": "assistant", "content": full_response})
