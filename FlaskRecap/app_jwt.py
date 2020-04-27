from flask import Flask,request,abort
from functools import wraps
import json
from jose import jwt
from urllib.request import urlopen


# Configuration
# UPDATE THIS TO REFLECT YOUR AUTH0 ACCOUNT
AUTH0_DOMAIN = 'prasauth.auth0.com'
#AUTH0_DOMAIN = 'fsnd.auth0.com'
ALGORITHMS = ['RS256']
#API_AUDIENCE = 'image'
API_AUDIENCE = 'https://prasauth.auth0.com/api/v2/'
app= Flask(__name__)

token="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVjekhuLUQxZ1Z3elNBRE5nZ2FKRyJ9.eyJpc3MiOiJodHRwczovL3ByYXNhdXRoLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTlmYzljNzIwN2YzNDBjOTAxM2RkMzYiLCJhdWQiOiJodHRwczovL3ByYXNhdXRoLmF1dGgwLmNvbS9hcGkvdjIvIiwiaWF0IjoxNTg3NjA2ODQ4LCJleHAiOjE1ODc2MTQwNDgsImF6cCI6ImNuNnp2SjQ0ejdBak5ySzIwVWZtRFcwRFowTTAyYjJJIiwic2NvcGUiOiIifQ.oJdtYlTSyfSGremsGKx-MtLHlBAA_y9Y6VIWMW8xhtLU7JF6kGpK9YKxqrCIfhR18hkruveS5RR6L29RXbPV_odhhSeZ6Eb8RDNCq7ioNHsCTaWnpHaGCgxmCD_FrHTxTPGvgRFhvy7VAcyl9yCyZ0cvlFb55VeTzTT9lJE59kwwOQvjw__AgDs5H1wUTxahtrmf_Mx90n7waS6wNK0aEJKcNiXWQmWKfKTH3SrpZO7wPfElJXNBWUusUlvXzlizACBdjswT3wnnaOdudb1vOdUTHy2pwF4zqu6WUAcf7t04nBiBGaCGn2YGgyL6ywQziAkEQ4wyErSET-ZGt7CU-w"

def get_token_auth_header():
    if 'Authorization' not in request.headers:
        abort(401)
    header_parts = request.headers['Authorization'].split()

    if(len(header_parts)) !=2:
        print("error: header is not of two parts: ",header_parts)
        abort(401)
    elif header_parts[0].lower() != 'bearer':
        print("error: bearer is not first part")
        abort(401)
    return header_parts[1]

def requires_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        jwt = get_token_auth_header()  
        #is_valid = verify_decode_jwt(token)
        try:
            payload = verify_decode_jwt(token)
        except:
            abort(401)
        return f(payload,*args,**kwargs)
    return wrapper 

def check_permission(permission,payload):
    if 'permissions' not in payload:
        abort(400)
    if permission not in paylaod['permission']:
        abort(403)
    return True

def requires_auth(permission=''):
    def requires_auth_perission(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            jwt = get_token_auth_header()  
            #is_valid = verify_decode_jwt(token)
            try:
                payload = verify_decode_jwt(token)
            except:
                abort(401)
            check_permission(permission,payload)
            return f(payload,*args,**kwargs)
        return wrapper 
    return requires_auth_permission

@app.route('/headers')
@requires_auth
def headers(jwt):
    #jwt = get_token_auth_header()
    print(jwt)
    return 'not implemeneted'

@app.route('/image')
@requires_auth('get:image')
def images(jwt):
    print(jwt)
    return 'not implemented'

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

def verify_decode_jwt(token):
    # GET THE PUBLIC KEY FROM AUTH0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    
    # GET THE DATA IN THE HEADER
    unverified_header = jwt.get_unverified_header(token)
    
    # CHOOSE OUR KEY
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],               
                'e': key['e']
            }

        # Finally, verify!!!
    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)