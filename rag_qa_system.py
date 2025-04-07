import os
import torch
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain_huggingface import HuggingFacePipeline
from langchain.chains import RetrievalQA
from langchain.schema import Document
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.llms import LlamaCpp

device = "cpu"

# Set up embedding model and vector store
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db_path = "chroma_persistent_storage"
vector_store = Chroma(persist_directory=db_path, embedding_function=embedding_model)

pdf_folder = "/Users/varsha/Desktop/rag_qa_app/mental_health_documents/mental_health_documents"

def load_documents_from_pdfs(directory_path):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    documents = []

    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory_path, filename)
            print(f"🔍 Loading PDF: {file_path}")
            loader = PyMuPDFLoader(file_path)
            pages = loader.load()
            for page in pages:
                chunks = text_splitter.split_documents([page])
                documents.extend(chunks)
    
    return documents

if not os.path.exists(os.path.join(db_path, "index")):
    print("⚙️ No index found — loading PDFs and creating vector store...")
    docs = load_documents_from_pdfs(pdf_folder)
    if not docs:
        raise ValueError("❌ No documents found! Check your folder.")
    vector_store.add_documents(docs)
    vector_store.persist()
    print("✅ Documents loaded and stored!")

else:
    print("📂 Using existing vector store...")

# Retriever and LLM setup
retriever = vector_store.as_retriever(search_kwargs={"k":2})


llm = LlamaCpp(
    model_path="models/mistral-7b-instruct-v0.2-q4_0.gguf",
    n_ctx=2048,  # Increase if needed (depends on model)
    n_threads=8,  # Adapt to your CPU
    temperature=0.7,
    top_p=0.9,
    repeat_penalty=1.1,
    max_tokens=512,
    verbose=True
)


custom_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=(
        "You are a helpful and knowledgeable medical assistant. "
        "Answer the question in a clear, detailed, and friendly way, as if you’re explaining it to someone without a medical background. "
        "Use the information from the context below. If the answer is not available, say 'I don't know.'\n\n"
        "Context:\n{context}\n\n"
        "Question:\n{question}\n\n"
        "Answer:"
    )
)


memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    memory=memory,
    chain_type="stuff",
    chain_type_kwargs={"prompt": custom_prompt}
)

def get_rag_response(query):
    docs = retriever.get_relevant_documents(query)
    print("📄 Retrieved Context:")
    for d in docs:
        print(d.page_content[:500])  # print first 500 chars

    response = rag_chain.invoke({"query": query})["result"].strip()

    return response


