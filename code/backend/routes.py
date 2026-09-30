from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ai_core.gemini_generator import generate_legal_document


router = APIRouter()


# ---------------------------------------------------------
# Request model
# ---------------------------------------------------------

class DocumentRequest(BaseModel):

    document_type: str = Field(
        ...,
        min_length=1
    )

    parties: str = Field(
        ...,
        min_length=1
    )

    terms: str = Field(
        ...,
        min_length=1
    )

    effective_date: str = Field(
        ...,
        min_length=1
    )

    jurisdiction: Optional[str] = "India"

    additional_instructions: Optional[str] = ""


# ---------------------------------------------------------
# Generate document
# ---------------------------------------------------------

@router.post("/generate")
def generate_document(
    request: DocumentRequest
):

    try:

        document = generate_legal_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            effective_date=request.effective_date,
            jurisdiction=request.jurisdiction or "India",
            additional_instructions=(
                request.additional_instructions or ""
            ),
        )

        return {
            "success": True,
            "document": document,
            "document_type": request.document_type,
        }

    except Exception as exc:

        print(
            "[LegalEase] Generation error:",
            str(exc)
        )

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )