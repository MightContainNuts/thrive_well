import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv()


class LangChainHandler:
    def __init__(self):
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4o-mini"
        self.temperature = 0.7
        self.max_retries = 2
        self.llm = self.init_model()

    def __repr__(self):
        return (
            f"LangChainHandler(model={self.model}, "
            f"temperature={self.temperature}, "
            f"max_retries={self.max_retries})"
        )

    def __str__(self):
        return (
            f"LangChainHandler(model={self.model}, "
            f"temperature={self.temperature}, "
            f"max_retries={self.max_retries})"
        )

    def init_model(self):
        """initialise chat model"""
        return ChatOpenAI(
            model=self.model,
            temperature=self.temperature,
            max_retries=self.max_retries,
        )

    def analyze_journal_entry(self, journal_entry: str):
        """analyze journal entry using langchain"""
        return self.llm.invoke(journal_entry).content


if __name__ == "__main__":
    handler = LangChainHandler()
    print(handler.analyze_journal_entry("I am feeling sad today"))
