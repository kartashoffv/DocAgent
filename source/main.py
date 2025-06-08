from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn
from source.api.api import api_router
from source.config import config
from source.utils.logger_settings import setup_logger


app = FastAPI(
    title=config.PROJECT_NAME,
    openapi_url=f"{config.API_V1_STR}/openapi.json",
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix=config.API_V1_STR)
if __name__ == "__main__":
    LOG_CONFIG = setup_logger()
    uvicorn.run("source.main:app",
                host="0.0.0.0",
                port=config.API_PORT,
                log_config=LOG_CONFIG,
                reload=config.IS_DEBUG)
