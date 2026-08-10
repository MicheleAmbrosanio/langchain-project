from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    message: str
    count: int
    status: str


def greet(state: State) -> State:
    return {
        "message": f"Ciao! Hai detto: {state['message']}",
        "count": state["count"],
    }


def count_message(state: State) -> State:
    return {
        "message": state["message"],
        "count": len(state["message"]),
    }

def set_status(state: State) -> State:
    if state["count"] > 30:
        status = "messaggio lungo"
    else:
        status = "messaggio breve"

    return {
        "message": state["message"],
        "count": state["count"],
        "status": status,
    }

builder = StateGraph(State)

builder.add_node("greet", greet)
builder.add_node("count_message", count_message)
builder.add_node("set_status", set_status)

builder.add_edge(START, "greet")
builder.add_edge("greet", "count_message")
builder.add_edge("count_message", END)
builder.add_edge("count_message", "set_status")
builder.add_edge("set_status", END)

graph = builder.compile()


if __name__ == "__main__":
    result = graph.invoke(
        {
            "message": "sto imparando LangGraph",
            "count": 0,
            "status": "",
        }
    )

    print(result)