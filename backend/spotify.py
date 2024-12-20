from dotenv import load_dotenv
from requests import post
import os, base64, json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token() -> str:
    """Get the generated token using the client id and secret"""
    auth_string = f'{client_id}:{client_secret}'
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f'Basic {auth_base64}',
        "Content-Type": 'application/x-www-form-urlencoded'
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers = headers, data = data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    
    return token

def generate_random_str(length = 128) -> str:
    """Generate a random str between 43 and 128 chars as a code verifier for PKCE standard"""
    random_bytes = os.urandom(length)
    code_verifier = base64.urlsafe_b64encode(random_bytes).rstrip(b'=')
    
    return code_verifier.decode('utf-8')