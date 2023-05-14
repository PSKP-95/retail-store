from datetime import datetime
import functools
import logging
import socket
from time import time
from typing import List
from app.database import client as redisClient
from app.hashing import Hash
from app.helper import get_sha256_hash, mongo_to_dict, verify_sha256_hash
from app.auth import required_scopes
from cartorder.schemas import CartItem, Cart
from cartorder.service import change_item_in_cart, get_cart
from fastapi import APIRouter, Depends, Form, HTTPException, Header, Response, Request, Security, status
from passlib.context import CryptContext
import json

from jose import jws

router = APIRouter()


###### CART ######

@router.get("/cart", response_model=Cart)
@required_scopes(["cart:getItems"])
def get_my_cart(response: Response, request: Request):
    uid = request.headers.get('uid')

    return get_cart(uid)

@router.put("/cart")
@required_scopes(["cart:addItem", "cart:removeItem", "cart:changeQuantity"])
def edit_my_cart(response: Response, request: Request, iid: str, qty: float):
    uid = request.headers.get('uid')
    return change_item_in_cart(uid, iid, qty)

###### ORDER ######

###### HEALTH & METRICS ########

@router.get("/metrics/redis")
def redis_metrics(response: Response, request: Request):
    return redisClient.info()

@router.get("/metrics/health")
def health(response: Response, request: Request):
    return {'datetime': datetime.utcnow(), 'hostname': socket.gethostname()}