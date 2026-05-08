from langchain_core.prompts import ChatPromptTemplate

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un traductor de español a ingles muy preciso."),
    ("user", "{texto}")
])

messages = chat_prompt.format_messages(texto="Hola, como estas?")


for message in messages:
    print(f"Role: {message.type}, Content: {message.content}")
    