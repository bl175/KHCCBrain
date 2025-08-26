import base64
import os
import aiofiles
from mistralai import Mistral
from ..logger import setup_application_logger

logger = setup_application_logger(__name__)


# ===============================
# PDF Encoding Functions
# ===============================

async def encode_pdf_to_base64(pdf_path):
    try:
        async with aiofiles.open(pdf_path, "rb") as pdf_file:
            content = await pdf_file.read()
            encoded = base64.b64encode(content).decode('utf-8')
            logger.info(f"Successfully encoded PDF: {pdf_path}")
            return encoded
    except FileNotFoundError:
        logger.error(f"PDF file not found: {pdf_path}")
        return None
    except Exception as e:
        logger.error(f"Error encoding PDF {pdf_path}: {str(e)}")
        return None


# ===============================
# OCR Processing Functions
# ===============================

async def extract_pdf_with_mistral_ocr(pdf_path):
    try:
        logger.info(f"Starting OCR processing for: {pdf_path}")
        
        base64_pdf = await encode_pdf_to_base64(pdf_path)
        if not base64_pdf:
            return None
        
        api_key = os.environ.get("MISTRAL_API_KEY")
        if not api_key:
            logger.error("MISTRAL_API_KEY environment variable not found")
            return None
        
        client = Mistral(api_key=api_key)
        
        ocr_response = client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": f"data:application/pdf;base64,{base64_pdf}" 
            },
            include_image_base64=True
        )
        
        pdf_content = ""
        for i, page in enumerate(ocr_response.pages):
            pdf_content += page.markdown
            logger.debug(f"Processed page {i + 1}")
        
        logger.info(f"Successfully extracted content from {len(ocr_response.pages)} pages")
        return pdf_content
        
    except Exception as e:
        logger.error(f"Error processing PDF {pdf_path}: {str(e)}")
        return None