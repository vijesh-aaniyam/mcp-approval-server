# models/approval.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ApprovalRequest(BaseModel):
    approval_id: str
    session_id: str
    bib: int
    fraud_score: float
    fraud_level: str
    reason: str
    status: str  # pending | approved | rejected
    reviewer: Optional[str]
    decision_reason: Optional[str]
    created_at: datetime
