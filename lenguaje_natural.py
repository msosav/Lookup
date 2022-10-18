import requests

def procesamiento(texto: str):
    r = requests.post(url='https://hf.space/embed/Amrrs/gradio-sentiment-analyzer/+/api/predict/',
    json={"data": [texto]})
    texto = r.text
    if (texto.__contains__("POSITIVE")):
        return True
    else:
        return False 

print(procesamiento(""))