import asyncio
import asyncpg
import os
from dotenv import load_dotenv
from ..logger import setup_application_logger

load_dotenv()
logger = setup_application_logger(__name__)


# ===============================
# Database Connection Configuration
# ===============================

def get_postgresql_connection_params():
    return {
        "host": os.environ.get("POSTGRES_HOST"),
        "port": os.environ.get("POSTGRES_PORT"),
        "user": os.environ.get("POSTGRES_USER"), 
        "password": os.environ.get("POSTGRES_PASSWORD"),
        "database": os.environ.get("POSTGRES_DATABASE"),
        "ssl": os.environ.get("POSTGRES_SSL")
    }


# ===============================
# Table Management Functions
# ===============================

async def clear_all_lightrag_postgresql_tables():
    try:
        connection_params = get_postgresql_connection_params()
        
        tables_to_clear = [
            "LIGHTRAG_DOC_FULL",
            "LIGHTRAG_DOC_CHUNKS", 
            "LIGHTRAG_VDB_CHUNKS",
            "LIGHTRAG_VDB_ENTITY",
            "LIGHTRAG_VDB_RELATION",
            "LIGHTRAG_LLM_CACHE",
            "LIGHTRAG_DOC_STATUS",
            "LIGHTRAG_FULL_ENTITIES",
            "LIGHTRAG_FULL_RELATIONS"
        ]
        
        logger.info("Connecting to database...")
        conn = await asyncpg.connect(**connection_params)
        
        for table in tables_to_clear:
            try:
                logger.info(f"Clearing table: {table}")
                await conn.execute(f"DELETE FROM {table}")
                logger.info(f"Successfully cleared {table}")
            except Exception as e:
                logger.error(f"Failed to clear {table}: {str(e)}")
        
        logger.info("All tables cleared successfully!")
        
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        raise
    finally:
        if 'conn' in locals():
            await conn.close()
            logger.info("Database connection closed")