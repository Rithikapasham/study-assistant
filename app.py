
import streamlit as st
import ollama
import chromadb
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
import uuid

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide"
)

st.title("📚 AI Study Assistant")
st.caption("Your personal AI tutor powered by Ollama and RAG")

# ---------------- SETTINGS ----------------

MODEL = "llama3.2"

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

@st.cache_resource
def load_database():
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(
        name="study_documents"
    )
    return collection

embedder = load_embedding_model()
collection = load_database()

# ---------------- SESSION MEMORY ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- AI FUNCTION ----------------

def ask_ai(prompt, history=None, system_prompt=None):
    messages = [
        {
            "role": "system",
            "content": system_prompt or
            "You are a friendly AI study tutor. "
            "Explain concepts in simple language with "
            "examples and step-by-step explanations."
        }
    ]

    if history:
        messages.extend(history)

    messages.append({
        "role": "user",
        "content": prompt
    })

    response = ollama.chat(
        model=MODEL,
        messages=messages
    )

    return response["message"]["content"]

# ---------------- PDF PROCESSING ----------------

def extract_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text

def split_text(text, chunk_size=700, overlap=100):
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])

        if chunk.strip():
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks

def store_pdf(uploaded_file):
    text = extract_pdf_text(uploaded_file)

    if not text.strip():
        return 0

    chunks = split_text(text)

    embeddings = embedder.encode(chunks).tolist()

    # Unique IDs prevent accidental overwriting
    ids = [str(uuid.uuid4()) for _ in chunks]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids,
        metadatas=[
            {"filename": uploaded_file.name}
            for _ in chunks
        ]
    )

    return len(chunks)

# ---------------- DOCUMENT SEARCH ----------------

def search_documents(question, n_results=3):
    if collection.count() == 0:
        return ""

    query_embedding = embedder.encode(
        [question]
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=min(n_results, collection.count())
    )

    documents = results.get("documents", [[]])[0]

    return "\n\n".join(documents)

# ---------------- SIDEBAR ----------------

st.sidebar.title("⚙️ Study Settings")

mode = st.sidebar.selectbox(
    "Choose Study Mode",
    [
        "AI Tutor",
        "PDF Question Answering",
        "Summarize Notes",
        "Generate Quiz"
    ]
)

st.sidebar.markdown("---")
st.sidebar.write("📖 Upload your study material")

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file is not None:
    if st.sidebar.button("Process PDF"):
        with st.spinner("Reading and indexing PDF..."):
            try:
                count = store_pdf(uploaded_file)
                st.sidebar.success(
                    f"Processed {count} text chunks!"
                )
            except Exception as e:
                st.sidebar.error(str(e))

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# ---------------- DISPLAY CHAT HISTORY ----------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- USER INPUT ----------------

user_question = st.chat_input(
    "Ask your study question..."
)

if user_question:
    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        with st.spinner("Preparing your answer..."):
            try:
                if mode == "AI Tutor":
                    system_prompt = (
                        "You are a friendly AI tutor. "
                        "Explain concepts simply, "
                        "use examples and organize answers "
                        "with headings and bullet points."
                    )

                    answer = ask_ai(
                        user_question,
                        history=st.session_state.messages[:-1],
                        system_prompt=system_prompt
                    )

                elif mode == "PDF Question Answering":
                    context = search_documents(user_question)

                    if not context:
                        answer = (
                            "Please upload and process a PDF "
                            "first so I can answer from your notes."
                        )
                    else:
                        prompt = f"""
                        Answer the question using the
                        following study material.

                        Study material:
                        {context}

                        Question:
                        {user_question}

                        If the answer is not in the material,
                        clearly say that the document does
                        not provide enough information.
                        """

                        answer = ask_ai(prompt)

                elif mode == "Summarize Notes":
                    context = search_documents(user_question)

                    if not context:
                        answer = (
                            "Please upload and process your "
                            "PDF notes first."
                        )
                    else:
                        prompt = f"""
                        Summarize the following study material.
                        Use simple language, headings,
                        important points and examples.

                        Material:
                        {context}

                        Additional instruction:
                        {user_question}
                        """
                        answer = ask_ai(prompt)

                elif mode == "Generate Quiz":
                    context = search_documents(user_question)

                    if not context:
                        answer = (
                            "Please upload and process your "
                            "PDF notes first."
                        )
                    else:
                        prompt = f"""
                        Create 5 study questions based on
                        the following material.

                        Include multiple-choice questions,
                        four options per question,
                        and an answer key with short explanations.

                        Material:
                        {context}

                        Topic or instruction:
                        {user_question}
                        """
                        answer = ask_ai(prompt)

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error(
                    "Error connecting to the AI model. "
                    "Check whether Ollama is running "
                    f"and the model {MODEL} is installed.\n\n{e}"
                )