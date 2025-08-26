import os
from typing import List, Dict
from langchain_openai import AzureChatOpenAI
from ..logger import setup_application_logger

logger = setup_application_logger(__name__)


# ===============================
# Azure OpenAI Model Functions
# ===============================

async def call_azure_openai_model(model_name: str=None,
                     messages: List[Dict]=None,
                     temperature: float = 0.0,
                     **kwargs
                     ):
    try:
        logger.info("Initializing Azure OpenAI model call")
        model_name = model_name or os.environ.get("AZURE_OPENAI_DEPLOYMENT")
        if not model_name:
            logger.error("Model deployment name not provided")
            raise ValueError("Model deployment name not provided")
        if not messages:
            logger.error("Empty messages provided to model")
            raise ValueError("Messages cannot be empty")
            
        api_key = os.environ.get("AZURE_OPENAI_KEY")
        api_version = os.environ.get("AZURE_OPENAI_API_VERSION")
        endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        
        if not all([api_key, api_version, endpoint]):
            logger.error("Missing required Azure OpenAI configuration")
            raise ValueError("Missing required Azure OpenAI configuration")

        logger.info(f"Creating LLM instance with model: {model_name}")
        llm = AzureChatOpenAI(
            azure_deployment=model_name,
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=endpoint,
            temperature=temperature if "gpt-5" not in model_name else None,
            reasoning_effort="minimal" if "gpt-5" in model_name else None
        )
        
        if "tools" in kwargs:
            logger.info("Binding tools to LLM")
            llm = llm.bind_tools(kwargs["tools"])
        if "structured_output" in kwargs:
            logger.info("Setting up structured output")
            llm = llm.with_structured_output(kwargs["structured_output"])

        logger.info("Invoking LLM")
        response = await llm.ainvoke(messages)
        logger.info("LLM call completed successfully")
        return response
    except Exception as e:
        logger.error(f"Azure OpenAI API call failed: {str(e)}")
        raise Exception(f"Azure OpenAI API call failed: {str(e)}")
