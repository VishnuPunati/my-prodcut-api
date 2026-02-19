import uuid
from sqlalchemy import Column, String, Integer, Numeric
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime
from src.db.session import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=False)

    price = Column(Numeric(10, 2), nullable=False)
    stock_quantity = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
