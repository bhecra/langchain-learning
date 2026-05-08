from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_openai import ChatOpenAI
import json

#configuracion del modelo
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def preprocess_text(text):
    """Limpia el texto eliminando espacios extras y limitando longitud"""
    return text.strip().lower()[:500]

preprocessor = RunnableLambda(preprocess_text)

def generate_summary(text):
    """Genera un resumen conciso del texto"""
    prompt = f"Resume en una sola oración: {text}"
    response = llm.invoke(prompt)
    return response.content

summary_branch = RunnableLambda(generate_summary)

def analyze_sentiment(text):
    """Analiza el sentimiento y devuelve resultado estructurado"""
    prompt = f"""Analiza el sentimiento del siguiente texto.
    Responde ÚNICAMENTE en formato JSON válido:
    {{"sentimiento": "positivo|negativo|neutro", "razon": "justificación breve"}}
    
    Texto: {text}"""
    
    response = llm.invoke(prompt)
    try:
        return json.loads(response.content)
    except json.JSONDecodeError:
        return {"sentimiento": "neutro", "razon": "Error en análisis"}

sentiment_branch = RunnableLambda(analyze_sentiment)


def merge_results(data):
    """Combina los resultados de ambas ramas en un formato unificado"""
    return {
        "resumen": data["resumen"],
        "sentimiento": data["sentimiento_data"]["sentimiento"],
        "razon": data["sentimiento_data"]["razon"]
    }

merger =  RunnableLambda(merge_results)

parallel_analysis = RunnableParallel({"resumen": summary_branch, "sentimiento_data": sentiment_branch})

chain = preprocessor | parallel_analysis | merger

# Prueba con diferentes textos
textos_prueba = [
    "¡Me encanta este producto! Funciona perfectamente y llegó muy rápido.",
    "El servicio al cliente fue terrible, nadie me ayudó con mi problema.",
    "El clima está nublado hoy, probablemente llueva más tarde."
]

batch_results = chain.batch(textos_prueba)

print(f"Resultado del batch: {batch_results}")
print("-" * 50)
for batch in batch_results:
    print(f"Texto: {batch['resumen']}")
    print(f"Sentimiento: {batch['sentimiento']}")
    print(f"Razon: {batch['razon']}")
    print("-" * 50)


#Reflexiones finales: 
#¿Qué ventajas tiene dividir el procesamiento en funciones separadas?
## Separar responsabilidades, mejorar la legibilidad y mantenibilidad del codigo.

#¿Cómo mejorarías la precisión del análisis de sentimientos?
## Bajar la temperatura del modelo para que sea mas preciso.

#¿Qué otros de análisis podrías añadir a este sistema?
## Analisis de emociones, analisis de tono, analisis de intensidad, analisis de polaridad, analisis de sentimiento

#¿Cómo manejarías textos en diferentes idiomas?