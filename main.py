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
    import base64
    import requests
    from urllib.parse import urlencode

    code = request.query_params.get("code")
    if not code:
        return {"error": "Missing code from Twitter"}

    # Encode client_id and client_secret to base64 for the Authorization header
    basic_auth = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {basic_auth}",  # Correct way to send Twitter credentials
    }

    payload = {
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": TWITTER_REDIRECT_URI,
        "code_verifier": "challenge",  # must match what was used during auth
    }

    response = requests.post(
        "https://api.twitter.com/2/oauth2/token",
        data=urlencode(payload),
        headers=headers
    )

    return response.json()
