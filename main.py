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
    code = request.query_params.get("code")
    if not code:
        return {"error": "Missing code from Twitter"}

    import requests
    response = requests.post(
        "https://api.twitter.com/2/oauth2/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "code": code,
            "grant_type": "authorization_code",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,  # Include it here instead
            "redirect_uri": TWITTER_REDIRECT_URI,
            "code_verifier": "challenge",
        }
    )
    return response.json()
