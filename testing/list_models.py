from google import genai

client = genai.Client(api_key="AIzaSyDE_HMtsya4KrMk4pFCS0IqTmerCR9GSaA")

for model in client.models.list():
    print(model.name)