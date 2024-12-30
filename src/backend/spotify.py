from flask import Flask, redirect, app, request, session
from urllib.parse import urlencode
from dotenv import load_dotenv
import os, base64, hashlib, requests, json, secrets, string

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
REDIRECT_URI = 'http://localhost:8080/callback'
TOKEN_URL = "https://accounts.spotify.com/api/token"
SCOPE = 'user-read-private user-read-email'
AUTHURL = 'https://accounts.spotify.com/authorize'

app = Flask (__name__)
app.secret_key = os.getenv('CLIENT_SECRET')

# Code Challenge generator
def _generate_code_verifier(length = 128) -> str:
    """Generate a random str between 43 and 128 chars as a code verifier for PKCE standard"""
    allowed_chars = string.ascii_letters + string.digits + '-._~'
    return ''.join(secrets.choice(allowed_chars) for _ in range(length))

CODE_VERIFIER = _generate_code_verifier()

def _get_code_challenge(verifier: str) -> str:
    """Generate code challenge from hashing a random string"""
    sha256 = hashlib.sha256(verifier.encode('utf-8')).digest()
    hashed = base64.urlsafe_b64encode(sha256).decode('utf-8').rstrip('=')

    return hashed

CODE_CHALLENGE = _get_code_challenge(CODE_VERIFIER)

# Request user authorization and retrieve code
@app.route('/')
def request_user_auth():
    """Request user authorization to grant app perms"""
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'scope': SCOPE,
        'code_challenge_method': 'S256',
        'code_challenge': CODE_CHALLENGE,
        'redirect_uri': REDIRECT_URI,
    }

    auth_url_params = f'{AUTHURL}?{urlencode(params)}'
    return redirect(auth_url_params)

@app.route('/callback')
def set_token() -> str:
    """Set token based on user authorization"""
    # retrieve callback code
    call_code = request.args.get('code')
    _get_token(call_code)
    return 'Successfully authenticated!'
    
def _get_token(call_code: str):
    """Request token by exchanging authorization code"""
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': app.secret_key,
        'code': call_code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI,
        'code_verifier': CODE_VERIFIER,
    }

    header = {
        'Content_Type': 'application/x-www-form-urlencoded',
    }

    body = requests.post(TOKEN_URL, data=payload, headers=header)
    # nested dictionary
    response = json.loads(body.text)
    print(f'code verifier: {CODE_VERIFIER}')
    print(f'code challenge: {CODE_CHALLENGE}')
    print(response)

    # session['access_token'] = response['access_token']

    # we want to render something here in html.
    print('Success!')

if __name__ == '__main__':
    app.run(port=8080)
        