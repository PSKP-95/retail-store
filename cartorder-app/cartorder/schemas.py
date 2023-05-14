from enum import Enum
from fastapi import HTTPException
from typing import Dict, List, Optional, Text, Union
from wsgiref.validate import validator
from pydantic import BaseModel

from app.helper import as_form

class CartItem(BaseModel):
  iid: str
  qty: float

class Cart(BaseModel):
  items: List[CartItem] = []

class Address(BaseModel):
  name: str
  street: str
  pin: int
  village: str

class OrderItem(BaseModel):
  iid: str
  qty: float
  rate: float
  price: float

class Order(BaseModel):
  items: List[OrderItem] = []
  address: Address