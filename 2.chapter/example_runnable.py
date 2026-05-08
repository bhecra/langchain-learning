from langchain_core.runnables import RunnableLambda 

step1 = RunnableLambda(lambda x: x.upper()) 

def duplicate_text(text):
    return text + text

step2 = RunnableLambda(duplicate_text)

chain = step1 | step2

result = chain.invoke("Hola mundo ")

print(result)