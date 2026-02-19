from sqlalchemy.orm import Session
from src.models.product import Product
from src.models.schemas import ProductCreate, ProductUpdate
from src.services.cache_service import cache_service


def create_product(db: Session, product_data: ProductCreate) -> Product:
    product = Product(**product_data.model_dump())
    print(product)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_product_by_id(db: Session, product_id: str) -> Product | None:
    cache_key = f"product:{product_id}"

    # Check cache
    cached_product = cache_service.get(cache_key)
    if cached_product:
        return Product(**cached_product)

    # Fetch from DB
    product = db.query(Product).filter(Product.id == product_id).first()

    if product:
        cache_service.set(
            cache_key,
            {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": str(product.price),
                "stock_quantity": product.stock_quantity,
            }
        )

    return product


def get_all_products(db: Session) -> list[Product]:
    return db.query(Product).all()


def update_product(
    db: Session,
    product_id: str,
    update_data: ProductUpdate
) -> Product | None:

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        return None

    update_dict = update_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(product, key, value)

    db.commit()
    cache_key = f"product:{product_id}"
    cache_service.delete(cache_key)

    db.refresh(product)

    return product


def delete_product(db: Session, product_id: str) -> bool:
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        return False

    db.delete(product)
    cache_key = f"product:{product_id}"
    cache_service.delete(cache_key)

    db.commit()

    return True
