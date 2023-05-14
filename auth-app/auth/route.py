from datetime import datetime
import functools
import logging
import socket
from time import time
from typing import List
from app.database import client as redisClient
from app.hashing import Hash
from app.helper import get_sha256_hash, mongo_to_dict, verify_sha256_hash
from auth.auth import generate_session_token, generate_token, public_keys, required_scopes
from auth.service import find_user_with_id, find_user_with_userid, signup, update_user_profile
from .schemas import  KeysSchema, User, UserEdit, UserWithId
from fastapi import APIRouter, Depends, Form, HTTPException, Header, Response, Request, Security, status
from passlib.context import CryptContext
import json

from jose import jws

router = APIRouter()

priv = '''-----BEGIN PRIVATE KEY-----
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

@router.get("/", response_model=UserWithId)
@required_scopes(["iam:getProfile"])
def get_profile(response: Response, request: Request):
    uid = request.headers.get('uid')
    etag = request.headers.get("If-None-Match")

    uidHash = redisClient.get('uidHash-' + uid)
    
    if uidHash:
        uidHash = uidHash.decode('utf-8')
    
    if etag and uidHash and etag == uidHash:
        logging.info(f'Cache hit and etag has same value as cache hash')
        response.status_code = status.HTTP_304_NOT_MODIFIED
        return response

    if uidHash:
        logging.info(f'Cache hit but etag not found')
        user = json.loads(redisClient.get('uid-' + uid).decode('utf-8'))
        if user:
            response.headers["ETag"] = uidHash
            return user
    
    logging.info(f'Cache missed. fetching results from DB.')
    user = find_user_with_id(uid, dictFormat=True)
    userBytes = json.dumps(user).encode('utf-8')
    uidHash = Hash.bcrypt(userBytes)

    logging.info(f'adding profile of user with id {uid} in cache.')
    redisClient.set('uidHash-' + uid, uidHash)
    redisClient.set('uid-' + uid, userBytes)
    response.headers["ETag"] = uidHash
    return user

@router.put("/", response_model=UserWithId)
@required_scopes(["iam:editProfile"])
def edit_profile(response: Response, request: Request, user: UserEdit):
    uid = request.headers.get('uid')
    
    logging.info(f'updating profile for user with id {uid}.')
    newUserInfo = update_user_profile(uid, user)

    logging.info(f'invalidating profile cache for user with id {uid}')
    redisClient.delete('uidHash-' + uid)
    redisClient.delete('uid-' + uid)    
    return newUserInfo

@router.post("/login")
def do_login(response: Response, userid: str = Form(...), password: str = Form(...)):
    if userid == None or password == None:
        pass

    user = find_user_with_userid(userid, password)

    if user != None:
        scopes = []
        for scope in user.role.scopes:
            scopes.append(scope.name)
        token = generate_token(user, scopes)
        response.set_cookie('jwt', token, max_age=600, httponly=True)
        refresh_token = generate_session_token()
        redisClient.set(refresh_token, str(user.id))
        response.set_cookie('refresh_token', refresh_token, httponly=True)
        response.status_code = status.HTTP_204_NO_CONTENT
    return response

@router.post("/signup", response_model=UserEdit)
def do_signup(request: User):
    return signup(request)

@router.get("/token_keys", response_model=KeysSchema)
def get_token_keys(response: Response):
    return public_keys()

@router.get("/token")
def get_token(response: Response, request: Request):
    refresh_token = request.cookies.get('refresh_token')
    if refresh_token == None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'no refresh_token cookie found.')
    uid = redisClient.get(refresh_token).decode('utf-8')

    if uid == None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'refresh_token cookie is not valid.')
    user = find_user_with_id(uid)
    if user != None:
        scopes = []
        for scope in user.role.scopes:
            scopes.append(scope.name)
        token = generate_token(user, scopes)
        response.set_cookie('jwt', token, max_age=600, httponly=True)
        response.status_code = status.HTTP_204_NO_CONTENT
    return response

@router.get("/logout")
def logout(response: Response, request: Request):
    refresh_token = request.cookies.get('refresh_token')
    jwt = request.cookies.get('jwt')

    if refresh_token != None:
        redisClient.delete(refresh_token)
        response.delete_cookie('refresh_token')
    
    if jwt != None:
        response.delete_cookie('jwt')
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@router.get("/metrics/redis")
def redis_metrics(response: Response, request: Request):
    return redisClient.info()

@router.get("/metrics/health")
def health(response: Response, request: Request):
    return {'datetime': datetime.utcnow(), 'hostname': socket.gethostname()}