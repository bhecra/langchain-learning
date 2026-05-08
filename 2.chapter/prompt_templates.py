from langchain_core.prompts import PromptTemplate

template = "Eres un experto en marketing digital. Crea una estrategia de marketing digital para el siguiente producto: {producto}"

prompt = PromptTemplate(
    input_variables=["producto"],
    template=template
)

formatted_prompt = prompt.format(producto="Café organico")
print(formatted_prompt)