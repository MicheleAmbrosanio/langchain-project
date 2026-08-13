from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

class Formazione(BaseModel):
    portiere: list[str] = Field(description="Nome della persona che giocherà in porta")
    difensori: list[str] = Field(description="Nome della persona che giocherà in difesa")
    centrocampisti: list[str] = Field(description="Nome della persona che giocherà a centrocampo")
    attaccanti: list[str] = Field(description="Nome della persona che giocherà in attacco")

prompt = ChatPromptTemplate.from_template(
    """Classifica i giocatori della formazione.

MAPPATURA OBBLIGATORIA:
portiere:
difensori:
centrocampisti:
attaccanti:

Testo da classificare:
{testo}
"""
)

model = ChatOllama(model="qwen2.5:3b")

structured_model = model.with_structured_output(Formazione)

chain = prompt | structured_model

response = chain.invoke({
    "testo": "La formazione è composta da Gianluigi Donnarumma in porta. In difesa giocano William Saliba, Achraf Hakimi,Theo Hernández e Virgil van Dijk.A centrocampo ci sono Rodri, Jude Bellingham e Pedri.In attacco giocano Vinícius Júnior, Erling Haaland e Bukayo Saka"
})

print(response)