# # main.py
# from fastapi import FastAPI, UploadFile, File
# from langchain.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.vectorstores import Chroma
# from langchain.chains import RetrievalQA
# from langchain.chat_models import ChatOpenAI
# import shutil
# import os
# from dotenv import load_dotenv

# load_dotenv()

# app = FastAPI()

# CHROMA_DIR = "chroma_store"
# TEMP_DIR = "temp"
# os.makedirs(CHROMA_DIR, exist_ok=True)
# os.makedirs(TEMP_DIR, exist_ok=True)

# # Initialize embeddings and language model
# embeddings = OpenAIEmbeddings()
# llm = ChatOpenAI(model_name="gpt-3.5-turbo")

# @app.get("/")
# def read_root():
#     return {"message": "Resume Shortlister API is up and running."}

# @app.post("/upload_resume/")
# async def upload_resume(file: UploadFile = File(...)):
#     file_path = f"{TEMP_DIR}/{file.filename}"
#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     loader = PyPDFLoader(file_path)
#     docs = loader.load()

#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
#     chunks = text_splitter.split_documents(docs)

#     vectordb = Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_DIR)
#     vectordb.persist()

#     return {"status": "uploaded", "file": file.filename}

# @app.post("/shortlist/")
# async def shortlist(job_description: str):
#     vectordb = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
#     retriever = vectordb.as_retriever(search_kwargs={"k": 3})
#     qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

#     result = qa.run(f"Compare resumes with this job description and give best matches: {job_description}")
#     return {"result": result}


# main.py
from fastapi import FastAPI, UploadFile, File
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import shutil
import os
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

CHROMA_DIR = "chroma_store"
TEMP_DIR = "temp"
os.makedirs(CHROMA_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# Initialize embeddings and LLM
embeddings = OpenAIEmbeddings()
llm = ChatOpenAI(model_name="gpt-3.5-turbo")

@app.get("/")
def read_root():
    return {"message": "Resume Shortlister API is up and running."}

@app.post("/upload_resume/")
async def upload_resume(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(TEMP_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        loader = PyPDFLoader(file_path)
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_documents(docs)

        if os.path.exists(os.path.join(CHROMA_DIR, "index")):
            vectordb = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
            vectordb.add_documents(chunks)
        else:
            vectordb = Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_DIR)

        vectordb.persist()
        return {"status": "uploaded", "file": file.filename}
    
    except Exception as e:
        return {"status": "error", "file": file.filename, "error": str(e)}

class JobDescription(BaseModel):
    job_description: str

# @app.post("/shortlist/")
# async def shortlist(data: JobDescription):
#     vectordb = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
#     retriever = vectordb.as_retriever(search_kwargs={"k": 3})
#     qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

#     result = qa.run(f"Compare resumes with this job description and give best matches: {data.job_description}")
#     return {"result": result}

# @app.post("/shortlist/")
# async def shortlist(data: JobDescription):
#     vectordb = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
#     retriever = vectordb.as_retriever(search_kwargs={"k": 5})
#     qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

#     result = qa.run(f"Compare resumes with this job description and give best matches: {data.job_description}")

#     # Get top documents with scores
#     docs_with_scores = vectordb.similarity_search_with_score(data.job_description, k=5)

#     scored_resumes = []
#     for doc, score in docs_with_scores:
#         normalized_score = max(0, min(10, round((1 - score) * 10, 2)))  # Score out of 10
#         scored_resumes.append({
#             "content": doc.page_content[:300] + "...",  # Limit preview for UI
#             "score_out_of_10": normalized_score
#         })

#     return {
#         "result": result,
#         "scored_resumes": scored_resumes
#     }

from collections import defaultdict

@app.post("/shortlist/")
async def shortlist(data: JobDescription):
    vectordb = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    retriever = vectordb.as_retriever(search_kwargs={"k": 10})
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    result = qa.run(f"Compare resumes with this job description and give best matches: {data.job_description}")

    # Search top 20 most relevant chunks with scores
    docs_with_scores = vectordb.similarity_search_with_score(data.job_description, k=20)

    # Aggregate scores by resume (source)
    resume_scores = defaultdict(list)
    resume_previews = {}

    for doc, score in docs_with_scores:
        filename = doc.metadata.get("source", "Unknown")
        resume_scores[filename].append(score)
        if filename not in resume_previews:
            resume_previews[filename] = doc.page_content[:300] + "..."

    # Compute average score per resume
    scored_resumes = []
    for filename, scores in resume_scores.items():
        avg_score = sum(scores) / len(scores)
        normalized_score = max(0, min(10, round((1 - avg_score) * 10, 2)))
        scored_resumes.append({
            "file": filename,
            "score_out_of_10": normalized_score,
            "preview": resume_previews[filename]
        })

    # Sort by score descending
    scored_resumes = sorted(scored_resumes, key=lambda x: x["score_out_of_10"], reverse=True)

    return {
        "result": result,
        "scored_resumes": scored_resumes
    }