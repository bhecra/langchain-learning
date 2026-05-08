from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate(
    input_variables=["nombre"],
    template="Salua al usuario con su nombre.  El nombre del usuario es: {nombre}"
)

chat = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

chain = prompt | chat

result = chain.invoke({"nombre": "Juan"})

print(result.content)