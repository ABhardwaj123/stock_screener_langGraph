#ChatOllama gives us LangChain interface for interacting with a chat model
from langchain_ollama import ChatOllama
#helps us to execute tool calls requested by LLMs
from langgraph.prebuilt import ToolNode

#typing module helps us to determine types of things in code like name: str
#Annotated helps us to attach additional information to that type. some kind of instructions/metadata on how some field should be handled
from typing import Annotated

#stateGraph helps us to define the structure of the graph (nodes + edges + state)
from langgraph.graph import START , END , StateGraph

#helps us to properly merge new messages into existing message history
#helps us to maintain the message history that includes user's message , LLM's message
from langgraph.graph.message import add_messages

#keeps the checkpoints in memory. 
#checkpoint is a saved snapshot of graph's state at a particular point
from langgraph.checkpoint.memory import InMemorySaver
from tool import simple_screener

#creating a LLM
llm = ChatOllama(model='qwen2.5:14b')

tools = [simple_screener]

llm_with_tools = llm.bind_tools(tools)

tool_node = ToolNode(tools)