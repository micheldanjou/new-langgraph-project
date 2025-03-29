"""Define a simple chatbot agent using OpenAI."""

from typing import Any, Dict

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph

from agent.configuration import Configuration
from agent.state import State


async def chat_with_openai(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Process the user input with OpenAI's chat model."""
    configuration = Configuration.from_runnable_config(config)
    
    # Initialize the chat model
    chat = ChatOpenAI(
        model=configuration.model_name,
        temperature=configuration.temperature
    )
    
    # Prepare the messages
    messages = [SystemMessage(content=configuration.system_message)]
    
    # Add chat history
    for msg in state.messages:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))
    
    # Add current message
    messages.append(HumanMessage(content=state.current_message))
    
    # Get response from OpenAI
    response = await chat.ainvoke(messages)
    
    # Update state with the new message
    new_messages = state.messages + [
        {"role": "user", "content": state.current_message},
        {"role": "assistant", "content": response.content}
    ]
    
    return {"messages": new_messages}


# Define a new graph
workflow = StateGraph(State, config_schema=Configuration)

# Add the chat node to the graph
workflow.add_node("chat", chat_with_openai)

# Set the entrypoint as chat
workflow.add_edge("__start__", "chat")

# Set the end of the graph to be the chat node
workflow.set_finish_point("chat")

# Compile the workflow into an executable graph
graph = workflow.compile()
graph.name = "OpenAI Chat Graph"
