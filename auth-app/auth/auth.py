

from datetime import datetime
import functools
import json
import logging
import secrets
import string
from typing import List
from fastapi import APIRouter, HTTPException, Response, Request, status
from jose import JWSError, jws

from auth.models import User

public_key = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC+5knMWpDmk1j8sD+85DHG1rGm
3o9tXcgyulXaP+9oi7JqXbrJpARCxDzETWN1X3BBC86NwIFLNJ+cC8h+wY2+O44P
uiCQuIh5TJx/7aESf4umNdF7NFONL3CKuOWoRtzrOyYiQGhWqvLpnlB4pDL5RBvb
2aDj55Y14RzJlel21wIDAQAB
-----END PUBLIC KEY-----'''

private_key = '''-----BEGIN PRIVATE KEY-----
MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAL7mScxakOaTWPyw
P7zkMcbWsabej21dyDK6Vdo/72iLsmpdusmkBELEPMRNY3VfcEELzo3AgUs0n5wL
yH7Bjb47jg+6IJC4iHlMnH/toRJ/i6Y10Xs0U40vcIq45ahG3Os7JiJAaFaq8ume
UHikMvlEG9vZoOPnljXhHMmV6XbXAgMBAAECgYAmQGbRN+SJD0VpfLeI1gDTYvm+
AiKjO4N+BrBlRyJlxHg/sABZny/rYP78JrWjMzh/ECqXZNeDhkvlLMdD/uyztKZV
Jq02WzTn6HSipP6lhsk+H/S9jdtRn5bkFGQBNbOBjrEVOKUNF1kAdaKuFklXGDfW
LOHwgNUQHO1S7qtgAQJBAPLtvvMIyRdTgeEpEZm5lIR+1zs9k/Zx9jgolRokqfrw
SNBK0wcoH3zXIAwShA2QQKQevRP2ULZ5pUGJhTAMotcCQQDJK9wuhd0ksPfId6jH
cRK71ZUslVr81LvK5uJLtMwzqM76SKK0LU+oQifzVzm8T1Yb6m/ay8QvhYERKRCL
A0wBAkEA7wlftjcz4B8MkujdZ71DVaiV0rYB7SMwGwxbwtDG7aQYkdS+l7E0Ypwv
7ZEenVYPNS8F8CmUPCmwoa9W/fPBGwJARccc3FY6Wpu3lqVKucMSyGxRDeHQaZow
eTSUkcXofpKzGEVRikWdN7Oav+EleZfbOlua6L19Ey6vkhA4WL+QAQJADnDlEvxh
bm4LU0Y7VT37AqBrLCbLdLVxjtE6xIdKiMWZS0g+ZxFMrmeIVkKG7bov7vwBHkMw
2TOK8ojWqkDOSA==
-----END PRIVATE KEY-----'''

def required_scopes(scopes):
    def decorator(func, *args, **kwargs):

        @functools.wraps(func)
        def wrapper(*args,request: Request, response: Response, **kwargs):
            logging.info(f'Checking cookies for jwt token.')
            signed = request.cookies.get("jwt")
            if signed == None:
                logging.error(f'cookie with key `jwt` didn\'t found.')
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not authenticated")
            
            try: 
                data = json.loads(jws.verify(signed, public_key, algorithms=['RS256']).decode('utf-8'))
            except JWSError as e:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="jwt verification failed")
            
            for scope in scopes:
                if not scope in data['scope']:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized")
            # add uid of user in header so that route function can access it
            request.headers.__dict__['_list'].append(('uid'.encode(), data.get('uid').encode()))
            return func(*args, request = request, response = response, **kwargs)
        return wrapper
    return decorator

def generate_token(user: User, scopes: List[str]):
    payload = {
        'exp': int(datetime.now().timestamp()) + 600,
        'nbf': int(datetime.now().timestamp()),
        'iss': 'retail.avabodha.in',
        'uid': str(user.pk),
        'umail': user.email,
        'iat': int(datetime.now().timestamp()),
        'role': user.role.name,
        'scope': scopes,
    }
    return jws.sign(payload, private_key, algorithm='RS256', headers={'kid': 'key-1'})
    
def public_keys():
    return {'keys': [{ 'kid': 'key-1','value': public_key, 'alg': 'RS256' }]}

def generate_session_token():
    characters = string.ascii_letters + string.digits + string.punctuation
    session = ''.join((secrets.choice(characters) for i in range(64)))
    return session