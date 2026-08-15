from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from pydantic import BaseModel

# ============================================================
# 1. DOCUMENTI
# ============================================================

documenti = [
    "Michele ha 30 anni ed è un programmatore.",
    "Michele vive a Napoli.",
    "Nel tempo libero Michele studia intelligenza artificiale.",
    "Michele possiede una bicicletta rossa.",
]

# ============================================================
# 2. RETRIEVER SEMPLIFICATO
# ============================================================

def cerca_documenti(domanda):
    risultati = []

    parole_chiave = ["vive", "città"]

    for documento in documenti:
        if any(parola in documento.lower() for parola in parole_chiave):
            risultati.append(documento)

    return risultati

# ============================================================
# 3. DOMANDA
# ============================================================

domanda = "Dove vive Michele?"

# ============================================================
# 4. RECUPERO DEI DOCUMENTI
# ============================================================

risultati = cerca_documenti(domanda)

print("=== DOCUMENTI TROVATI ===")

for documento in risultati:
    print("-", documento)

# ============================================================
# 5. CREAZIONE DEL CONTESTO
# ============================================================

contesto = "\n".join(risultati)

print("\n=== CONTESTO ===")
print(contesto)

# ============================================================
# 6. MODELLO
# ============================================================

model = ChatOllama(model="qwen2.5:3b")

# ============================================================
# 7. PROMPT PER LA RISPOSTA
# ============================================================

prompt_risposta = ChatPromptTemplate.from_template(
    """Rispondi alla domanda usando esclusivamente il contesto fornito.

CONTESTO:
{contesto}

DOMANDA:
{domanda}

Se la risposta non è presente nel contesto, rispondi:
"Informazione non presente nel contesto."
"""
)

# ============================================================
# 8. CHAIN
# ============================================================

risposta_chain = prompt_risposta | model

# ============================================================
# 9. INVOCazione DELLA CHAIN
# ============================================================

risposta = risposta_chain.invoke({
    "contesto": contesto,
    "domanda": domanda
})

# ============================================================
# 10. RISULTATO
# ============================================================

print("\n=== RISPOSTA ===")
print(risposta.content)