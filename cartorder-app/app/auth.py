

from datetime import datetime
import functools
import json
import logging
import secrets
import string
from typing import List
from fastapi import APIRouter, HTTPException, Response, Request, status
from jose import JWSError, jws

public_key = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC+5knMWpDmk1j8sD+85DHG1rGm
3o9tXcgyulXaP+9oi7JqXbrJpARCxDzETWN1X3BBC86NwIFLNJ+cC8h+wY2+O44P
uiCQuIh5TJx/7aESf4umNdF7NFONL3CKuOWoRtzrOyYiQGhWqvLpnlB4pDL5RBvb
2aDj55Y14RzJlel21wIDAQAB
-----END PUBLIC KEY-----'''


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
