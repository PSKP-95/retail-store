from http import HTTPStatus
import logging
from typing import List
from app.auth import required_scopes
from app.hashing import Hash
from app.helper import get_sha256_hash, verify_sha256_hash
from pricing.service import find_item_with_id, get_all_items, add_item, update_item
from .schemas import  ItemWithId, Item
from app.database import client as redisClient
from fastapi import APIRouter, HTTPException, Header, Response, Request, status
from passlib.context import CryptContext
import json

router = APIRouter()

@router.get("/{id}", response_model=ItemWithId)
def get_item(response: Response, id: str, request: Request):
    iidHash = redisClient.get('iidHash-' + id)

    if iidHash:
        iidHash = redisClient.get('iidHash-' + id).decode('utf-8')
    etag = request.headers.get("If-None-Match")
    
    if etag and iidHash and iidHash == etag:
        return Response(status_code=HTTPStatus.NOT_MODIFIED)
    
    if iidHash:
        logging.info(f'cache hit, reading from cache')
        item = json.loads(redisClient.get('iid-'+id).decode('utf-8'))
        print(item)
        if item:
            response.headers['Etag'] = iidHash
            return item
    logging.info(f'Cache missed. fetching results from database.')
    item = find_item_with_id(id)

    byteData = json.dumps(item).encode('utf-8')
    newEtag = Hash.bcrypt(byteData)

    redisClient.set('iid-'+id, byteData)
    redisClient.set('iidHash-'+id, newEtag)

    response.headers["ETag"] = newEtag
    
    return item

@router.get("/", response_model=List[ItemWithId])
def get_items():
    return get_all_items()

@router.post("/", response_model=ItemWithId)
@required_scopes(["product:create"])
def create_item(request: Request, response: Response, item: Item):
    return add_item(item)

@router.put("/{id}", response_model=ItemWithId)
@required_scopes(["product:edit"])
def edit_item(request: Request, response: Response, id: str, item: Item):
    logging.info(f'invalidating profile cache for user with id {id}')
    redisClient.delete('iidHash-' + id)
    redisClient.delete('iid-' + id)
    return update_item(id, item)

@router.get("/metrics/redis")
def redis_metrics(response: Response, request: Request):
    return redisClient.info()

@router.get("/metrics/health")
def health(response: Response, request: Request):
    return {"OK"}
