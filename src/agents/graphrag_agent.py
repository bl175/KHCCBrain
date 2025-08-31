import os
import asyncio
import glob
from lightrag import LightRAG, QueryParam
from lightrag.utils import EmbeddingFunc
import numpy as np
from dotenv import load_dotenv
from openai import AzureOpenAI
from lightrag.kg.shared_storage import initialize_pipeline_status
from datetime import datetime
import nest_asyncio
from ..logger import setup_application_logger
from ..utils.doc_utils import extract_pdf_with_mistral_ocr

nest_asyncio.apply()
load_dotenv()

logger = setup_application_logger(__name__)


# ===============================
# Configuration
# ===============================

WORKING_DIR = "./policies"
if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)
    logger.info(f"Created working directory: {WORKING_DIR}")


# ===============================
# Azure OpenAI Functions
# ===============================

async def azure_openai_llm_generation(
    prompt, system_prompt=None, history_messages=[], keyword_extraction=False, **kwargs
) -> str:
    try:
        api_key = os.environ.get("AZURE_OPENAI_API_KEY")
        api_version = os.environ.get("AZURE_OPENAI_API_VERSION")
        endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT")
        
        if not all([api_key, api_version, endpoint, deployment]):
            raise ValueError("Missing required Azure OpenAI environment variables")
        
        client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=endpoint,
        )
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        if history_messages:
            messages.extend(history_messages)
        messages.append({"role": "user", "content": prompt})
        
        chat_completion = client.chat.completions.create(
            model=deployment,
            messages=messages,
            temperature=kwargs.get("temperature", 0) if "gpt-5" not in deployment else 1,
            top_p=kwargs.get("top_p", 1),
            n=kwargs.get("n", 1),
            # reasoning_effort="minimal" if "gpt-5" in deployment else None
        )
        
        result = chat_completion.choices[0].message.content
        logger.debug(f"LLM response generated successfully")
        return result
        
    except Exception as e:
        logger.error(f"Error in LLM model function: {str(e)}")
        raise


async def azure_openai_embedding_generation(texts: list[str]) -> np.ndarray:
    try:
        api_key = os.environ.get("AZURE_OPENAI_API_KEY")
        api_version = os.environ.get("AZURE_EMBEDDING_API_VERSION")
        endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        deployment = os.environ.get("AZURE_EMBEDDING_DEPLOYMENT")
        
        if not all([api_key, api_version, endpoint, deployment]):
            raise ValueError("Missing required Azure OpenAI embedding environment variables")
        
        client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=endpoint,
        )
        
        embedding = client.embeddings.create(
            model=deployment, 
            input=texts
        )
        
        embeddings = [item.embedding for item in embedding.data]
        logger.debug(f"Generated embeddings for {len(texts)} texts")
        return np.array(embeddings)
        
    except Exception as e:
        logger.error(f"Error in embedding function: {str(e)}")
        raise


# ===============================
# RAG Initialization
# ===============================

async def initialize_graphrag_with_postgresql():
    try:
        logger.info("Initializing LightRAG")
        
        embedding_dim = os.environ.get("AZURE_EMBEDDING_DIMENSION")
        if not embedding_dim:
            raise ValueError("Missing AZURE_EMBEDDING_DIMENSION environment variable")
        
        rag = LightRAG(
            working_dir=WORKING_DIR,
            llm_model_func=azure_openai_llm_generation,
            embedding_func=EmbeddingFunc(
                embedding_dim=int(embedding_dim),
                max_token_size=8192,
                func=azure_openai_embedding_generation,
            ),
            kv_storage="PGKVStorage",
            vector_storage="PGVectorStorage", 
            graph_storage="PGGraphStorage",
            doc_status_storage="PGDocStatusStorage",
        )
        
        await rag.initialize_storages()
        await initialize_pipeline_status()
        
        logger.info("RAG initialization completed successfully")
        return rag
        
    except Exception as e:
        logger.error(f"Error initializing RAG: {str(e)}")
        raise


# ===============================
# Document Processing Functions
# ===============================

async def insert_pdf_documents_to_graphrag(rag, directory_path):
   import csv
   
   try:
       logger.info(f"Processing PDF documents from directory: {directory_path}")
       
       if not os.path.exists(directory_path):
           logger.error(f"Directory does not exist: {directory_path}")
           return False
       
       pdf_files = glob.glob(os.path.join(directory_path, "*.pdf"))
       
       if not pdf_files:
           logger.warning(f"No PDF files found in directory: {directory_path}")
           return False
       
       logger.info(f"Found {len(pdf_files)} PDF files to process")
       
       csv_file = "/home/bl175/Desktop/Test/policies/pdf_processing_status.csv"
       csv_exists = os.path.exists(csv_file)
       
       processed_files = set()
       if csv_exists:
           with open(csv_file, "r", newline="") as f:
               reader = csv.DictReader(f)
               for row in reader:
                   if row.get("status") == "success":
                       processed_files.add(row.get("file_name"))
       
       files_to_process = [pdf_file for pdf_file in pdf_files if os.path.basename(pdf_file) not in processed_files]
       
       if not files_to_process:
           logger.info("All PDF files have already been processed successfully")
           return True
       
       logger.info(f"Processing {len(files_to_process)} new PDF files (skipping {len(pdf_files) - len(files_to_process)} already processed)")
       
       successful_insertions = 0
       for pdf_file in files_to_process:
           file_name = os.path.basename(pdf_file)
           formatted_name = os.path.splitext(file_name)[0].replace(" ", "_")
           status = "failed"
           
           try:
               logger.info(f"Processing document: {file_name}")
               
               pdf_content = await extract_pdf_with_mistral_ocr(pdf_file)
               if pdf_content:
                   logger.info(f"Inserting document into RAG: {file_name}")
                   await rag.ainsert([pdf_content], file_paths=[formatted_name])
                   successful_insertions += 1
                   status = "success"
                   logger.info(f"Successfully inserted: {file_name}")
               else:
                   logger.error(f"Failed to extract content from: {file_name}")
                   
           except Exception as e:
               logger.error(f"Error processing {file_name}: {str(e)}")
           
           with open(csv_file, "a", newline="") as f:
               writer = csv.writer(f)
               if not csv_exists:
                   writer.writerow(["file_name", "formatted_name", "status", "timestamp"])
                   csv_exists = True
               writer.writerow([file_name, formatted_name, status, datetime.now().isoformat()])
       
       logger.info(f"Successfully inserted {successful_insertions}/{len(files_to_process)} documents")
       return successful_insertions > 0
       
   except Exception as e:
       logger.error(f"Error processing directory {directory_path}: {str(e)}")
       return False


# ===============================
# Query Functions
# ===============================

async def query_graphrag_with_mode(rag, query_text, mode="hybrid"):
    try:
        logger.info(f"Querying RAG with mode '{mode}': {query_text}")
        
        result = await rag.aquery(query_text, param=QueryParam(mode=mode))
        
        logger.info("Query completed successfully")
        return result
        
    except Exception as e:
        logger.error(f"Error querying RAG: {str(e)}")
        return None