import os

from dotenv import load_dotenv
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain_core.tools import tool


@tool
def get_weather(city: str):
    """
    Retrieves the current weather conditions for a given city from
    OpenWeatherMap.

    This tool allows the agent to fetch real-time weather data for a specified
    city, including key information such as temperature, humidity, weather
    description, and more.

    Args:
        city (str): The name of the city for which the weather information
                    is to be retrieved. The city name will be used to query
                    the OpenWeatherMap API.

    Returns:
        str: A formatted string containing the current weather conditions for
             the specified city, such as temperature, humidity, weather
             description, and other relevant details. If the city is not found
             or an error occurs, a message will indicate the issue.

    Example:
        If the user asks, "What's the weather like in Paris?",
        the agent would fetch the current weather details for Paris and return
        them in a readable format, such as "The current weather in Paris is
        15°C with clear skies."
    """
    print(" Agent is calling the OpenWeatherMapAPIWrapper")
    load_dotenv()
    weather = OpenWeatherMapAPIWrapper(
        openweathermap_api_key=os.getenv("OPENWEATHERMAP_API_KEY")
    )
    weather_data = weather.run(city)
    return weather_data



if __name__ == "__main__":
    print(get_weather.invoke("Berlin"))
