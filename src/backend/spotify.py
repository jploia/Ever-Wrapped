from flask import Flask, redirect, request
from urllib.parse import urlencode
from dotenv import load_dotenv
import os, base64, hashlib

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = 'http://EverWrapped/callback'
SCOPE = 'user-read-private user-read-email'
AUTHURL = 'https://accounts.spotify.com/authorize'

app = Flask (__name__)

# Code Challenge generator
def _generate_code_verifier(length = 128) -> str:
    """Generate a random str between 43 and 128 chars as a code verifier for PKCE standard"""
    random_bytes = os.urandom(length)
    code_verifier = base64.urlsafe_b64encode(random_bytes).rstrip(b'=')
    
    return code_verifier.decode('utf-8')

def _hash_code(code: str) -> str:
    """Hash the code verifier using the SHA256 algorithm and return base64"""
    hasher = hashlib.sha256(code.encode('utf-8'))
    hash_val = hasher.hexdigest()
    hash_bytes = hash_val.encode('utf-8')

    return str(base64.b64encode(hash_bytes), 'utf-8')

def _get_code_challenge() -> str:
    """Generate code challenge from hashing a random string"""
    return _hash_code(_generate_code_verifier())

# Request user authorization and retrieve code
@app.route('/')
def request_user_auth():
    """Request user authorization to grant app perms"""
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'scope': SCOPE,
        'code_challenge_method': 'S256',
        'code_challenge': _get_code_challenge(),
        'redirect_uri': REDIRECT_URI,
    }

    auth_url_params = f'{AUTHURL}?{urlencode(params)}'
    return redirect(auth_url_params)

# @app.route('/callback')
# def callback():
#     """Retrieve the callback code from the authorization url"""
#     return request.args.get('code')
    


if __name__ == '__main__':
    app.run(port=8080)
        