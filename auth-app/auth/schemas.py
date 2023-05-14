from enum import Enum
from fastapi import HTTPException
from typing import Dict, List, Optional, Text, Union
from wsgiref.validate import validator
from pydantic import BaseModel, EmailStr, SecretStr

from app.helper import as_form

class Address(BaseModel):
  name: str
  street: str
  pin: int
  village: str

# @as_form
class User(BaseModel):
  name: str
  email: EmailStr
  mobNum: str
  password: SecretStr
  address: Address

# @as_form
class UserEdit(BaseModel):
  name: Optional[str] = None
  email: Optional[EmailStr] = None
  mobNum: Optional[str] = None
  address: Optional[Address] = None

class UserWithId(User):
  id: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
    scopes: List[str] = []

class KeySchema(BaseModel):
  kid: str
  alg: str
  value: str

class KeysSchema(BaseModel):
  keys: List[KeySchema]