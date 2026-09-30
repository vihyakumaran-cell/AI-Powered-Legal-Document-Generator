// LegalEase - client-side form workflow (academic prototype)
const state = {
  documentType: "",
  inputs: {},
  generating: false
};

const requiredFields = {
  nda: ["partyA", "partyB", "purpose"],
  lease: ["landlord", "tenant", "propertyAddress", "startDate"],
  affidavit: ["deponentName", "statementPurpose"],
  authorization: ["authorizer", "authorizedPerson", "purpose"]
};

function validateForm() {
  const fields = requiredFields[state.documentType] || [];
  const missing = fields.filter((name) => !state.inputs[name]?.trim());
  return { valid: missing.length === 0, missing };
}

async function generateDraft() {
  const validation = validateForm();
  if (!validation.valid) {
    showError(`Please complete: ${validation.missing.join(", ")}`);
    return;
  }

  state.generating = true;
  showLoading(true);

  try {
    // Call your own backend. Never expose an AI API key in browser code.
    const response = await fetch("/api/documents/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        documentType: state.documentType,
        inputs: state.inputs
      })
    });

    if (!response.ok) throw new Error("Generation service unavailable");
    const result = await response.json();

    renderDraft(result.draft);
    showDisclaimer();
  } catch (error) {
    showError("Draft generation failed. Please review the inputs and try again.");
  } finally {
    state.generating = false;
    showLoading(false);
  }
}
