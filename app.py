# app.py
import time
import streamlit as st
from src.helper import get_pdf_text, get_text_chunks, get_vector_store, get_conversational_chain
def handle_user_input(user_question):
    # Run the conversation chain and get the answer
    response = st.session_state.conversation.invoke({"question": user_question})
    
    # Show user question
    st.write("User:", user_question)
    
    # Show bot answer
    st.write("Bot:", response["answer"])

    # Optional: if you want to show full history (requires access to memory)
    if hasattr(st.session_state.conversation, "memory"):
        chat_history = st.session_state.conversation.memory.chat_memory.messages
        st.subheader("Chat History")
        for i, message in enumerate(chat_history):
            role = "User" if i % 2 == 0 else "Bot"
            st.markdown(f"**{role}:** {message.content}")


def main():
    st.header("📄 Information Retrieval System")
    user_question = st.text_input("Ask a question about the PDF documents:")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    with st.sidebar:
        st.title("📂 Upload & Process PDFs")
        pdf_docs = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

        if st.button("Submit & Process"):
            if not pdf_docs or len(pdf_docs) == 0:
                st.warning("Please upload at least one PDF file.")
            else:
                with st.spinner("Processing..."):
                    raw_text = get_pdf_text(pdf_docs)
                    if not raw_text.strip():
                        st.warning("No text found in the PDFs. Try different files.")
                    else:
                        text_chunks = get_text_chunks(raw_text)
                        if len(text_chunks) == 0:
                            st.warning("Text chunks could not be created. Check chunk size or PDF content.")
                        else:
                            vector_store = get_vector_store(text_chunks)
                            st.session_state.conversation = get_conversational_chain(vector_store)
                            st.success("✅ Processing complete!")

    if user_question and st.session_state.conversation:
        handle_user_input(user_question)


if __name__ == "__main__":
    main()
