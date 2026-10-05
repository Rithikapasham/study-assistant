# 📚 AI Study Assistant

An **AI-powered Study Assistant** built with **Python, Streamlit, Ollama, ChromaDB, Sentence Transformers, and RAG (Retrieval-Augmented Generation)**.

The application works as a personal AI tutor that can answer questions, understand uploaded PDF study materials, summarize notes, and generate quizzes.

---

## 🚀 Features

### 🤖 AI Tutor

* Ask general academic questions.
* Get simple and easy-to-understand explanations.
* Provides examples and step-by-step explanations.
* Maintains conversation history during the session.

### 📄 PDF Question Answering

* Upload study materials in PDF format.
* Extract text automatically from the PDF.
* Split the document into smaller chunks.
* Convert chunks into vector embeddings.
* Store embeddings in ChromaDB.
* Retrieve relevant information using semantic search.
* Generate answers based on the uploaded study material.

### 📝 Summarize Notes

* Upload your notes as a PDF.
* Retrieve relevant sections from the document.
* Generate simple summaries.
* Organizes information using headings and important points.

### 🧠 Generate Quiz

* Creates 5 questions based on uploaded study material.
* Generates multiple-choice questions.
* Provides four options for each question.
* Includes an answer key and short explanations.

### 💬 Chat Interface

* Interactive Streamlit chat interface.
* Displays previous messages.
* Provides a **Clear Chat** option.
* Supports multiple study modes.

---

## 🛠️ Technologies Used

| Technology                | Purpose                                       |
| ------------------------- | --------------------------------------------- |
| **Python**                | Main programming language                     |
| **Streamlit**             | Web application interface                     |
| **Ollama**                | Runs the local Llama AI model                 |
| **Llama 3.2**             | Large Language Model                          |
| **ChromaDB**              | Vector database for document storage          |
| **Sentence Transformers** | Generates document embeddings                 |
| **PyPDF**                 | Extracts text from PDF files                  |
| **UUID**                  | Generates unique document chunk IDs           |
| **RAG**                   | Retrieves relevant information from documents |

---

## 🧩 System Architecture

```text
                  ┌─────────────────────┐
                  │       User          │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │     Streamlit UI    │
                  └──────────┬──────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
        AI Tutor       PDF Processing    Study Modes
                             │
                             ▼
                      ┌──────────────┐
                      │  PyPDF       │
                      │ Text Extract │
                      └──────┬───────┘
                             │
                             ▼
                      ┌──────────────┐
                      │ Text Chunking│
                      └──────┬───────┘
                             │
                             ▼
                  ┌────────────────────┐
                  │ SentenceTransformers│
                  │    Embeddings      │
                  └──────────┬─────────┘
                             │
                             ▼
                      ┌──────────────┐
                      │   ChromaDB   │
                      │ Vector Store │
                      └──────┬───────┘
                             │
                       Semantic Search
                             │
                             ▼
                      ┌──────────────┐
                      │   Ollama     │
                      │  Llama 3.2   │
                      └──────┬───────┘
                             │
                             ▼
                      ┌──────────────┐
                      │ AI Response  │
                      └──────────────┘
```

---

## 🔍 How RAG Works

This project uses **Retrieval-Augmented Generation (RAG)** for answering questions from PDF documents.

### Step 1: Upload PDF

The user uploads a PDF containing study material.

### Step 2: Extract Text

`PyPDF` extracts text from every page.

```python
reader = PdfReader(uploaded_file)
```

### Step 3: Split Text

The extracted text is divided into smaller chunks.

```python
chunks = split_text(text)
```

The project uses:

* Chunk size: **700 words**
* Overlap: **100 words**

The overlap helps preserve context between chunks.

### Step 4: Generate Embeddings

Sentence Transformers converts each chunk into a numerical vector.

```python
embedder.encode(chunks)
```

The project uses:

```text
all-MiniLM-L6-v2
```

### Step 5: Store in ChromaDB

The embeddings and corresponding text chunks are stored in ChromaDB.

```python
collection.add(
    documents=chunks,
    embeddings=embeddings,
    ids=ids
)
```

### Step 6: Search

When the user asks a question, the question is converted into an embedding.

ChromaDB searches for the most relevant document chunks.

### Step 7: Generate Answer

The retrieved information is provided to **Llama 3.2 through Ollama**.

The AI generates an answer using the retrieved study material.

```text
Question
   ↓
Embedding
   ↓
ChromaDB Search
   ↓
Relevant PDF Chunks
   ↓
Llama 3.2
   ↓
Answer
```

---

## 📁 Project Structure

```text
AI-Study-Assistant/
│
├── app.py
├── README.md
├── requirements.txt
│
└── chroma_db/
    └── Vector database files
```

> The Python file containing the provided code can be named `app.py`.

---

## ⚙️ Requirements

Make sure the following are installed:

* Python 3.9 or higher
* VS Code
* Ollama
* Llama 3.2
* Required Python libraries

---

## 📦 Installation

### 1. Clone or Download the Project

Open the project folder in VS Code.

### 2. Create a Virtual Environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

---

### 3. Install Required Libraries

Create a file called:

```text
requirements.txt
```

Add:

```text
streamlit
ollama
chromadb
sentence-transformers
pypdf
```

Then install them:

```bash
pip install -r requirements.txt
```

---

## 🦙 Install Ollama

Download and install Ollama on your computer.

After installation, check whether it is working:

```bash
ollama --version
```

Download the Llama 3.2 model:

```bash
ollama pull llama3.2
```

Test the model:

```bash
ollama run llama3.2
```

If the model responds, Ollama is ready.

---

## ▶️ Run the Application

Open the project folder in VS Code terminal.

Run:

```bash
streamlit run app.py
```

Streamlit will start the application and provide a local URL.

Usually it will be available at:

```text
http://localhost:8501
```

Open the URL in your browser.

---

## 🖥️ How to Use

### Step 1

Start Ollama and make sure the Llama 3.2 model is installed.

### Step 2

Run the Streamlit application:

```bash
streamlit run app.py
```

### Step 3

Select a study mode from the sidebar:

```text
AI Tutor
PDF Question Answering
Summarize Notes
Generate Quiz
```

### Step 4

For PDF-based features:

1. Click **Upload PDF**.
2. Select your study material.
3. Click **Process PDF**.
4. Wait for the indexing to complete.
5. Enter your question or instruction.
6. Get the AI-generated response.

---

## 📌 Study Modes

### 1. AI Tutor

Example:

```text
What is inheritance in Java?
```

The AI provides a simple explanation with examples.

---

### 2. PDF Question Answering

Example:

```text
What is the main purpose of normalization?
```

The application searches the uploaded PDF and generates an answer using the relevant content.

---

### 3. Summarize Notes

Example:

```text
Give me a summary of this chapter.
```

The application retrieves relevant document content and generates a simplified summary.

---

### 4. Generate Quiz

Example:

```text
Create a quiz about DBMS normalization.
```

The AI generates:

* 5 questions
* 4 options per question
* Correct answers
* Short explanations

---

## 💾 Data Storage

The project uses **ChromaDB** as a persistent vector database.

```python
client = chromadb.PersistentClient(
    path="./chroma_db"
)
```

The database is stored locally in:

```text
chroma_db/
```

Each uploaded PDF is converted into text chunks and stored as embeddings.

Unique UUIDs are used for every chunk:

```python
ids = [str(uuid.uuid4()) for _ in chunks]
```

This prevents accidental overwriting of existing chunks.

---

## 🔐 Privacy

This project is designed to work locally.

The AI model is accessed through **Ollama**, allowing the Llama model to run on the user's computer.

Uploaded PDF content is stored in the local ChromaDB database.

> Avoid uploading confidential or sensitive documents unless you understand how your local storage is configured.

---

## ⚡ Caching

The application uses Streamlit's resource caching:

```python
@st.cache_resource
```

This prevents the embedding model and database connection from being unnecessarily recreated every time the application reruns.

---

## 🧠 Technologies Explained

### Streamlit

Used to create the interactive web interface using Python.

### Ollama

Used to run the Llama 3.2 language model locally.

### Llama 3.2

Acts as the AI tutor and generates answers, summaries, and quizzes.

### ChromaDB

Stores document embeddings and performs similarity searches.

### Sentence Transformers

Converts text into numerical embeddings that can be compared for semantic similarity.

### PyPDF

Extracts text from uploaded PDF documents.

### RAG

Combines document retrieval with an LLM to generate answers based on external knowledge stored in the uploaded documents.

---

## 🎯 Project Objectives

The main objectives of this project are:

1. Build an AI-powered personal study assistant.
2. Provide simple explanations of academic concepts.
3. Allow students to interact with their PDF notes.
4. Implement RAG for document-based question answering.
5. Generate summaries from study material.
6. Automatically generate practice quizzes.
7. Use locally running AI models through Ollama.
8. Provide an easy-to-use Streamlit interface.

---

## 🌟 Advantages

* Easy to use
* Beginner-friendly interface
* Supports PDF study materials
* Local AI model support
* Uses RAG for document-based answers
* Multiple study modes
* Interactive chat interface
* Persistent vector database
* Useful for exam preparation
* Can work without sending study documents to a cloud LLM API

---

## 🔮 Future Enhancements

The project can be improved by adding:

* 📚 Multiple PDF support with document selection
* 🔊 Text-to-speech for AI answers
* 🎤 Voice-based questions
* 📊 Student progress tracking
* 📝 Automatic flashcard generation
* 🧪 Difficulty-based quiz generation
* 📈 Quiz score analysis
* 🌐 Web-based research mode
* 👤 Student login and profiles
* 💾 Chat history storage
* 📑 Page-number citations from PDFs
* 🌙 Dark/light theme
* 📱 Improved mobile interface

---

## 🐛 Troubleshooting

### Ollama is not recognized

If you get:

```text
ollama is not recognized as the name of a cmdlet
```

make sure Ollama is installed and restart VS Code after installation.

Then run:

```bash
ollama --version
```

---

### Llama 3.2 is not installed

Run:

```bash
ollama pull llama3.2
```

Then test:

```bash
ollama run llama3.2
```

---

### Streamlit is not recognized

Install Streamlit:

```bash
pip install streamlit
```

Then run:

```bash
python -m streamlit run app.py
```

---

### PDF gives no answer

Make sure:

1. The PDF contains selectable text.
2. The PDF was successfully processed.
3. You clicked **Process PDF**.
4. ChromaDB contains the document chunks.
5. Your question relates to the uploaded material.

Scanned/image-only PDFs may require OCR before their text can be extracted.

---

## 📜 License

This project is intended for **educational and academic purposes**.

You may modify and extend the project for learning, demonstrations, and college projects.

---

## 👩‍💻 Author

**AI Study Assistant**

Built using:

```text
Python + Streamlit + Ollama + Llama 3.2
+ ChromaDB + Sentence Transformers + RAG
```

---

## ⭐ Project Summary

**AI Study Assistant** is a locally powered educational application that combines **Generative AI and RAG technology** to help students learn from their own study materials.

Users can interact with an AI tutor, upload PDF notes, ask questions about their documents, generate summaries, and create quizzes. The combination of **Llama 3.2, Ollama, Sentence Transformers, and ChromaDB** provides a practical implementation of an AI-powered learning assistant.
