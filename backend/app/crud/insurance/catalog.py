import uuid

from sqlmodel import Session, select

from app.models.insurance.catalog import (
    Insurer,
    InsurerCreate,
    InsurerUpdate,
    Product,
    ProductCreate,
    ProductUpdate,
)


def create_insurer(*, session: Session, insurer_in: InsurerCreate) -> Insurer:
    db_obj = Insurer.model_validate(insurer_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_insurer_by_name(session: Session, *, name: str) -> Insurer | None:
    statement = select(Insurer).where(Insurer.name == name)
    return session.exec(statement).first()


def create_product(*, session: Session, product_in: ProductCreate) -> Product:
    db_obj = Product.model_validate(product_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_product_by_name(session: Session, *, name: str) -> Product | None:
    statement = select(Product).where(Product.name == name)
    return session.exec(statement).first()


def update_insurer(
    *, session: Session, db_insurer: Insurer, insurer_in: InsurerUpdate
) -> Insurer:
    insurer_data = insurer_in.model_dump(exclude_unset=True)
    db_insurer.sqlmodel_update(insurer_data)
    session.add(db_insurer)
    session.commit()
    session.refresh(db_insurer)
    return db_insurer


def update_product(
    *, session: Session, db_product: Product, product_in: ProductUpdate
) -> Product:
    product_data = product_in.model_dump(exclude_unset=True)
    db_product.sqlmodel_update(product_data)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


def get_insurers(session: Session, *, skip: int = 0, limit: int = 100) -> list[Insurer]:
    statement = select(Insurer).offset(skip).limit(limit)
    return list(session.exec(statement).all())


def count_insurers(session: Session) -> int:
    from sqlmodel import func

    statement = select(func.count()).select_from(Insurer)
    return session.exec(statement).one()


def delete_insurer(session: Session, *, db_insurer: Insurer) -> None:
    session.delete(db_insurer)
    session.commit()


def get_products(
    session: Session,
    *,
    skip: int = 0,
    limit: int = 100,
    insurer_id: uuid.UUID | None = None,
) -> list[Product]:
    statement = select(Product)
    if insurer_id:
        statement = statement.where(Product.insurer_id == insurer_id)
    statement = statement.offset(skip).limit(limit)
    return list(session.exec(statement).all())


def count_products(session: Session, *, insurer_id: uuid.UUID | None = None) -> int:
    from sqlmodel import func

    statement = select(Product)
    if insurer_id:
        statement = statement.where(Product.insurer_id == insurer_id)
    count_statement = select(func.count()).select_from(statement.subquery())
    return session.exec(count_statement).one()


def delete_product(session: Session, *, db_product: Product) -> None:
    session.delete(db_product)
    session.commit()
