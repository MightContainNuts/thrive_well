import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import pandas as pd
import re

load_dotenv()


def google_search(query):
    url = "https://www.googleapis.com/customsearch/v1"

    params = {
        "key": os.getenv("GOOGLE_SEARCH_API_KEY"),
        "cx": os.getenv("GOOGLE_SEARCH_ENGINE_ID"),
        "q": f"ways to support someone with {query} cancer",
    }
    response = requests.get(url, params=params)
    return response.json()


def clean_text(page_text):
    soup = BeautifulSoup(page_text, "html.parser")

    for element in soup(
        ["script", "style", "header", "footer", "nav", "aside"]
    ):  # noqa E501
        element.decompose()

    cleaned_text = soup.get_text()
    cleaned_text = re.sub(r"\s+", " ", cleaned_text)
    cleaned_text = cleaned_text.strip()
    cleaned_text = re.sub(
        r"(Copyright|Privacy Policy|Terms of Service).*", "", cleaned_text  # noqa E501
    )

    return cleaned_text


def scrape_page(google_search_results):
    scraped_data = []
    if not google_search_results:
        return None

    for item in google_search_results.get("items", []):
        url = item["link"]
        print(f"Scraping: {url}")

        try:
            response = requests.get(url)
            response.raise_for_status()
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                page_text = soup.get_text()
                clean_text_content = clean_text(page_text)
                scraped_data.append({"url": url, "text": clean_text_content})

        except Exception as e:
            print(f"Error scraping {url}: {e}")

    df = pd.DataFrame(scraped_data)
    print(df)
    return df


if __name__ == "__main__":
    results = google_search(query="breast")
    scrape_page(results)
