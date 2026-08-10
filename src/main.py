from langchain_ollama import ChatOllama

model = ChatOllama(model="qwen2.5:3b")

response = model.invoke("Spiegami in una frase cos'è LangChain.")

print(response.content)