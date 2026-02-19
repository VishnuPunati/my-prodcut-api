from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.db.session import get_db
from src.models.schemas import (
    ProductCreate,
    ProductUpdate,
    ProductResponse
)
from src.services import product_service


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    return product_service.create_product(db, product)


@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def get_product(
    product_id: str,
    db: Session = Depends(get_db)
):
    product = product_service.get_product_by_id(db, product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return product


@router.get(
    "/",
    response_model=List[ProductResponse]
)
def get_all_products(
    db: Session = Depends(get_db)
):
    return product_service.get_all_products(db)


@router.put(
    "/{product_id}",
    response_model=ProductResponse
)
def update_product(
    product_id: str,
    product_update: ProductUpdate,
    db: Session = Depends(get_db)
):
    updated_product = product_service.update_product(
        db,
        product_id,
        product_update
    )

    if not updated_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return updated_product


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_product(
    product_id: str,
    db: Session = Depends(get_db)
):
    deleted = product_service.delete_product(db, product_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return
