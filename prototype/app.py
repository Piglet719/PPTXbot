import os
import fitz  # PyMuPDF
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import streamlit as st
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from md2pptx import convert_markdown_to_pptx

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# read all pdf files and return text
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# split text into chunks
def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000, chunk_overlap=1000)
    chunks = splitter.split_text(text)
    return chunks  # list of strings

# get embeddings for each chunk
def get_vector_store(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001")  # type: ignore
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro",
                                   client=genai,
                                   temperature=0.3,
                                   )
    prompt = PromptTemplate(template=prompt_template,
                            input_variables=["context", "question"])
    chain = load_qa_chain(llm=model, chain_type="stuff", prompt=prompt)
    return chain

def clear_chat_history():
    st.session_state.messages = [
        {"role": "assistant", "content": "upload some pdfs"}]

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001")  # type: ignore

    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True) 
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    response = chain(
        {"input_documents": docs, "question": user_question}, return_only_outputs=True, )

    print(response)
    return response

def display_pdf(pdf_file):
    doc = fitz.open(pdf_file)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img_data = pix.tobytes("ppm")
        st.image(img_data, caption=f"Page {page_num + 1}", use_column_width=True)

def get_md_chain():
    prompt_template = """
    Please use Markdown syntax to output detailed presentation content from the provided context. Make sure to provide all the details. \n\n
    Context:\n {context}\n

    Presentation content example:
    # Title
    ## Introduction
    - **Keyword**: Description.
    - **Keyword2**: Description2.
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro",
                                   client=genai,
                                   temperature=0.3,
                                   )
    prompt = PromptTemplate(template=prompt_template,
                            input_variables=["context"])
    chain = load_qa_chain(llm=model, chain_type="stuff", prompt=prompt)
    return chain

def output_md():
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001")  # type: ignore

    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True) 
    docs = new_db.similarity_search("Summarize this content")

    chain = get_md_chain()

    response = chain(
        {"input_documents": docs}, return_only_outputs=True, )

    print(response)
    return response

def save_uploadedfile(uploadedfile):
    with open(os.path.join("uploaded_files", uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    return os.path.join("uploaded_files", uploadedfile.name)

def main():
    st.set_page_config(
        page_title="Gemini PDF Chatbot",
        page_icon="🤖"
    )

    # Ensure the upload directory exists
    if not os.path.exists("uploaded_files"):
        os.makedirs("uploaded_files")

    # Sidebar for uploading PDF files
    with st.sidebar:
        st.title("Menu:")
        menu_option = st.selectbox(
            "Choose an option",
            ["Upload PDF", "Display PDF", "Create PPT from PDF", "Chat with Bot"]
        )
        pdf_docs = st.file_uploader(
            "Upload your PDF Files", accept_multiple_files=True)
        template = st.file_uploader("Upload your PowerPoint template")
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                if pdf_docs:
                    saved_files = [save_uploadedfile(pdf) for pdf in pdf_docs]
                    raw_text = get_pdf_text(saved_files)
                    text_chunks = get_text_chunks(raw_text)
                    get_vector_store(text_chunks)
                    st.success("Done")

    if menu_option == "Display PDF":
        if pdf_docs:
            saved_files = [save_uploadedfile(pdf) for pdf in pdf_docs]
            for pdf in saved_files:
                display_pdf(pdf)
        else:
            st.warning("Please upload a PDF file first.")

    if menu_option == "Create PPT from PDF":
        if template and pdf_docs:
            with st.spinner("Generating Markdown..."):
                saved_files = [save_uploadedfile(pdf) for pdf in pdf_docs]
                raw_text = get_pdf_text(saved_files)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                response = output_md()
                placeholder = st.empty()
                full_response = ''
                for item in response['output_text']:
                    full_response += item
                    placeholder.text(full_response)
                placeholder.text(full_response)
                pptx_file = convert_markdown_to_pptx(full_response, template)
                with open(pptx_file, "rb") as file:
                    st.download_button(
                        label="Download PPTX",
                        data=file,
                        file_name="presentation.pptx",
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                    )
        else:
            st.warning("Please upload both a PDF file and a PowerPoint template.")

    if menu_option == "Chat with Bot":
        st.title("Chat with PDF files using Gemini🤖")
        st.write("Welcome to the chat!")
        st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

        if "messages" not in st.session_state.keys():
            st.session_state.messages = [
                {"role": "assistant", "content": "upload some pdfs"}]

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        if prompt := st.chat_input():
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = user_input(prompt)
                    placeholder = st.empty()
                    full_response = ''
                    for item in response['output_text']:
                        full_response += item
                        placeholder.text(full_response)
                    placeholder.text(full_response)
            if response is not None:
                message = {"role": "assistant", "content": full_response}
                st.session_state.messages.append(message)

if __name__ == "__main__":
    main()
