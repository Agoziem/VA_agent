from typing import AsyncIterator, Optional
from app.modules.agents.VA_graph import graph
from uuid import uuid4
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage
import json


class VAServices:
    """
    This class provides methods to interact with the VA services.
    """

    async def generate_chat_response(self, message: str, checkpoint_id: Optional[str] = None) -> AsyncIterator[str]:
        """
        Generates a response for the given user input.
        """
        is_new_checkpoint = checkpoint_id is None or checkpoint_id == "null"
        print("end point called with message:", message)
        if is_new_checkpoint:
            new_checkpoint_id = str(uuid4())

            thread_config = RunnableConfig(
                {"configurable": {
                    "thread_id": new_checkpoint_id,
                }}
            )
            events = graph.astream_events({
                "messages": [
                    HumanMessage(content=message),
                ]
            }, config=thread_config, version="v2")

            yield f"data: {json.dumps({
                'type': 'checkpoint',
                'checkpoint_id': new_checkpoint_id})}\n\n"

        else:
            thread_config = RunnableConfig(
                {"configurable": {
                    "thread_id": checkpoint_id,
                }}
            )

            events = graph.astream_events({
                "messages": [
                    HumanMessage(content=message),
                ]
            }, config=thread_config, version="v2")

        async for event in events:
            event_type = event.get("event")
            data = event.get("data", {})

            # when the Ai model starts streaming data
            if event_type == "on_chat_model_stream":
                chunk = data.get("chunk")
                if chunk and hasattr(chunk, "content"):
                    yield f"data: {json.dumps({'type': 'content', 'content': chunk.content})}\n\n"

            # when the Ai model ends streaming data and returns the final output
            elif event_type == "on_chat_model_end":
                output = data.get("output")
                tool_calls = getattr(output, "tool_calls", []) if output else []
                search_calls = [call for call in tool_calls if call.get("name") == "tavily_search"]
                # confirms that the search tool was called
                if search_calls:
                    query = search_calls[0].get("args", {}).get("query", "")
                    yield f"data: {json.dumps({'type': 'search_start', 'query': query})}\n\n"
            
            # when a tool call ends and returns the search results
            elif event_type == "on_tool_end" and event.get("name") == "tavily_search":
                output = data.get("output")
                results = output.get("results", []) if isinstance(output, dict) else []
                if isinstance(results, list):
                    urls = [result["url"] for result in results if isinstance(result, dict) and "url" in result]
                    urls_json = json.dumps(urls)
                    yield f"data: {json.dumps({'type': 'search_results', 'urls': urls_json})}\n\n"

        yield f"data: {json.dumps({'type': 'end'})}\n\n"


               
