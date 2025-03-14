from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
)
from flask_login import login_required, current_user
from application.langgraph_interface.langchain_handler import LangGraphHandler


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
    print("\n" + "=" * 40)
    print(f"📩 Message received: {msg}")
    print("=" * 40 + "\n")
    if current_user.profile.profile_id not in user_handlers:
        user_handlers[current_user.profile.profile_id] = LangGraphHandler(
            current_user.profile.profile_id
        )

    llm_instance = user_handlers[current_user.profile.profile_id]
    ai_response = llm_instance.process_chat(msg)

    print("\n" + "-" * 40)
    print(f"🤖 AI Response:\n{ai_response}")
    print("-" * 40 + "\n")
    chat_history.append({"sender": "user", "message": f"👤 User: \n{msg}\n"})
    chat_history.append(
        {"sender": "ai", "message": f"🤖 AI: \n{ai_response}\n"}
    )

    return jsonify({"response": ai_response})


@chat_bp.route("/get_messages", methods=["GET"])
def get_messages():
    return jsonify(chat_history)
