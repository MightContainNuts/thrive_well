from langchain_community.retrievers import TavilySearchAPIRetriever


import os
from dotenv import load_dotenv

load_dotenv()


def get_tavily_search_tool(search_query: str):
    """
    Performs a web search using the tavily API.

    This tool allows the agent to retrieve up-to-date and relevant
    information from the web based on a given query.

    Args:
        search_query (str): The search query specifying the information needed.

    Returns:
        list: A list of search results, where each result is a dictionary
        containing:
            - "title" (str): The title of the webpage.
            - "url" (str): The URL of the webpage.
            - "snippet" (str): A brief summary or snippet of the page
             content.

    Example:
        If the user asks, "What are the latest advancements in AI?"
        the function might return:

        [
            {
                "title": "Breakthroughs in AI: 2024",
                "url": "https://example.com/ai-news",
                "snippet": "Researchers have developed a new AI model that."
            },
            ...
        ]

    """
    api_key = os.getenv("TAVILY_API_KEY")
    print(api_key)
    retriever = TavilySearchAPIRetriever(api_key=api_key, k=3)

    response = retriever.invoke(search_query)

    return response
