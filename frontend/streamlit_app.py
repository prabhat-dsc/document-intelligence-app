import requests
import streamlit as st

API_URL = st.sidebar.text_input(
    "API URL",
    "http://localhost:8000/api/v1",
)

st.set_page_config(
    page_title="Document Intelligence",
    page_icon="📚",
    layout="wide",
)

st.title("📚 Document Intelligence")
st.caption("OCR + Hybrid Search + Reranking + RAG")

if "session_id" not in st.session_state:
    import uuid
    st.session_state.session_id = str(uuid.uuid4())

with st.sidebar:
    st.header("Documents")
    uploaded = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True,
    )    

    if st.button("Upload & Process", disabled=not uploaded):
            files = [
                (
                "files",
                (file.name, file.getvalue(), "application/pdf"),
                )
            for file in uploaded
            ]
            with st.spinner("Uploading..."):
                response = requests.post(
                    f"{API_URL}/documents/upload",
                    files=files,
                    timeout=120,
                )

            
            if response.ok:
                 st.success("Documents uploaded. Processing started.")
            else:
                 st.error(response.text)

    st.divider()    


