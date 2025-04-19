from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import os

app = FastAPI()

TWITTER_REDIRECT_URI = os.getenv("TWITTER_REDIRECT_URI")
CLIENT_ID = os.getenv("TWITTER_CLIENT_ID")
CLIENT_SECRET = os.getenv("TWITTER_CLIENT_SECRET")

@app.get("/")
def home():
    return {"message": "Hello, Twitter OAuth Backend is running!"}

@app.get("/auth/callback")
async def auth_callback(request: Request):
    import requests
    from urllib.parse import urlencode

    code = request.query_params.get("code")
    if not code:
        return {"error": "Missing code from Twitter"}

    payload = {
        "code": code,
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": TWITTER_REDIRECT_URI,
        "code_verifier": "challenge",  # Should match the one used in authorize URL
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(
        "https://api.twitter.com/2/oauth2/token",
        data=urlencode(payload),  # encode properly
        headers=headers
    )

    return response.json()
