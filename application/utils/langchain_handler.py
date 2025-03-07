import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# from application.utils.structured_outputs import SOJournal
from langchain.memory import ConversationBufferMemory
from typing_extensions import TypedDict
from application.utils.db_handler import DBHandler
from application.app import app

# from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.chains import LLMChain

AIResponse = TypedDict
load_dotenv()


class LangChainHandler:
    def __init__(self, profile_id: str):
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4o-mini"
        self.temperature = 0.7
        self.max_retries = 2
        self.profile_id = profile_id
        self.db_handler = DBHandler()
        self.llm = self.init_model()

    def __repr__(self):
        return (
            f"LangChainHandler(model={self.model}, "
            f"temperature={self.temperature}, "
            f"max_retries={self.max_retries}),"
            f"profile_id={self.profile_id}"
        )

    def __str__(self):
        return (
            f"LangChainHandler(model={self.model}, "
            f"temperature={self.temperature}, "
            f"max_retries={self.max_retries}),"
            f"profile_id={self.profile_id}"
        )

    def init_model(self):
        """initialise chat model"""
        prompt = ChatPromptTemplate(
            [
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{text}"),
            ]
        )
        memory = self.get_conversation_chain()
        return LLMChain(
            llm=ChatOpenAI(
                model=self.model,
                temperature=self.temperature,
                max_retries=self.max_retries,
            ),
            prompt=prompt,
            memory=memory,
        )

    def analyze_chat_entry(self, user_query: str) -> AIResponse:
        """analyze journal entry using langchain"""
        content = """
        You are a helpful assistant focused on the well-being of
        others. Categorize the mood of the text as either "positive",
        "negative" or "neutral". Followed by assisting or answering any
        questions asked. The response should be helpful and informative.
        Summarise keywords used in the text and response.
        """

        messages = [
            {"role": "system", "content": content},
            {"role": "user", "content": user_query},
        ]

        response = self.llm.invoke(messages)
        mood = response["mood"]
        keywords = response["keywords"]
        user_query = user_query
        ai_response = response["ai_response"]
        self.db_handler.write_chat_message_to_history(
            profile_id=self.profile_id,
            mood=mood,
            user_query=user_query,
            ai_response=ai_response,
            keywords=keywords,
        )

        return response

    def get_conversation_chain(self):
        """get conversation chain"""
        chat_history = self.db_handler.get_chat_history(  # noqa F841
            profile_id=self.profile_id
        )
        memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )

        return memory


if __name__ == "__main__":
    with app.app_context():
        profile_id = "b926fc86-5ffd-4fc6-a777-e55669166140"
        handler = LangChainHandler(profile_id=profile_id)
        print(handler.analyze_chat_entry("What did we talk about last time"))
