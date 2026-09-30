// LegalEase UI Policy logic
// Pseudocode adaptable to React/Angular/vanilla JS or a form platform.

function applyDocumentTypePolicy(documentType) {
  hideAllConditionalFields();

  const rules = {
    nda: ["partyA", "partyB", "purpose", "confidentialityPeriod"],
    lease: ["landlord", "tenant", "propertyAddress", "startDate", "rent"],
    affidavit: ["deponentName", "statementPurpose", "declarationDate"],
    authorization: ["authorizer", "authorizedPerson", "purpose", "validUntil"]
  };

  (rules[documentType] || []).forEach(showField);

  // Always display a human-review disclaimer.
  showField("legalReviewNotice");
}

function validateConditionalFields(documentType, values) {
  const required = {
    nda: ["partyA", "partyB", "purpose"],
    lease: ["landlord", "tenant", "propertyAddress", "startDate"],
    affidavit: ["deponentName", "statementPurpose"],
    authorization: ["authorizer", "authorizedPerson", "purpose"]
  };

  return (required[documentType] || []).every(
    field => typeof values[field] === "string" && values[field].trim() !== ""
  );
}
