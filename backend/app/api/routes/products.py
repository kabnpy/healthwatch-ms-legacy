import uuid
from typing import Any

from fastapi import APIRouter, HTTPException

from app.api.deps import CurrentUser, SessionDep, StaffUser
from app.crud import (
    count_products,
    get_product_by_name,
    get_products,
)
from app.crud import (
    create_product as crud_create_product,
)
from app.crud import (
    delete_product as crud_delete_product,
)
from app.crud import (
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
    session: SessionDep,
    _current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
    insurer_id: uuid.UUID | None = None,
) -> Any:
    """
    Retrieve products.
    """
    count = count_products(session=session, insurer_id=insurer_id)
    products = get_products(
        session=session, skip=skip, limit=limit, insurer_id=insurer_id
    )
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
    *, session: SessionDep, _current_user: StaffUser, product_in: ProductCreate
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
    _current_user: StaffUser,
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
    session: SessionDep, _current_user: StaffUser, id: uuid.UUID
) -> Any:
    """
    Delete a product.
    """
    product = session.get(Product, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    crud_delete_product(session=session, db_product=product)
    return Message(message="Product deleted successfully")
