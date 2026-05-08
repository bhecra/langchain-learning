from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

question = "Cual es el mejor candidado a la presidencia en colombia 2026?"

result = llm.invoke(question)

print(result.content)