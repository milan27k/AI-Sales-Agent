import streamlit as st
import requests

st.set_page_config(
    page_title="AI Sales Agent"
)
st.title("Ai Sales Agent")

company = st.text_input("company name")
industry = st.text_input("industry")
website = st.text_input("website")
contact_email = st.text_input("contact_email")

st.write(contact_email)
if st.button("analyze lead"):
    if not company or not industry or not website or not contact_email:
        st.error("Please fill all fields")
        st.stop()
    with st.spinner("analyzing...."):
        response = requests.post(
            "http://127.0.0.1:8000/analyze",
            json={
                 "company":company,
                 "industry":industry,
                 "website":website,
                 "contact_email":contact_email
            }
            )
        result = response.json()
        result["company"] = company
        result["industry"] = industry
        result["website"] = website
        result["contact_email"] = contact_email

    st.subheader("research")
    st.write(result['research'])

    st.subheader("lead score")
    st.write(result['score'])

    st.subheader("email")
    st.write(result['email'])

                     