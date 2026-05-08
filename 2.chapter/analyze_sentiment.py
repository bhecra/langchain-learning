from langchain_core.runnables import RunnableLambda
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

def merge_results(data):
    """Combina los resultados de ambas ramas en un formato unificado"""
    return {
        "resumen": data["resumen"],
        "sentimiento": data["sentimiento_data"]["sentimiento"],
        "razon": data["sentimiento_data"]["razon"]
    }

def process_one(t):
    resumen = generate_summary(t)              # Llamada 1 al LLM
    sentimiento_data = analyze_sentiment(t)    # Llamada 2 al LLM
    return merge_results({
        "resumen": resumen,
        "sentimiento_data": sentimiento_data
    })
 
# Convertir en Runnable
process = RunnableLambda(process_one)

chain = preprocessor | process

# Prueba con diferentes textos
textos_prueba = [
    "¡Me encanta este producto! Funciona perfectamente y llegó muy rápido.",
    "El servicio al cliente fue terrible, nadie me ayudó con mi problema.",
    "El clima está nublado hoy, probablemente llueva más tarde."
]

for texto in textos_prueba:
    resultado = chain.invoke(texto)
    print(f"Texto: {texto}")
    print(f"Resultado: {resultado}")
    print("-" * 50)


#Reflexiones finales: 
#¿Qué ventajas tiene dividir el procesamiento en funciones separadas?
## Separar responsabilidades, mejorar la legibilidad y mantenibilidad del codigo.

#¿Cómo mejorarías la precisión del análisis de sentimientos?
## Bajar la temperatura del modelo para que sea mas preciso.

#¿Qué otros de análisis podrías añadir a este sistema?
## Analisis de emociones, analisis de tono, analisis de intensidad, analisis de polaridad, analisis de sentimiento

#¿Cómo manejarías textos en diferentes idiomas?