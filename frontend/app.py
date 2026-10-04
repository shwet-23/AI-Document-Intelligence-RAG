import requests
import streamlit as st


# --------------------------------
# CONFIGURATION
# --------------------------------

API_URL = "http://127.0.0.1:8000"


# --------------------------------
# GET DOCUMENTS
# --------------------------------

def get_documents():

    try:

        response = requests.get(
            f"{API_URL}/documents"
        )

        if response.status_code == 200:

            return response.json().get(
                "documents",
                []
            )

    except requests.RequestException:

        return []

    return []


# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="AI Document Intelligence",
    page_icon="🤖",
    layout="centered"
)


# --------------------------------
# TITLE
# --------------------------------

st.title("🤖 AI Document Intelligence")

st.write(
    "Upload a PDF and chat with your documents using AI."
)


# --------------------------------
# CHAT HISTORY
# --------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


# --------------------------------
# PDF UPLOAD
# --------------------------------

st.subheader("📄 Upload Document")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)


if uploaded_file is not None:

    if st.button("📤 Upload Document"):

        with st.spinner(
            "Uploading and processing document..."
        ):

            try:

                response = requests.post(
                    f"{API_URL}/upload",
                    files={
                        "file": (
                            uploaded_file.name,
                            uploaded_file,
                            "application/pdf"
                        )
                    }
                )

                if response.status_code == 200:

                    result = response.json()

                    st.success(
                        result["message"]
                    )

                else:

                    st.error(
                        f"Upload failed: {response.text}"
                    )

            except requests.RequestException as error:

                st.error(
                    f"Backend connection error: {error}"
                )


# --------------------------------
# DOCUMENT SELECTION
# --------------------------------

st.divider()

st.subheader("📚 Select Documents")

available_documents = get_documents()


if available_documents:

    selected_documents = st.multiselect(
        "Choose which documents AI should use:",
        options=available_documents,
        default=available_documents
    )

else:

    selected_documents = []

    st.info(
        "No PDF documents available yet."
    )


# --------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------

st.subheader("💬 Document Chat")


for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )

        # ----------------------------
        # SOURCES
        # ----------------------------

        if message.get("sources"):

            st.caption("📚 Sources")

            for index, source in enumerate(
                message["sources"],
                start=1
            ):

                document = source.get(
                    "document",
                    "Unknown document"
                )

                page = source.get(
                    "page",
                    "Unknown"
                )

                relevance = source.get(
                    "relevance"
                )


                if relevance is not None:

                    st.caption(
                        f"📄 {index}. {document} "
                        f"— Page {page} "
                        f"• Relevance: {relevance}%"
                    )

                else:

                    st.caption(
                        f"📄 {index}. {document} "
                        f"— Page {page}"
                    )


# --------------------------------
# CHAT INPUT
# --------------------------------

question = st.chat_input(
    "Ask a question about your documents..."
)


if question:

    # --------------------------------
    # ADD USER MESSAGE
    # --------------------------------

    st.session_state.messages.append({

        "role": "user",

        "content": question

    })


    # --------------------------------
    # PREVIOUS CONVERSATION
    # --------------------------------

    history = [

        {
            "role": message["role"],
            "content": message["content"]
        }

        for message in st.session_state.messages[:-1]

    ]


    # --------------------------------
    # ASK BACKEND
    # --------------------------------

    with st.spinner(
        "🔍 Searching documents and generating answer..."
    ):

        try:

            response = requests.post(

                f"{API_URL}/ask",

                json={

                    "question": question,

                    "history": history,

                    "selected_documents": selected_documents

                }

            )


            # --------------------------------
            # SUCCESS
            # --------------------------------

            if response.status_code == 200:

                result = response.json()

                answer = result["answer"]

                sources = result["sources"]


                # Add AI response to history

                st.session_state.messages.append({

                    "role": "assistant",

                    "content": answer,

                    "sources": sources

                })


                st.rerun()


            # --------------------------------
            # BACKEND ERROR
            # --------------------------------

            else:

                st.error(
                    f"Failed to get answer: {response.text}"
                )


        except requests.RequestException as error:

            st.error(
                f"Backend connection error: {error}"
            )