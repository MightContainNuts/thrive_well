from flask import Blueprint, redirect, url_for, session
import requests


def auth_views(google):
    auth = Blueprint("auth", __name__)

    @auth.route("/login")
    def login():
        return google.authorize_redirect(
            url_for("auth.oauth_callback", _external=True)
        )  # noqa E501

    @auth.route("/logout")
    def logout():
        token = session.get("google_token")
        if token:
            # Revoking the token using Google's revocation endpoint
            revoke_url = "https://oauth2.googleapis.com/revoke"
            response = requests.post(
                revoke_url, data={"token": token["access_token"]}
            )  # noqa E501

            if response.status_code == 200:
                print("Successfully revoked the token.")
            else:
                print("Failed to revoke the token.")

        # Clear the session
        session.pop("google_token", None)
        return redirect(url_for("main.index"))

    @auth.route("/oauth-authorized")
    def oauth_callback():
        token = google.authorize_access_token()
        if not token:
            return "Access denied: no token received."

        user_info = google.get("userinfo").json()
        session["user"] = user_info  # Store user info in session
        return f"Logged in as {user_info['email']}"

    return auth
