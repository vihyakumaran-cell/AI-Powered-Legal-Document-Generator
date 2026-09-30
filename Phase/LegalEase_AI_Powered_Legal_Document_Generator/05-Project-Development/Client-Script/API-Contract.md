# LegalEase API Contract (Prototype)

POST /api/documents/generate

Request:
{
  "documentType": "nda",
  "inputs": {
    "partyA": "Example Company",
    "partyB": "Example Person",
    "purpose": "Evaluation of a business proposal",
    "confidentialityPeriod": "12 months"
  }
}

Response:
{
  "draft": "...generated draft...",
  "status": "generated",
  "reviewRequired": true
}

Security:
- Authenticate the user where applicable.
- Validate and sanitize input.
- Keep provider API keys server-side.
- Avoid logging sensitive document contents unnecessarily.
- Apply rate limits and access controls.
