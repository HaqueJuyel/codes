# # app.py
# import streamlit as st
# import requests

# API_BASE = "http://localhost:8000"

# st.title("Resume Shortlisting AI")

# option = st.selectbox("Choose an option", ["Upload Resume", "Shortlist Candidates"])

# if option == "Upload Resume":
#     uploaded_file = st.file_uploader("Upload a resume (PDF)", type="pdf")
#     if uploaded_file is not None:
#         files = {"file": uploaded_file}
#         res = requests.post(f"{API_BASE}/upload_resume/", files=files)
#         st.success(f"Uploaded: {uploaded_file.name}")

# elif option == "Shortlist Candidates":
#     job_description = st.text_area("Paste the job description")
#     if st.button("Shortlist Resumes"):
#         res = requests.post(f"{API_BASE}/shortlist/", json={"job_description": job_description})
#         st.write("### Result:")
#         st.write(res.json()["result"])

# app.py
import streamlit as st
import requests

API_BASE = "http://localhost:8000"

st.title("🤖 Resume Shortlisting AI")

option = st.selectbox("Choose an option", ["Upload Resumes", "Shortlist Candidates"])

if option == "Upload Resumes":
    uploaded_files = st.file_uploader("Upload one or more resumes (PDF)", type="pdf", accept_multiple_files=True)
    if uploaded_files:
        for uploaded_file in uploaded_files:
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            res = requests.post(f"{API_BASE}/upload_resume/", files=files)
            if res.status_code == 200:
                st.success(f"✅ Uploaded: {uploaded_file.name}")
            else:
                st.error(f"❌ Failed to upload: {uploaded_file.name}")

# elif option == "Shortlist Candidates":
#     job_description = st.text_area("📄 Paste the Job Description")
#     if st.button("Shortlist Resumes"):
#         res = requests.post(f"{API_BASE}/shortlist/", json={"job_description": job_description})
#         if res.status_code == 200:
#             st.subheader("📌 Shortlisting Result:")
#             st.write(res.json()["result"])
#         else:
#             st.error("Error during shortlisting. Please try again.")
elif option == "Shortlist Candidates":
    job_description = st.text_area("📄 Paste the Job Description")
    if st.button("Shortlist Resumes"):
        res = requests.post(f"{API_BASE}/shortlist/", json={"job_description": job_description})
        if res.status_code == 200:
            data = res.json()
            st.subheader("📌 Shortlisting Result:")
            st.write(data["result"])
            st.subheader("📊 Resume Scores:")
            for i, resume in enumerate(data["scored_resumes"], start=1):
                st.markdown(f"**{i}. {resume['file']}**")
                st.write(f"🧠 Score: {resume['score_out_of_10']} / 10")
                st.write(f"📝 Preview: {resume['preview']}")
                st.markdown("---")

            # st.subheader("📊 Resume Scores:")
            # for i, resume in enumerate(data["scored_resumes"], start=1):
            #     st.markdown(f"**Candidate {i}**")
            #     st.write(f"🧠 Score: {resume['score_out_of_10']} / 10")
            #     st.write(f"📝 Preview: {resume['content']}")
            #     st.markdown("---")
        else:
            st.error("Error during shortlisting. Please try again.")
