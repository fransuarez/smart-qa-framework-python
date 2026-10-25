"""
Pydantic data models for the Fake Store API.
"""

from pydantic import BaseModel
from typing import List, Optional

class AuthResponse(BaseModel):
    token: str

class User(BaseModel):
    id: int
    username: str
    password: str
    # TODO: add other fields as needed

class Product(BaseModel):
    id: Optional[int] = None
    title: str
    price: float
    description: str
    category: str
    image: str
    rating: Optional[dict] = None
    # TODO: adjust schema to match the real API