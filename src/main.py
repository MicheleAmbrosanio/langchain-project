from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    message: str


def greet(state: State) -> State:
    return {
        "message": f"Ciao! Hai detto: {state['message']}"
    }


def uppercase(state: State) -> State:
    return {
        "message": state["message"].upper()
    }


builder = StateGraph(State)

builder.add_node("greet", greet)
builder.add_node("uppercase", uppercase)

builder.add_edge(START, "greet")
builder.add_edge("greet", "uppercase")
builder.add_edge("uppercase", END)

graph = builder.compile()


if __name__ == "__main__":
    result = graph.invoke(
        {"message": "sto imparando LangGraph"}
    )

    print(result)