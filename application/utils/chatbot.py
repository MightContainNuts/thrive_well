import uuid
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.chat_history import InMemoryChatMessageHistory

# Define a new graph
builder = StateGraph(state_schema=MessagesState)
load_dotenv()

# Define a chat model
model = ChatOpenAI(model="gpt-4o-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
chats_by_session_id = {}


# Define the function that calls the model
def call_model(
    state: MessagesState, config: RunnableConfig
) -> list[BaseMessage]:
    # Make sure that config is populated with the session id
    if (
        "configurable" not in config
        or "session_id" not in config["configurable"]
    ):
        raise ValueError(
            "Make sure that the config includes the following information: {'configurable': {'session_id': 'some_value'}}"  # noqa E501
        )
    # Fetch the history of messages and append to it any new messages.
    chat_history = get_chat_history(config["configurable"]["session_id"])
    messages = list(chat_history.messages) + state["messages"]
    ai_message = model.invoke(messages)
    # Finally, update the chat message history to include
    # the new input message from the user together with the
    # repsonse from the model.
    chat_history.add_messages(state["messages"] + [ai_message])
    return {"messages": ai_message}


def get_chat_history(session_id: str) -> InMemoryChatMessageHistory:
    chat_history = chats_by_session_id.get(session_id)
    if chat_history is None:
        chat_history = InMemoryChatMessageHistory()
        chats_by_session_id[session_id] = chat_history
    return chat_history


# Define the two nodes we will cycle between
builder.add_edge(START, "model")
builder.add_node("model", call_model)

graph = builder.compile()

# Here, we'll create a unique session ID to identify the conversation
session_id = uuid.uuid4()
config = {"configurable": {"session_id": session_id}}

input_message = HumanMessage(content="hi! I'm bob")
for event in graph.stream(
    {"messages": [input_message]}, config, stream_mode="values"
):
    event["messages"][-1].pretty_print()

# Here, let's confirm that the AI remembers our name!
input_message = HumanMessage(content="what was my name?")
for event in graph.stream(
    {"messages": [input_message]}, config, stream_mode="values"
):
    event["messages"][-1].pretty_print()
