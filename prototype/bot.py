import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from md2pptx import convert_markdown_to_pptx  # Importing the function
import boto3
from langchain_community.embeddings import BedrockEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.document_loaders import PyPDFLoader
from langchain_aws import BedrockLLM
import tempfile

load_dotenv()

region = boto3.Session().region_name
session = boto3.Session(region_name=region)

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000, chunk_overlap=1000)
    chunks = splitter.split_text(text)
    return chunks  # list of strings

def get_vector_store(chunks):
    embeddings = BedrockEmbeddings()
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_template = """
    Please use Markdown syntax to output detailed presentation content from the provided context. Make sure to provide all the details and include speaker notes using the format ::: notes ... ::: at the end of each section or slide. The speaker notes should be written in a way that the presenter can read them directly during the presentation.\n\n
    Context:\n {context}\n

    Presentation content example:
    # Title
    ## Introduction
    - **Keyword**: Description.
    - **Keyword2**: Description2.
    ::: notes
    Provide additional information or explanation for the presenter here. Write it as a script that the presenter can read directly.
    :::
    """

    model = BedrockLLM(
        model_id="anthropic.claude-instant-v1")

    prompt = PromptTemplate(template=prompt_template,
                            input_variables=["context"])
    chain = load_qa_chain(llm=model, chain_type="stuff", prompt=prompt)
    return chain

def clear_chat_history():
    st.session_state.messages = [
        {"role": "assistant", "content": "upload some pdfs"}]

def user_input(user_question):
    embeddings = BedrockEmbeddings()
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain(
        {"input_documents": docs}, return_only_outputs=True, )
    return response

def clean_markdown_content(markdown_text):
    """ Clean the markdown content by removing any text before the first h1 header """
    lines = markdown_text.split('\n')
    clean_lines = []
    found_h1 = False
    for line in lines:
        #print(f"Processing line: {line}")  # Debugging line to print each line being processed
        if line.startswith("# "):
            found_h1 = True
        if found_h1:
            clean_lines.append(line)
    # Print the lines for debugging
    '''print("Lines after split:")
    print(lines)
    print("Cleaned lines:")
    print(clean_lines)'''
    return '\n'.join(clean_lines)

def main():
    st.set_page_config(
        page_title="Gemini PDF Chatbot",
        page_icon="🤖"
    )

    # Sidebar for uploading PDF files
    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader(
            "Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        template = st.file_uploader("Upload your PowerPoint template")
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done")

    # Main content area for displaying chat messages
    st.title("PowerPaper🤖")
    st.write("Welcome to the chat!")
    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

    # Chat input
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
            {"role": "assistant", "content": "upload some pdfs"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input(placeholder="是否對ppt有特別的指示"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Display chat messages and bot response
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
                
                # Print the response for debugging
                '''print("Generated Response:")
                print(full_response)'''
                
                # Clean the markdown content
                clean_response = clean_markdown_content(full_response)

                # Print the cleaned markdown content for debugging
                '''print("Cleaned Markdown Content:")
                print(clean_response)'''

                # Handle template file
                if template is not None:
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pptx') as temp_template_file:
                        temp_template_file.write(template.read())
                        template_path = temp_template_file.name
                else:
                    template_path = None

                # Generate the PPTX file
                pptx_file = convert_markdown_to_pptx(clean_response, 'output.pptx', template_path)
                

                with open(pptx_file, "rb") as file:
                    st.download_button(
                        label="Download PPTX",
                        data=file,
                        file_name="presentation.pptx",
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                    )
        if response is not None:
            message = {"role": "assistant", "content": full_response}
            st.session_state.messages.append(message)

if __name__ == "__main__":
    main()
