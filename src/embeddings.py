from langchain_ollama import OllamaEmbeddings
import math


# ============================================================
# 1. MODELLO DI EMBEDDING
# ============================================================

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# ============================================================
# 2. DOMANDA E DOCUMENTI
# ============================================================

domanda = "Dove abita Michele?"

documenti = [
    "Michele vive a Napoli.",
    "Michele possiede una bicicletta rossa.",
    "Michele studia intelligenza artificiale.",
]


# ============================================================
# 3. CREIAMO L'EMBEDDING DELLA DOMANDA
# ============================================================

vettore_domanda = embeddings.embed_query(domanda)


# ============================================================
# 4. CREIAMO GLI EMBEDDING DEI DOCUMENTI
# ============================================================

vettori_documenti = []

for documento in documenti:
    vettore = embeddings.embed_query(documento)
    vettori_documenti.append(vettore)


# ============================================================
# 5. COSINE SIMILARITY
# ============================================================

def cosine_similarity(vettore_a, vettore_b):

    prodotto_scalare = sum(
        a * b
        for a, b in zip(vettore_a, vettore_b)
    )

    norma_a = math.sqrt(
        sum(a * a for a in vettore_a)
    )

    norma_b = math.sqrt(
        sum(b * b for b in vettore_b)
    )

    return prodotto_scalare / (norma_a * norma_b)


# ============================================================
# 6. CONFRONTIAMO LA DOMANDA CON OGNI DOCUMENTO
# ============================================================

print("\n=== SIMILARITÀ ===")

for documento, vettore_documento in zip(
    documenti,
    vettori_documenti
):

    similarita = cosine_similarity(
        vettore_domanda,
        vettore_documento
    )

    print(f"{similarita:.4f} -> {documento}")