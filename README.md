# 🩺 RAG-Based Medical Q&A System using LangChain

This is a **Retrieval-Augmented Generation (RAG) Q&A System** that provides **human-friendly and accurate responses** to medical questions. 
It leverages **LangChain, ChromaDB, and Mistral-7B** to retrieve and generate responses in a conversational format.

---

## Features

**Retrieval-Augmented Generation (RAG)** - Retrieves medical documents for accurate answers.
**LangChain Integration** - Uses LangChain's retriever, embeddings, and chains for structured querying.
**Optimized LLM (Mistral-7B)** - Runs efficiently with 4-bit quantization.
**Conversational Memory** - Keeps track of previous interactions using LangChain Memory.
**ChromaDB for Vector Storage** - Stores embeddings for fast retrieval.
**User-Friendly Gradio Interface** - Simple web-based chatbot UI.

---

## Installation  

### **1. Clone the Repository**  
```bash
git clone https://github.com/varshax11/RAG-based-Medical-Q-A-System-using-Langchain.git
cd RAG-based-Medical-Q-A-System-using-Langchain

```
### **2. Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows

```
### **3. Install Dependencies**

```bash
pip install -r requirements.txt

```
## Usage

## Run the Chatbot
```bash

python rag_qa_system.py

```
Once the server starts, a Gradio interface will open in your browser, where you can ask medical-related questions.

## Project Structure

```bash

medical-chatbot-langchain/
│── app.py                # Main chatbot script
│── requirements.txt      # Dependencies
│── README.md             # Project documentation
│── medical_records/      # Folder for storing medical documents
│── chroma_persistent_storage/  # Stores vectorized documents

```

## Contributing

Feel free to contribute! Open an issue or submit a pull request if you find any bugs or want to add improvements.

## License

This project is licensed under the MIT License
