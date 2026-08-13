from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field, ValidationError
from typing import Annotated

NonVuota = Annotated[str, Field(min_length=1)]

class Formazione(BaseModel):
    portiere: list[NonVuota] = Field(
        min_length=1,
        max_length=1,
        description="Nome della persona che giocherà in porta"
    )

    difensori: list[NonVuota] = Field(
        min_length=4,
        max_length=4,
        description="Nome delle persone che giocheranno in difesa"
    )

    centrocampisti: list[NonVuota] = Field(
        min_length=3,
        max_length=3,
        description="Nome delle persone che giocheranno a centrocampo"
    )

    attaccanti: list[NonVuota] = Field(
        min_length=3,
        max_length=3,
        description="Nome delle persone che giocheranno in attacco"
    )

giocatori_validi = [
    "Gianluigi Donnarumma",
    "William Saliba",
    "Achraf Hakimi",
    "Theo Hernández",
    "Virgil van Dijk",
    "Rodri",
    "Jude Bellingham",
    "Pedri",
    "Vinícius Júnior",
    "Erling Haaland",
    "Bukayo Saka"
]

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

try:
    response = chain.invoke({
       "testo": "La formazione è composta da Gianluigi Donnarumma in porta. In difesa giocano William Saliba, Achraf Hakimi, Theo Hernández e Virgil van Dijk. A centrocampo ci sono Rodri, Jude Bellingham e Pedri. In attacco giocano Vinícius Júnior, Erling Haaland e Bukayo Saka."
    })

    tutti_i_giocatori = (
    response.portiere
    + response.difensori
    + response.centrocampisti
    + response.attaccanti
    )

    for giocatore in tutti_i_giocatori:
        if giocatore not in giocatori_validi:
            raise ValueError(
                f"Giocatore non presente nella formazione: {giocatore}"
            )

    if len(tutti_i_giocatori) != len(set(tutti_i_giocatori)):
        raise ValueError(
            "Un giocatore è stato assegnato a più ruoli."
        )

    giocatori_mancanti = set(giocatori_validi) - set(tutti_i_giocatori)

    if giocatori_mancanti:
        raise ValueError(
            f"Giocatori mancanti nella formazione: {giocatori_mancanti}"
        )

    print(response)

except ValidationError as e:
    print("ERRORE DI VALIDAZIONE:")
    print(e)

except ValueError as e:
    print("ERRORE DATI:")
    print(e)