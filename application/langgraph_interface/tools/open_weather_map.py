from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import os
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from bs4 import BeautifulSoup
import wikipedia


class FixedWikipediaAPIWrapper(WikipediaAPIWrapper):
    """Custom Wikipedia Wrapper to fix BeautifulSoup parser warning
    and return summary + link."""

    def __init__(self, lang="en", top_k_results=1, doc_content_chars_max=200):
        super().__init__(
            lang=lang,
            top_k_results=top_k_results,
            doc_content_chars_max=doc_content_chars_max,
        )

    def run(self, query: str):
        """Search Wikipedia and return only the summary and the page URL."""
        try:
            page = wikipedia.page(query)
            soup = BeautifulSoup(page.html(), "html.parser")
            paragraphs = soup.find_all("p")
            summary = (
                paragraphs[0].get_text(strip=True)
                if paragraphs
                else "No summary available."
            )
            return {"summary": summary, "url": page.url}

        except wikipedia.exceptions.DisambiguationError as e:
            return {
                "summary": f"Disambiguation error: {e.options}",
                "url": None,
            }
        except wikipedia.exceptions.PageError:
            return {"summary": "No page found for the query.", "url": None}


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)


@tool
def get_weather(city: str):
    """Get the weather for a given city."""

    weather = OpenWeatherMapAPIWrapper(
        openweathermap_api_key=os.getenv("OPENWEATHERMAP_API_KEY")
    )
    weather_data = weather.run(city)
    return weather_data


@tool
def get_wiki_summary(topic: str):
    """Get the summary for a given topic."""
    wikipedia = WikipediaQueryRun(
        api_wrapper=FixedWikipediaAPIWrapper(
            lang="en", top_k_results=1, doc_content_chars_max=200
        )
    )
    summary = wikipedia.run(topic)
    return summary


tools = [get_weather, get_wiki_summary]
graph = create_react_agent(model, tools=tools)


def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()


inputs = {"messages": [("user", "whats the weather like in Halle")]}
print_stream(graph.stream(inputs, stream_mode="values"))

inputs = {"messages": [("user", "How old is the city of Halle")]}
print_stream(graph.stream(inputs, stream_mode="values"))
