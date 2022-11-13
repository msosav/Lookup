import requests
from transformers import pipeline
def procesamiento(texto: str):
    sentiment_pipeline = pipeline("sentiment-analysis")
    lista = list(texto)
    request = sentiment_pipeline(lista)
    if request[0]["label"] == "POSITIVE":
        return True
    else:
        return False 