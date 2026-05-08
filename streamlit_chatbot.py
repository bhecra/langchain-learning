from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import streamlit as st
from langchain_core.prompts import PromptTemplate
 
# Configurar la página de la app
st.set_page_config(page_title="Chatbot Básico", page_icon="🤖")
st.title("🤖 Chatbot Básico con LangChain")
st.markdown("Este es un *chatbot de ejemplo* construido con LangChain + Streamlit. ¡Escribe tu mensaje abajo para comenzar!")

with st.sidebar:
    st.header("Configuración")
    model_name = st.selectbox("Selecciona el modelo", ["gpt-4o-mini", "gpt-4o", "gpt-4o-mini-2024-07-18"])
    temperature = st.slider("Temperatura", min_value=0.0, max_value=1.0, value=0.5, step=0.1)

chat_model = ChatOpenAI(model=model_name, temperature=temperature)

prompt_template = PromptTemplate(
    input_variables=["mensaje", "historial"],
    template="""Eres un asistente útil y amigable llamado ChatBot Pro. 
 
Historial de conversación:
{historial}
 
Responde de manera clara y concisa a la siguiente pregunta: {mensaje}"""
)
 
# Inicializar el historial de mensajes
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
 
# Mostrar mensajes previos en la interfaz
for msg in st.session_state.mensajes:
    if isinstance(msg, SystemMessage):
        # No muestro el mensaje por pantalla
        continue
    
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

chain = prompt_template | chat_model
 
# Cuadro de entrada de texto de usuario
pregunta = st.chat_input("Escribe tu mensaje: ")


 
if pregunta:

    # Mostrar inmediatamente el mensaje del usuario en la interfaz
    with st.chat_message("user"):
        st.markdown(pregunta)

    
    try:
        # Mostrar la respuesta en la interfaz
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""

            for chunk in chain.stream({"mensaje": pregunta, "historial": st.session_state.mensajes}):
                full_response += chunk.content
                response_placeholder.markdown(full_response + "▌")

            response_placeholder.markdown(full_response)
        
        # Almacenamos el mensaje en la memoria de streamlit
        st.session_state.mensajes.append(HumanMessage(content=pregunta))
        st.session_state.mensajes.append(AIMessage(content=full_response))
    except Exception as e:
        st.error(f"Error al generar la respuesta: {e}")
        st.info("Verifica que tu API Key de OpenAI esté configurada correctamente.")

if st.button("🗑️ Nueva conversación"):
    st.session_state.mensajes = []
    st.rerun()