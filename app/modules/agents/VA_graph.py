from langgraph.graph import StateGraph, START,MessagesState
from .agents import (
    va_agent,
    enhancer_agent,
    research_agent,
    todo_agent
)
from langgraph.checkpoint.memory import MemorySaver

# Create the stateful graph
builder = StateGraph(MessagesState)

# Add nodes
builder.add_node("va_agent", va_agent)
builder.add_node("enhancer_agent", enhancer_agent)
builder.add_node("research_agent", research_agent)
builder.add_node("todo_agent", todo_agent)

# Define entry point
builder.add_edge(START, "va_agent")


# Build the graph
checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)
