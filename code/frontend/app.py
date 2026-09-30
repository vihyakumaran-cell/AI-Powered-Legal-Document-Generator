import sys
from pathlib import Path

import requests
import streamlit as st


# ---------------------------------------------------------
# Make project root importable
# ---------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from document_utils.exporters import (
    export_to_docx,
    export_to_pdf,
    export_to_txt,
)


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

BACKEND_URL = "http://127.0.0.1:8000"


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
)


# ---------------------------------------------------------
# Title
# ---------------------------------------------------------

st.title("⚖️ LegalEase")

st.subheader(
    "AI-Powered Legal Document Draft Generator"
)

st.write(
    "Create, edit and download professional legal document drafts."
)

st.info(
    "LegalEase creates drafts for informational purposes. "
    "Review important documents with a qualified legal professional "
    "before signing or using them."
)


# ---------------------------------------------------------
# Form
# ---------------------------------------------------------

with st.form("legal_document_form"):

    st.markdown("### Document Information")

    document_type = st.selectbox(
        "Document Type",

        [
            "Employment Contract",
            "Lease Agreement",
            "Non-Disclosure Agreement",
            "Service Agreement",
            "Freelance Agreement",
            "Partnership Agreement",
            "Loan Agreement",
            "Consulting Agreement",
            "Other",
        ],
    )

    if document_type == "Other":

        document_type = st.text_input(
            "Enter Document Type"
        )

    parties = st.text_area(
        "Parties",

        placeholder=(
            "Employer: ABC Technologies Pvt Ltd\n"
            "Employee: Rahul Kumar"
        ),

        height=120,
    )

    terms = st.text_area(
        "Important Terms",

        placeholder=(
            "Monthly salary: ₹40,000\n"
            "Working hours: 9 AM to 6 PM\n"
            "Probation period: 3 months\n"
            "Notice period: 30 days"
        ),

        height=180,
    )

    effective_date = st.text_input(
        "Effective Date",

        placeholder="01 October 2026",
    )

    jurisdiction = st.text_input(
        "Jurisdiction",

        value="India",
    )

    additional_instructions = st.text_area(
        "Additional Instructions",

        placeholder=(
            "Use simple professional language.\n"
            "Include confidentiality and termination clauses."
        ),

        height=120,
    )

    submitted = st.form_submit_button(
        "Generate Legal Document",
        use_container_width=True,
    )


# ---------------------------------------------------------
# Generate
# ---------------------------------------------------------

if submitted:

    if not parties.strip():

        st.error(
            "Please enter the parties."
        )

        st.stop()

    if not terms.strip():

        st.error(
            "Please enter the important terms."
        )

        st.stop()

    if not effective_date.strip():

        st.error(
            "Please enter the effective date."
        )

        st.stop()

    payload = {

        "document_type": document_type,

        "parties": parties,

        "terms": terms,

        "effective_date": effective_date,

        "jurisdiction": jurisdiction,

        "additional_instructions":
            additional_instructions,
    }

    with st.spinner(
        "Generating your legal document..."
    ):

        try:

            response = requests.post(
                f"{BACKEND_URL}/generate",

                json=payload,

                timeout=180,
            )

        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to the FastAPI backend.\n\n"
                "Make sure the backend is running on "
                "http://127.0.0.1:8000"
            )

            st.stop()

        except requests.exceptions.Timeout:

            st.error(
                "The backend took too long to respond. "
                "Please try again."
            )

            st.stop()

        except requests.exceptions.RequestException as exc:

            st.error(
                f"Request error: {exc}"
            )

            st.stop()


    # -----------------------------------------------------
    # Backend response
    # -----------------------------------------------------

    if response.status_code == 200:

        try:

            result = response.json()

        except ValueError:

            st.error(
                "Backend returned invalid JSON."
            )

            st.code(
                response.text
            )

            st.stop()


        if result.get("success"):

            st.session_state[
                "generated_document"
            ] = result.get(
                "document",
                ""
            )

            st.success(
                "Document generated successfully!"
            )

        else:

            st.error(
                result.get(
                    "detail",
                    "Document generation failed."
                )
            )

    else:

        try:

            error_data = response.json()

            error_message = error_data.get(
                "detail",
                "Unknown backend error."
            )

        except ValueError:

            error_message = response.text

        st.error(
            f"Backend Error (HTTP {response.status_code})"
        )

        st.code(
            str(error_message)
        )


# ---------------------------------------------------------
# Generated document editor
# ---------------------------------------------------------

if "generated_document" in st.session_state:

    st.divider()

    st.header(
        "Generated Document"
    )

    edited_document = st.text_area(
        "Edit your document before downloading:",

        value=st.session_state[
            "generated_document"
        ],

        height=600,
    )

    st.session_state[
        "generated_document"
    ] = edited_document


    # -----------------------------------------------------
    # Downloads
    # -----------------------------------------------------

    st.subheader(
        "Download"
    )

    col1, col2, col3 = st.columns(3)


    # TXT
    with col1:

        txt_data = export_to_txt(
            edited_document
        )

        st.download_button(
            label="Download TXT",

            data=txt_data,

            file_name="LegalEase_Document.txt",

            mime="text/plain",

            use_container_width=True,
        )


    # DOCX
    with col2:

        docx_data = export_to_docx(
            edited_document
        )

        st.download_button(
            label="Download DOCX",

            data=docx_data,

            file_name="LegalEase_Document.docx",

            mime=(
                "application/vnd.openxmlformats-"
                "officedocument.wordprocessingml.document"
            ),

            use_container_width=True,
        )


    # PDF
    with col3:

        pdf_data = export_to_pdf(
            edited_document
        )

        st.download_button(
            label="Download PDF",

            data=pdf_data,

            file_name="LegalEase_Document.pdf",

            mime="application/pdf",

            use_container_width=True,
        )


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.divider()

st.caption(
    "LegalEase — AI-powered legal document drafting tool. "
    "Generated documents should be reviewed before legal use."
)