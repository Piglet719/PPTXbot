import os
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

UPLOAD_FOLDER = 'uploaded_files'

def get_pdf_text(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        pdf_reader = PdfReader(file)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"  # Append the text of each page
    return text

def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000, chunk_overlap=1000)
    chunks = splitter.split_text(text)
    return chunks

def get_vector_store(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001")
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

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001")

    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True) 
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    response = chain(
        {"input_documents": docs, "question": user_question}, return_only_outputs=True, )

    return response['output_text']

def read_pdf(pdf_path):
    raw_text = get_pdf_text(pdf_path)
    text_chunks = get_text_chunks(raw_text)
    get_vector_store(text_chunks)

def output_md():
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001")

    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True) 
    docs = new_db.similarity_search("Summarize this content")

    chain = get_md_chain()

    response = chain(
        {"input_documents": docs}, return_only_outputs=True, )

    return response

def save_uploadedfile(uploadedfile):
    filename = secure_filename(uploadedfile.filename)
    file_path = os.path.join("uploaded_files", filename)
    uploadedfile.save(file_path)
    return file_path

def get_md_chain():
    prompt_template = """
Please use Markdown syntax to output detailed presentation content from the provided context. Make sure to provide all the details and include speaker notes using the format ::: notes ... ::: at the end of each section or slide. The speaker notes should be written in a way that the presenter can read them directly during the presentation.

Context:
{context}

This is an example of how the presentation content should be structured. Make sure to substitute the placeholders with the actual content from the provided context:

# Presentation Title

## Introduction
- **Keyword1**: Detailed description of Keyword1.
- **Keyword2**: Detailed description of Keyword2.\n
::: notes
Provide additional information or explanation for the presenter here. Write it as a script that the presenter can read directly.
:::

## Section 1: Detailed Analysis
- **Subsection 1.1**: Comprehensive explanation of Subsection 1.1, including relevant data and insights.
- **Subsection 1.2**: In-depth discussion of Subsection 1.2, covering key points and implications.\n
::: notes
Elaborate on the key points discussed in this section, providing examples or anecdotes that the presenter can use.
:::

## Section 2: Methodology
- **Step 1**: Description of Step 1, explaining the process and tools used.
- **Step 2**: Description of Step 2, highlighting important considerations and techniques.\n
::: notes
Guide the presenter through the methodology, emphasizing any critical steps or potential pitfalls to avoid.
:::

## Section 3: Results and Discussion
- **Result 1**: Analysis of Result 1, interpreting the data and its significance.
- **Result 2**: Discussion of Result 2, connecting it to the broader context and objectives.\n
::: notes
Offer insights into the results, suggesting ways the presenter can engage the audience with questions or interactive elements.
:::

## Conclusion
- **Summary**: Recap the main findings and their implications.
- **Future Work**: Outline potential future research directions or applications.\n
::: notes
Provide closing remarks and any final points for the presenter here. Encourage the audience to ask questions or provide feedback.
:::
"""


    model = ChatGoogleGenerativeAI(model="gemini-pro",
                                   client=genai,
                                   temperature=0.3,
                                   )
    prompt = PromptTemplate(template=prompt_template,
                            input_variables=["context"])
    chain = load_qa_chain(llm=model, chain_type="stuff", prompt=prompt)
    return chain

def get_recent_pdf_content():
    files = os.listdir(UPLOAD_FOLDER)
    pdf_files = [file for file in files if file.endswith('.pdf')]
    if pdf_files:
        recent_pdf = max(pdf_files, key=lambda x: os.path.getctime(os.path.join(UPLOAD_FOLDER, x)))
        pdf_path = os.path.join(UPLOAD_FOLDER, recent_pdf)
        if os.path.exists(pdf_path):
            print(pdf_path)
            return pdf_path
    return None

