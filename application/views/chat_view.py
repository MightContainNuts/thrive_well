from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
)
from flask_login import login_required, current_user
from application.utils.langchain_handler import LangChainHandler


chat_bp = Blueprint("chat", __name__)

# Define a route for the chat page
chat_history = []
user_handlers = {}


@chat_bp.route("/chatbot")
def chatbot():
    return render_template("chat.html")  # Your chat interface


# Define SocketIO event handlers for the chat
@login_required
@chat_bp.route("/send_message", methods=["POST"])
def send_message():
    data = request.json
    msg = data.get("message")
    print(f"Message received: {msg}")
    if current_user.profile.profile_id not in user_handlers:
        user_handlers[current_user.profile.profile_id] = LangChainHandler(
            current_user.profile.profile_id
        )

    llm_instance = user_handlers[current_user.profile.profile_id]
    ai_response = llm_instance.process_chat(msg)

    print(f"AI Response: {ai_response}")
    chat_history.append({"sender": "user", "message": msg})
    chat_history.append({"sender": "ai", "message": ai_response})

    return jsonify({"response": ai_response})


@chat_bp.route("/get_messages", methods=["GET"])
def get_messages():
    return jsonify(chat_history)
