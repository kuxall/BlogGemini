import streamlit as st
import streamlit_chat as st_chat
import PyPDF2 as pdf
import google.generativeai as genai
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

# Set up Google API key from Streamlit secrets
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# Set up the page
st.set_page_config(layout="wide", page_icon="📜", page_title="PDF Q&A with RAG")
st.title("PDF Q&A with RAG")

# Set up chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to clear chat history


def clear_chat():
    st.session_state.chat_history = []


# Clear button and chat input side by side
col1, col2 = st.columns([1, 5])
with col1:
    st.button("Clear Chat", on_click=clear_chat)
with col2:
    user_question = st.text_input("Ask a question about the PDF:")

# Function to extract text from PDF


@st.cache_data
def extract_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to create vector store


@st.cache_data
def create_vector_store(pdf_text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_text(pdf_text)
    embeddings = HuggingFaceEmbeddings()
    vector_store = FAISS.from_texts(texts, embeddings)
    return vector_store


# Upload PDF
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

# Extract text and create vector store if a PDF is uploaded
if uploaded_file and "vector_store" not in st.session_state:
    pdf_text = extract_pdf_text(uploaded_file)
    st.session_state.pdf_text = pdf_text
    st.session_state.vector_store = create_vector_store(pdf_text)
    st.success("PDF uploaded and text extracted!")

# Function to get response from gemini-pro model


def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)
    content = response.candidates[0].content.parts[0].text
    return content


# Improved Prompt Template
input_prompt_template = """
You are an advanced AI with extensive expertise in Laws and Ethics and worked as a lawyer. You have given the legal documents. Please answer the question based on their content. Your task is to understand the document and provide an accurate and relevant answer to the question in English. If you don't know the answer, you can say 'I don't know'.

document: {text}
question: {question}

The response should be in the following JSON format:
{{
  "Answer": "Detailed answer here."
}}
"""

# Process the question and get the response
if "vector_store" in st.session_state and user_question:
    if st.button("Ask", key="ask_button"):
        if user_question:
            # Retrieve relevant chunks from the vector store
            retriever = st.session_state.vector_store.as_retriever()
            docs = retriever.get_relevant_documents(user_question)
            context = "\n".join([doc.page_content for doc in docs])

            # Prepare the input for the gemini-pro model
            input_prompt = input_prompt_template.format(
                text=context, question=user_question)
            response_text = get_gemini_response(input_prompt)

            # Clean the response text
            response_text = response_text.strip().strip("```json").strip("```").strip()

            try:
                response = json.loads(response_text)
                answer = response["Answer"]

                # Add to chat history
                st.session_state.chat_history.append(
                    {"question": user_question, "answer": answer})
            except json.JSONDecodeError:
                st.error("Failed to decode JSON response from the model.")
        else:
            st.error("Please enter a question.")

# Display chat history
for chat in st.session_state.chat_history:
    st_chat.message(chat["question"], is_user=True)
    st_chat.message(chat["answer"])
