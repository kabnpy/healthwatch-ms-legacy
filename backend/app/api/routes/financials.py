import uuid
from typing import Any

from fastapi import APIRouter, HTTPException

from app.api.deps import CurrentUser, SessionDep, StaffUser
from app.crud.insurance import (
    create_invoice,
    create_invoice_bulk,
    create_receipt,
    create_receipt_allocation,
    get_invoice,
    get_invoices,
    get_receipt,
    get_receipts,
    void_receipt,
)
from app.models import (
    InvoiceBulkCreate,
    InvoiceCreate,
    InvoicePublic,
    InvoicesPublic,
    Message,
    ReceiptAllocationCreate,
    ReceiptCreate,
    ReceiptPublic,
    ReceiptsPublic,
)

router = APIRouter()

# ==========================================
# Invoice Routes
# ==========================================


@router.get("/invoices/", response_model=InvoicesPublic)
def read_invoices(
    session: SessionDep,
    _current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
    client_id: str | None = None,
) -> Any:
    """
    Retrieve invoices.
    """
    client_uuid: uuid.UUID | None = None
    if client_id:
        try:
            client_uuid = uuid.UUID(client_id)
        except ValueError:
            pass

    invoices = get_invoices(
        session=session, skip=skip, limit=limit, client_id=client_uuid
    )
    return InvoicesPublic(data=invoices, count=len(invoices))


@router.get("/invoices/{id}", response_model=InvoicePublic)
def read_invoice(session: SessionDep, _current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get invoice by ID.
    """
    invoice = get_invoice(session=session, id=id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@router.post("/invoices/", response_model=InvoicePublic)
def create_new_invoice(
    *, session: SessionDep, _current_user: StaffUser, invoice_in: InvoiceCreate
) -> Any:
    """
    Create new invoice.
    """
    return create_invoice(session=session, invoice_in=invoice_in)


@router.post("/bulk-invoices/", response_model=InvoicePublic)
def create_bulk_invoice(
    *, session: SessionDep, _current_user: StaffUser, bulk_in: InvoiceBulkCreate
) -> Any:
    """
    Create an invoice from multiple Risk Notes.
    """
    return create_invoice_bulk(session=session, bulk_in=bulk_in)


# ==========================================
# Receipt Routes
# ==========================================


@router.get("/receipts/", response_model=ReceiptsPublic)
def read_receipts(
    session: SessionDep,
    _current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
    client_id: str | None = None,
) -> Any:
    """
    Retrieve receipts.
    """
    client_uuid: uuid.UUID | None = None
    if client_id:
        try:
            client_uuid = uuid.UUID(client_id)
        except ValueError:
            pass

    receipts = get_receipts(
        session=session, skip=skip, limit=limit, client_id=client_uuid
    )
    return ReceiptsPublic(data=receipts, count=len(receipts))


@router.get("/receipts/{id}", response_model=ReceiptPublic)
def read_receipt_by_id(
    session: SessionDep, _current_user: CurrentUser, id: uuid.UUID
) -> Any:
    """
    Get receipt by ID.
    """
    receipt = get_receipt(session=session, id=id)
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return receipt


@router.post("/receipts/", response_model=ReceiptPublic)
def create_new_receipt(
    *, session: SessionDep, _current_user: StaffUser, receipt_in: ReceiptCreate
) -> Any:
    """
    Create new receipt.
    """
    return create_receipt(session=session, receipt_in=receipt_in)


@router.post("/receipts/{id}/allocations", response_model=Message)
def allocate_receipt(
    *,
    session: SessionDep,
    _current_user: StaffUser,
    id: uuid.UUID,
    allocation_in: ReceiptAllocationCreate,
) -> Any:
    """
    Allocate a receipt to an invoice.
    """
    receipt = get_receipt(session=session, id=id)
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")

    create_receipt_allocation(session=session, allocation_in=allocation_in)
    return Message(message="Allocation successful")


@router.delete("/receipts/{id}", response_model=ReceiptPublic)
def delete_receipt(
    *, session: SessionDep, _current_user: StaffUser, id: uuid.UUID
) -> Any:
    """
    Void a receipt.
    """
    receipt = get_receipt(session=session, id=id)
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    if receipt.status == "Voided":
        raise HTTPException(status_code=400, detail="Receipt is already voided")

    return void_receipt(session=session, db_receipt=receipt)

