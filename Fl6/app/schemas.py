from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Схема для создания пользователя
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

# Схема для ответа по пользователю
class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True

# Схема для создания продукта
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

# Схема для ответа по продукту
class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float

    class Config:
        orm_mode = True

# Схема для создания заказа
class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    status: str

# Схема для ответа по заказу
class OrderResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    order_date: datetime
    status: str

    class Config:
        orm_mode = True
