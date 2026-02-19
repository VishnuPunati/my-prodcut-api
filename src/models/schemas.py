from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    price: Decimal = Field(..., ge=0)
    stock_quantity: int = Field(..., ge=0)


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = Field(None, min_length=1)
    price: Optional[Decimal] = Field(None, ge=0)
    stock_quantity: Optional[int] = Field(None, ge=0)


class ProductResponse(BaseModel):
    id: str
    name: str
    description: str
    price: Decimal
    stock_quantity: int

    class Config:
        from_attributes = True
