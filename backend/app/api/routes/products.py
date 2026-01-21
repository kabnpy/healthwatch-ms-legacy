import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.crud.insurance.catalog import (
    create_product as crud_create_product,
)
from app.crud.insurance.catalog import (
    get_product_by_name,
)
from app.crud.insurance.catalog import (
    update_product as crud_update_product,
)
from app.models import (
    Message,
    Product,
    ProductCreate,
    ProductPublic,
    ProductsPublic,
    ProductUpdate,
)

router = APIRouter()


@router.get("/", response_model=ProductsPublic)
def read_products(
    session: SessionDep, _current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve products.
    """
    count_statement = select(func.count()).select_from(Product)
    count = session.exec(count_statement).one()
    statement = select(Product).offset(skip).limit(limit)
    products = session.exec(statement).all()
    return ProductsPublic(data=products, count=count)


@router.get("/{id}", response_model=ProductPublic)
def read_product(session: SessionDep, _current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get product by ID.
    """
    product = session.get(Product, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=ProductPublic)
def create_product(
    *, session: SessionDep, _current_user: CurrentUser, product_in: ProductCreate
) -> Any:
    """
    Create new product.
    """
    existing_product = get_product_by_name(session=session, name=product_in.name)
    if existing_product:
        # Check if it's the same insurer to be strict, but for now name is unique-ish
        if existing_product.insurer_id == product_in.insurer_id:
            raise HTTPException(
                status_code=400,
                detail="The product with this name already exists for this insurer.",
            )

    product = crud_create_product(session=session, product_in=product_in)
    return product


@router.put("/{id}", response_model=ProductPublic)
def update_product(
    *,
    session: SessionDep,
    _current_user: CurrentUser,
    id: uuid.UUID,
    product_in: ProductUpdate,
) -> Any:
    """
    Update a product.
    """
    product = session.get(Product, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product = crud_update_product(
        session=session, db_product=product, product_in=product_in
    )
    return product


@router.delete("/{id}", response_model=Message)
def delete_product(
    session: SessionDep, _current_user: CurrentUser, id: uuid.UUID
) -> Any:
    """
    Delete a product.
    """
    product = session.get(Product, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()
    return Message(message="Product deleted successfully")
