from fastapi import FastAPI
import uvicorn

import logging
from core.logging import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI(title="RistoApp Backend", version="1.0.0")

def main():
    logger.info("Starting the RistoApp backend application...")
    
if __name__ == "__main__":
    main()