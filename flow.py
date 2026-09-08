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

#state is the info the graph is carrying while it executes
#has all the info that gets passed between the nodes of the graph
#used to store kind of previous-context

#dict means that our state will look something like this
# state = {"messages": [....]}
class State(dict):  
    #whenever this field gets updated , use add_messages to determin how new messages should be combined with others
    messages: Annotated[list , add_messages]

#this is a langGraph node. receives current state , gives the state to LLM and returns the LLM'S response as an update to state
#chatbot is expecting input of state
def chatbot(state: State):
    #take the current state , sends that to the LLM and then takes the LLM's response and returns it as a new message to be added to the state
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


def router(state: State):
    #getting the last message of the conversation because that is the response the chatbot just generated
    last_message = state["messages"][-1]

    #checks if the LLM has asked for a tool or not because either LLM can ask for a tool or it can directly answer on its own without using tool

    #we are checking if the last message have tool calls and if tes , then are there actually any tool calls
    if hasattr(last_message , "tool_calls") and last_message.tool_calls:
        return "tools"
    else:
        return END


#graph_builder is just used to describe the graph
#creating a graph whose state follows State
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot" , chatbot)
graph_builder.add_node("tools" , tool_node)
graph_builder.add_edge(START , "chatbot")
graph_builder.add_edge("tools", "chatbot")

#after chatbot is done , router will decide what will happen next
graph_builder.add_conditional_edges("chatbot", router)


#this is used to store checkpoints of the graph's state in memory
#stores graph-state checkpoints in memory so the state can be persisted across graph execution
memory = InMemorySaver()

#this is where the graph actually becomes an executable one
#passing checkpointer so that when this graph runs , this checkpointer to be used to save state
graph = graph_builder.compile(checkpointer=memory)



if __name__ == "__main__":
    while True:
        prompt = input("Pass your prompt here: ")

        #now executing the graph with initial state as {"messages": [{"role":"user" , "content":prompt}]}
        #we need configuration to tell langGraph to save checkpoints for this execution thread
        #thread_id identifies which conversation this state belongs to
        result = graph.invoke({"messages":[{"role":"user" , "content":prompt}]}, config={"configurable":{"thread_id":1234}})
        print(result["messages"][-1].content)