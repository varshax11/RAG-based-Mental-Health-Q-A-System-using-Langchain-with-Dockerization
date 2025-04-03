import os
import torch
import gradio as gr
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from langchain.schema import Document
from langchain.memory import ConversationBufferMemory
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate


device = "cuda" if torch.cuda.is_available() else "cpu"

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

db_path = "/content/chroma_persistent_storage"
vector_store = Chroma(persist_directory=db_path, embedding_function=embedding_model)

def load_documents(directory_path):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    documents = []

    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            with open(os.path.join(directory_path, filename), "r", encoding="utf-8") as file:
                text = file.read()
                chunks = text_splitter.split_text(text)
                for i, chunk in enumerate(chunks):
                    documents.append(Document(page_content=chunk, metadata={"source": filename, "chunk_id": i+1}))

    vector_store.add_documents(documents)
    vector_store.persist()

directory_path = "/medical records directory path/" #your medical record documents path
if not os.path.exists(directory_path):
    os.makedirs(directory_path)
load_documents(directory_path)

retriever = vector_store.as_retriever(search_kwargs={"k": 2})

model_name = "mistralai/Mistral-7B-Instruct-v0.1"
bnb_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16)

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, quantization_config=bnb_config, device_map="auto")

llm_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_length=500,  
    temperature=0.7,  
    top_p=0.9,  
    repetition_penalty=1.1  
)
llm = HuggingFacePipeline(pipeline=llm_pipeline)


custom_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="Answer the question based on the provided context. If you don't know the answer, say 'I don't know'. \n\nContext: {context}\n\nQuestion: {question}\n\nAnswer: ",
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    memory=memory,
    chain_type="stuff",
    chain_type_kwargs={"prompt": custom_prompt}
)


def chatbot(question):
    response = rag_chain.run(question)
    return response.strip()


interface = gr.Interface(
    fn=chatbot,
    inputs=gr.Textbox(lines=2, placeholder="Ask a health-related question..."),
    outputs="text",
    title="🩺 RAG Medical System",
    description="Get concise and human-friendly answers for any health condition",
)

interface.launch(share=True)
