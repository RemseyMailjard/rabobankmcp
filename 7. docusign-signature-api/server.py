"""
Dummy DocuSign Signature API
=============================
A simple REST API simulating DocuSign's electronic signature system.
Students will build an MCP server that wraps these endpoints.

Run with:
    uv run uvicorn server:app --reload --port 8001

API docs available at: http://localhost:8001/docs
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid

app = FastAPI(
    title="DocuSign Signature API",
    description="A dummy DocuSign Signature API for building an MCP server against.",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------------------------

class Document(BaseModel):
    documentId: str
    name: str
    documentBase64: str  # Base64 encoded document

class Signer(BaseModel):
    email: str
    name: str
    recipientId: str
    routingOrder: str = "1"
    status: str = "created"  # created, sent, delivered, signed, declined, completed
    tabs: Optional[dict] = None  # e.g., {"signTabs": [{"documentId": "1", "pageNumber": "1", "xPosition": "100", "yPosition": "100"}]}

class Recipients(BaseModel):
    signers: List[Signer] = []

class Envelope(BaseModel):
    envelopeId: str
    emailSubject: str
    status: str = "created"  # created, sent, voided, completed, declined, delivered
    recipients: Recipients = Recipients()
    documents: List[Document] = []
    statusDateTime: datetime = datetime.now()

# ---------------------------------------------------------------------------
# In-memory data
# ---------------------------------------------------------------------------

envelopes = {}

# ---------------------------------------------------------------------------
# Request Models
# ---------------------------------------------------------------------------

class CreateEnvelopeRequest(BaseModel):
    emailSubject: str
    status: str = "created"
    recipients: Recipients = Recipients()
    documents: List[Document] = []

# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.post("/envelopes", response_model=dict)
def create_envelope(request: CreateEnvelopeRequest):
    """Create a new envelope."""
    envelope_id = str(uuid.uuid4())
    envelope = Envelope(
        envelopeId=envelope_id,
        emailSubject=request.emailSubject,
        status=request.status,
        recipients=request.recipients,
        documents=request.documents
    )
    envelopes[envelope_id] = envelope
    return {"envelopeId": envelope_id, "uri": f"/envelopes/{envelope_id}", "statusDateTime": envelope.statusDateTime.isoformat()}

@app.post("/envelopes/{envelope_id}/documents")
def add_document(envelope_id: str, document: Document):
    """Add a document to an envelope."""
    if envelope_id not in envelopes:
        raise HTTPException(status_code=404, detail="Envelope not found")
    envelope = envelopes[envelope_id]
    if envelope.status != "created":
        raise HTTPException(status_code=400, detail="Cannot add documents to non-created envelope")
    envelope.documents.append(document)
    return {"message": "Document added"}

@app.post("/envelopes/{envelope_id}/recipients")
def add_recipient(envelope_id: str, signer: Signer):
    """Add a signer to an envelope."""
    if envelope_id not in envelopes:
        raise HTTPException(status_code=404, detail="Envelope not found")
    envelope = envelopes[envelope_id]
    if envelope.status != "created":
        raise HTTPException(status_code=400, detail="Cannot add recipients to non-created envelope")
    envelope.recipients.signers.append(signer)
    return {"message": "Recipient added"}

@app.put("/envelopes/{envelope_id}")
def update_envelope_status(envelope_id: str, status: str = Query(...)):
    """Update envelope status (e.g., send)."""
    if envelope_id not in envelopes:
        raise HTTPException(status_code=404, detail="Envelope not found")
    envelope = envelopes[envelope_id]
    if status == "sent" and envelope.status == "created":
        if not envelope.documents:
            raise HTTPException(status_code=400, detail="No documents in envelope")
        if not envelope.recipients.signers:
            raise HTTPException(status_code=400, detail="No recipients in envelope")
        envelope.status = "sent"
        for signer in envelope.recipients.signers:
            signer.status = "sent"
    elif status == "voided":
        envelope.status = "voided"
    else:
        raise HTTPException(status_code=400, detail="Invalid status update")
    return {"message": f"Envelope status updated to {status}"}

@app.get("/envelopes/{envelope_id}", response_model=Envelope)
def get_envelope(envelope_id: str):
    """Get envelope details."""
    if envelope_id not in envelopes:
        raise HTTPException(status_code=404, detail="Envelope not found")
    return envelopes[envelope_id]

@app.post("/envelopes/{envelope_id}/recipients/{recipient_id}/sign")
def sign_envelope(envelope_id: str, recipient_id: str):
    """Simulate signing by a recipient."""
    if envelope_id not in envelopes:
        raise HTTPException(status_code=404, detail="Envelope not found")
    envelope = envelopes[envelope_id]
    if envelope.status != "sent":
        raise HTTPException(status_code=400, detail="Envelope not sent")
    for signer in envelope.recipients.signers:
        if signer.recipientId == recipient_id:
            if signer.status == "signed":
                raise HTTPException(status_code=400, detail="Already signed")
            signer.status = "signed"
            # Check if all signed
            if all(s.status == "signed" for s in envelope.recipients.signers):
                envelope.status = "completed"
            return {"message": "Signed"}
    raise HTTPException(status_code=404, detail="Recipient not found")

@app.get("/envelopes/{envelope_id}/documents/{document_id}")
def get_document(envelope_id: str, document_id: str):
    """Get a document."""
    if envelope_id not in envelopes:
        raise HTTPException(status_code=404, detail="Envelope not found")
    envelope = envelopes[envelope_id]
    for doc in envelope.documents:
        if doc.documentId == document_id:
            if envelope.status == "completed":
                # Simulate signed document
                content = f"SIGNED: {doc.documentBase64}"
            else:
                content = doc.documentBase64
            return {"documentId": doc.documentId, "name": doc.name, "documentBase64": content}
    raise HTTPException(status_code=404, detail="Document not found")