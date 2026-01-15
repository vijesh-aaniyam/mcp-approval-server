# tools/approval.py
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import HTMLResponse
from models.approval import ApprovalRequest
from uuid import uuid4
from datetime import datetime
from store.dynamo import get_approval, update_approval
from store.dynamo import table

router = APIRouter()
APPROVALS = {}

@router.post("/tools/request_approval")
def request_approval(payload: dict):
    approval_id = str(uuid4())

    approval = ApprovalRequest(
        approval_id=approval_id,
        session_id=payload["session_id"],
        bib=payload["bib"],
        fraud_score=payload["fraud_score"],
        fraud_level=payload["fraud_level"],
        reason=payload["reason"],
        status="pending",
        reviewer=None,
        decision_reason=None,
        created_at=datetime.utcnow()
    )

    APPROVALS[approval_id] = approval
    return {"approval_id": approval_id, "status": "pending"}

@router.post("/tools/submit_approval_decision")
def submit_decision(approval_id, approved, reviewer, reviewer_role, reason):
    approval = get_approval(approval_id)

    if reviewer_role != approval["reviewer_role"] and reviewer_role != "ADMIN":
        raise HTTPException(status_code=403, detail="Insufficient role")

    update_approval(
        approval_id,
        {
            "status": "approved" if approved else "rejected",
            "reviewed_by": reviewer,
            "decision_reason": reason
        }
    )

    return {"status": "ok"}


@router.post("/tools/submit_approval_decision_old")
def submit_decision_old(approval_id: str, approved: bool, reviewer: str, reason: str):
    approval = APPROVALS[approval_id]
    approval.status = "approved" if approved else "rejected"
    approval.reviewer = reviewer
    approval.decision_reason = reason
    return {"status": approval.status}

@router.get("/tools/get_approval_status")
def get_status(approval_id: str):
    approval = APPROVALS[approval_id]
    return {
        "status": approval.status,
        "reviewer": approval.reviewer,
        "decision_reason": approval.decision_reason
    }



@router.get("/ui/approvals", response_class=HTMLResponse)
def approval_ui():
    return open("templates/approvals.html").read()


@router.get("/tools/list_pending")
def list_pending():
    resp = table.scan(
        FilterExpression="status = :s",
        ExpressionAttributeValues={":s": "pending"}
    )
    return resp["Items"]

def required_role(fraud_level: str):
    if fraud_level == "high":
        return "SENIOR_REVIEW"
    if fraud_level == "medium":
        return "REVIEWER"
    return None
