from dotenv import load_dotenv
from requests import post
from urllib.parse import urlencode
import os, base64, json, hashlib, webbrowser

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = 'http://EverWrapped/callback'
SCOPE = 'user-read-private user-read-email'
AUTHURL = 'https://accounts.spotify.com/authorize'

# def get_token() -> str:
#     """Get the generated token using the client id and secret"""
#     auth_string = f'{client_id}:{client_secret}'
#     auth_bytes = auth_string.encode('utf-8')
#     auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

#     url = "https://accounts.spotify.com/api/token"
#     headers = {
#         "Authorization": f'Basic {auth_base64}',
#         "Content-Type": 'application/x-www-form-urlencoded'
#     }
#     data = {"grant_type": 'client_credentials'}
#     result = post(url, headers = headers, data = data)
#     json_result = json.loads(result.content)
#     token = json_result['access_token']
    
#     return token


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

def get_code_challenge() -> str:
    """Generate code challenge from hashing a random string"""
    return _hash_code(_generate_code_verifier())

# Request user authorization and retrieve code
def request_user_auth() -> str:
    """Request user authorization to grant app perms"""
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'scope': SCOPE,
        'code_challenge_method': 'S256',
        'code_challenge': get_code_challenge(),
        'redirect_uri': REDIRECT_URI,
    }

    auth_url_params = f'{AUTHURL}?{urlencode(params)}'
    
    return auth_url_params
    # print(auth_url_params)
    # print(f'Opening the following url in your browser: {auth_url_params}')
    # webbrowser.open(auth_url_params)
    # auth_code = input('Paste authorization code here: ')
    # print(f'Code received: {auth_code}')