import streamlit as st
import requests

st.set_page_config(page_title="AI Sales Agent")
st.title("AI Sales Agent")

company = st.text_input("company name")
industry = st.text_input("industry")
website = st.text_input("website")
contact_email = st.text_input("contact_email")

if st.button("analyze lead"):
    if not company or not industry or not website or not contact_email:
        st.error("Please fill all fields")
        st.stop()

    with st.spinner("analyzing..."):
        response = requests.post(
            "http://127.0.0.1:8000/analyze",
            json={
                "company": company,
                "industry": industry,
                "website": website,
                "contact_email": contact_email
            },
            timeout=180
        )

        if response.status_code != 200:
            st.error(response.text)
            st.stop()

        st.session_state["lead_result"] = response.json()


if "lead_result" in st.session_state:
    result = st.session_state["lead_result"]

    st.subheader("Research")
    st.write(result["research"])

    st.subheader("Buying Signals")
    st.write(result["buying_signals"])

    st.subheader("ICP Qualification")
    st.write(result["qualification"])

    st.subheader("Lead Score")
    st.write(result["score"])

    st.subheader("Email")
    st.write(result["email"])

    st.divider()
    st.subheader("Human Approval")

    status = result.get("status", "PENDING_APPROVAL")

    if status == "PENDING_APPROVAL":
        st.warning("Review the lead before approving or rejecting it.")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Approve Lead", type="primary"):
                response = requests.post(
                    f"http://127.0.0.1:8000/leads/{result['lead_id']}/approve"
                )

                if response.status_code == 200:
                    result["status"] = "APPROVED"
                    st.session_state["lead_result"] = result
                    st.success("Lead approved. No email was sent.")
                    st.rerun()
                else:
                    st.error(response.text)

        with col2:
            if st.button("Reject Lead"):
                response = requests.post(
                    f"http://127.0.0.1:8000/leads/{result['lead_id']}/reject"
                )

                if response.status_code == 200:
                    result["status"] = "REJECTED"
                    st.session_state["lead_result"] = result
                    st.warning("Lead rejected.")
                    st.rerun()
                else:
                    st.error(response.text)

    elif status == "APPROVED":
        st.success("Lead approved. No email was sent.")

    elif status == "REJECTED":
        st.error("Lead rejected.")
