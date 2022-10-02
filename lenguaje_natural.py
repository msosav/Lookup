import requests

def procesamiento(texto: str):
    r = requests.post(url='https://hf.space/embed/Amrrs/gradio-sentiment-analyzer/+/api/predict/', 
    json={"data": [texto]})
    return r.json()

print(procesamiento("Buen producto"))