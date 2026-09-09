This project is a simple stock screener agent built using LangGraph.

The system starts by taking a user's prompt and passing it to the LLM. Since this project is a stock screener, the prompt is mainly expected to be related to fetching or screening information about stocks or other financial assets.

The prompt is stored in the graph's state, specifically in the messages field. The LLM then processes the prompt and decides whether it can answer the query directly or needs additional information from a tool.

If the LLM can answer the question directly, it generates a normal response. The router checks the LLM's response, sees that there are no tool calls, and ends the graph execution.

If the LLM needs external information, it generates a tool call specifying which tool it wants to use and the arguments required. The router detects the tool call and routes the execution to the ToolNode.

The ToolNode executes the actual Python tool, simple_screener. This tool uses the yfinance library to interact with Yahoo Finance and retrieve the required stock information. It then processes the retrieved data and returns the relevant results.

The tool result is then added back to the graph's state and passed to the LLM. The LLM uses this information to generate the final response for the user. The router checks the LLM's response again, and if there are no further tool calls, the graph ends.