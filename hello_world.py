from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

question = "Cual es el mejor candidado a la presidencia en colombia 2026?"

result = llm.invoke(question)

print(result.content)