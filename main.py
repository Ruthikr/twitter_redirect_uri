from fastapi import FastAPI, Request
import os
import requests
from urllib.parse import urlencode
from fastapi.responses import RedirectResponse

app = FastAPI()

TWITTER_REDIRECT_URI = os.getenv("TWITTER_REDIRECT_URI")
CLIENT_ID = os.getenv("TWITTER_CLIENT_ID")
CLIENT_SECRET = os.getenv("TWITTER_CLIENT_SECRET")

@app.get("/")
def home():
    return {"message": "Hello, Twitter OAuth Backend is running!"}

@app.get("/auth/callback")
async def auth_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "Missing code from Twitter"}

    payload = {
        "code": code,
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "redirect_uri": TWITTER_REDIRECT_URI,
        "code_verifier": "challenge",  # Should match the one used in authorize URL
    }

    # Basic Auth header for client_secret (OAuth2 standard)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    # Adding Authorization header (Client credentials)
    auth = (CLIENT_ID, CLIENT_SECRET)

    response = requests.post(
        "https://api.twitter.com/2/oauth2/token",
        data=urlencode(payload),
        headers=headers,
        auth=auth  # Basic Auth
    )

    return response.json()
