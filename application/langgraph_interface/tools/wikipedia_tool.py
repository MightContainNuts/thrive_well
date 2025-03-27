import os

from dotenv import load_dotenv
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)


@tool
def get_wiki_summary(topic: str):
    """
    Fetches a brief summary of a given topic from Wikipedia.

    This tool allows the agent to retrieve a concise and informative summary
    of a specified topic by querying Wikipedia. It helps the agent provide
    relevant and fact-based information to the user, enhancing the quality
    of the conversation. If the query cannot be found or if the summary
    is unavailable, an appropriate message is returned to the user.

    Args:
        topic (str): A string representing the topic or concept the user
                     wants to learn more about.

    Returns:
        str: A brief summary of the Wikipedia article corresponding to
             the query and the URL. If no relevant article is found, a message
             indicating that the topic could not be located will be returned.

    Example:
        If the user asks about "Python programming," the agent would
        retrieve a summary of the Python programming language  and the URL from
        Wikipedia and present it to the user.
    """
    print("Agent is calling the WikipediaQueryRun")
    api_wrapper = WikipediaAPIWrapper(
        top_k_results=1, doc_content_chars_max=100
    )
    wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
    summary = wiki_tool.run(topic)
    return summary
