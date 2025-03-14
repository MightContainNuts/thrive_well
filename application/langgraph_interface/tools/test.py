# from langchain_openai import ChatOpenAI
# from langchain_core.tools import tool
# import os
# from dotenv import load_dotenv
# from langgraph.prebuilt import create_react_agent
# from langchain_community.utilities import OpenWeatherMapAPIWrapper
# from langchain_community.tools import WikipediaQueryRun
# from langchain_community.utilities import WikipediaAPIWrapper
# from bs4 import BeautifulSoup
# import wikipedia
# import langgraph
#
# # Load environment variables
# load_dotenv()
#
# # API Keys
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
#
# # Define model
# model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
#
# # Custom Wikipedia Wrapper
# class FixedWikipediaAPIWrapper(WikipediaAPIWrapper):
#     """Custom Wikipedia Wrapper to fix BeautifulSoup parser warning and return summary + link.""" # noqa E501
#
#     def __init__(self, lang="en", top_k_results=1, doc_content_chars_max=200): # noqa E501
#         super().__init__(lang=lang, top_k_results=top_k_results, doc_content_chars_max=doc_content_chars_max) # noqa E501
#
#     def run(self, query: str):
#         """Search Wikipedia and return only the summary and the page URL."""
#         try:
#             page = wikipedia.page(query)
#             soup = BeautifulSoup(page.html(), "html.parser")
#             paragraphs = soup.find_all("p")
#             summary = paragraphs[0].get_text(strip=True) if paragraphs else "No summary available." # noqa E501
#             return {"summary": summary, "url": page.url}
#
#         except wikipedia.exceptions.DisambiguationError as e:
#             return {"summary": f"Disambiguation error: {e.options}", "url": None} # noqa E501
#         except wikipedia.exceptions.PageError:
#             return {"summary": "No page found for the query.", "url": None}
#
# # Define tools
# @tool
# def get_weather(city: str):
#     """Get the weather for a given city."""
#     weather = OpenWeatherMapAPIWrapper(openweathermap_api_key=OPENWEATHERMAP_API_KEY) # noqa E501
#     return weather.run(city)
#
# @tool
# def get_wiki_summary(topic: str):
#     """Get the summary for a given topic."""
#     wikipedia = WikipediaQueryRun(api_wrapper=FixedWikipediaAPIWrapper(
#         lang="en", top_k_results=1, doc_content_chars_max=200
#     ))
#     return wikipedia.run(topic)
#
# @tool
# def generate_response(query: str):
#     """Generate a response when no suitable tool is found."""
#     return model.invoke(query).content
#
# # Combine tools
# tools = [get_weather, get_wiki_summary, generate_response]
#
# # **Step 1: Validation Function**
# def validate_query(inputs):
#     """Validate user query before tool selection."""
#     user_input = inputs["messages"][-1][1]  # Extract last user message
#     if len(user_input) < 3:  # Example rule: Query should be meaningful
#         return {"messages": [("system", "Query is too short. Please provide more details.")]} # noqa E501
#
#     return inputs  # If valid, continue to tool selection
#
# # **Step 2: Create Agent (Tool Selector)**
# agent = create_react_agent(model, tools=tools)
#
# # **Step 3: Define LangGraph Workflow**
# workflow = langgraph.Graph()
#
# workflow.add_node("validate_query", validate_query)
# workflow.add_node("agent", agent)
#
# workflow.set_entry_point("validate_query")
# workflow.add_edge("validate_query", "agent")  # Forward only valid queries
#
# # **Step 4: Create Graph**
# graph = workflow.compile()
#
# # **Step 5: Define Stream Printer**
# def print_stream(stream):
#     for s in stream:
#         message = s["messages"][-1]
#         print(message)
#
# # **Step 6: Run Example Queries**
# inputs = {"messages": [("user", "whats the weather like in Halle")]}
# print_stream(graph.stream(inputs, stream_mode="values"))
#
# inputs = {"messages": [("user", "How old is the city of Halle?")]}
# print_stream(graph.stream(inputs, stream_mode="values"))
#
# inputs = {"messages": [("user", "Hi")]}  # Invalid query
# print_stream(graph.stream(inputs, stream_mode="values"))
