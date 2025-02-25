import pytest
from flask import Flask
from unittest.mock import patch, MagicMock


from application.views.auth_views import auth_views


@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = "testsecretkey"

    # Mock the google client
    google_mock = MagicMock()

    # Register the blueprint with the mock google object
    app.register_blueprint(auth_views(google_mock))

    return app, google_mock


@pytest.fixture
def client(app):
    app, _ = app  # Unpack the app tuple in the fixture
    return app.test_client()


# Test the login route
def test_login_redirects_to_google(client):
    response = client.get("/login")
    assert response.status_code == 200


# Test the logout route
def test_logout(client):
    # Simulate a logged-in user by adding user info and token to session
    with client.session_transaction() as sess:
        sess["google_token"] = {"access_token": "some_access_token"}
        sess["user"] = {"email": "test@example.com"}

    # Mock the revoke request response
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        response = client.get("/logout")
        assert response
        mock_post.assert_called_once_with(
            "https://oauth2.googleapis.com/revoke",
            data={"token": "some_access_token"},  # noqa E501
        )


# Test the OAuth callback route
def test_oauth_callback(client, app):
    # Access the google_mock object passed to the app fixture
    _, google_mock = app

    # Mock the google OAuth methods
    with patch.object(
        google_mock,
        "authorize_access_token",
        return_value={"access_token": "some_access_token"},
    ):
        with patch.object(google_mock, "get") as mock_get:
            # Mock the user info response
            mock_get.return_value.json.return_value = {
                "email": "test@example.com",
                "name": "Test User",
            }

            # Simulate the OAuth callback route
            response = client.get("/oauth-authorized")

            # Assert that user info is stored in session
            with client.session_transaction() as sess:
                assert sess["user"]["email"] == "test@example.com"
                assert sess["user"]["name"] == "Test User"

            # Check the response contains the correct login message
            assert b"Logged in as test@example.com" in response.data
