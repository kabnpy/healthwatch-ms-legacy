from enum import Enum

class PolicyStatus(str, Enum):
    ACTIVE = "Active"
    EXPIRED = "Expired"
    CANCELLED = "Cancelled"
    LAPSED = "Lapsed"

class RiskNoteStatus(str, Enum):
    DRAFT = "Draft"
    ISSUED = "Issued"
    REPLACED = "Replaced"
    CANCELLED = "Cancelled"
    ACTIVE = "Issued"  # Alias for backward compatibility

class InvoiceStatus(str, Enum):
    UNPAID = "Unpaid"
    PARTIAL = "Partial"
    PAID = "Paid"
    CANCELLED = "Cancelled"

class ReceiptStatus(str, Enum):
    ACTIVE = "Active"
    VOIDED = "Voided"

class ClaimStatus(str, Enum):
    REPORTED = "Reported"
    ASSESSED = "Assessed"
    PAID = "Paid"
    REJECTED = "Rejected"
    CLOSED = "Closed"

class ClaimEventType(str, Enum):
    NOTIFICATION = "Notification"
    ASSESSMENT = "Assessment"
    CORRESPONDENCE = "Correspondence"
    PAYMENT = "Payment"

class DocumentEntityType(str, Enum):
    CLIENT = "Client"
    POLICY = "Policy"
    CLAIM = "Claim"
    USER = "User"
    RISK_NOTE = "RiskNote"

class DocumentType(str, Enum):
    LOGBOOK = "Logbook"
    ID = "ID"
    VALUATION = "Valuation"
    POLICE_ABSTRACT = "PoliceAbstract"
    RECEIPT = "Receipt"
    OTHER = "Other"
