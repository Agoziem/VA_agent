import asyncio
from typing import TypedDict, Annotated, List
from langgraph.graph import add_messages, StateGraph, END
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
from langchain_tavily import TavilySearch
from langchain_mcp_adapters.client import MultiServerMCPClient
from app.modules.mcp_servers.config import mcp_config
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.runnables import RunnableConfig


load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile")
search_tool = TavilySearch(max_results=5)


async def setup_tools():
    client = MultiServerMCPClient(mcp_config)
    remote_tools = await client.get_tools()
    tools = remote_tools + [search_tool]
    llm_with_tools = llm.bind_tools(tools)

    return llm_with_tools

memory = MemorySaver()


class State(TypedDict):
    messages: Annotated[List, add_messages]


async def model(state: State) -> State:
    """
    Model function that processes the state and returns it.
    """
    # Convert messages to a format suitable for the LLM
    llm_with_tools = await setup_tools()
    messages = state['messages']

    # Invoke the LLM with the messages
    response = await llm_with_tools.ainvoke(messages)

    return {
        "messages": [response]
    }


async def tool_router(state: State):
    """
    Tool router function that processes the state and returns it.
    """
    messages = state['messages']
    last_message = messages[-1] if messages else None
    # Check if the last message is a ToolMessage
    if last_message and hasattr(last_message, 'tool_calls') and len(last_message.tool_calls) > 0:
        return "tool_node"
    else:
        return END


async def tool_node(state: State):
    """
    Tool node function that processes the state and returns it.
    """
    tool_calls = state['messages'][-1].tool_calls
    if not tool_calls:
        return state
    # Process each tool call
    tool_messages = []
    for tool_call in tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_id = tool_call["id"]

        if tool_name == "tavily_search":
            # Call the Tavily search tool
            search_results = await search_tool.ainvoke(tool_args)
            # Create a ToolMessage with the search results
            tool_message = ToolMessage(
                content=str(search_results),
                name=tool_name,
                tool_call_id=tool_id,
            )
            tool_messages.append(tool_message)
    return {
        "messages": tool_messages
    }

graph_builder = StateGraph(State)

graph_builder.add_node("model", model)
graph_builder.add_node("tool_node", tool_node)

graph_builder.set_entry_point("model")
graph_builder.add_conditional_edges("model", tool_router, path_map={
    "tool_node": "tool_node",
    END: END
})
graph_builder.add_edge("tool_node", "model")


graph = graph_builder.compile(checkpointer=memory)


thread_config = RunnableConfig(
    {"configurable": {
        "thread_id": 15,
    }}
)

events = graph.astream_events({
    "messages": [
        HumanMessage(
            content="can you create a todo for me , about my meeting engagement in the evening "),
    ]
}, config=thread_config, version="v2")


async def handle_stream(events):
    async for event in events:
        print(event)  # Print the event for debugging purposes
        if event["event"] == "on_chat_model_stream":
            if "chunk" in event["data"]:
                # Print the content of the chunk
                print(event["data"]["chunk"].content, end="", flush=True)


# Assuming `events` is an async iterable
asyncio.run(handle_stream(events))
