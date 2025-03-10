import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


from sentence_transformers import SentenceTransformer
from application.utils.extensions import db
from application.db.models import VectorEmbeddings
from application.app import app


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
    ):  # noqa W501

        element.decompose()

    cleaned_text = soup.get_text()
    cleaned_text = re.sub(r"\s+", " ", cleaned_text)
    cleaned_text = cleaned_text.strip()
    cleaned_text = re.sub(
        r"(Copyright|Privacy Policy|Terms of Service).*",
        "",
        cleaned_text,  # noqa W501
    )
    return cleaned_text


def scrape_page(google_search_results, profile_id):

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

    df["embedding"] = df["text"].apply(lambda x: generate_embedding(x))
    df["profile_id"] = profile_id
    return df


def generate_embedding(text):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model.encode(text).tolist()


def add_embeddings_to_db(row):
    embedding_data = VectorEmbeddings(
        profile_id=profile_id,
        url=row["url"],
        text=row["text"],
        embedding=row["embedding"],
    )
    print(f"Adding data to the database: {embedding_data}")
    with app.app_context():
        try:
            db.session.add(embedding_data)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error committing to the database: {e}")


# TODO  testing only - delete after testing
if __name__ == "__main__":
    query = "breast"
    profile_id = "b926fc86-5ffd-4fc6-a777-e55669166140"
    results = google_search(query=query)
    dframe = scrape_page(results, profile_id)

    if dframe is not None:
        for _, row in dframe.iterrows():
            add_embeddings_to_db(row)
