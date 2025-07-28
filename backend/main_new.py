# main.py (punto de entrada principal)
import uvicorn
from app.main import app
from app.core.config import settings
from app.core.logging import logger

if __name__ == "__main__":
    logger.info(f"🚀 Iniciando {settings.PROJECT_NAME}...")
    logger.info(f"🌐 Servidor ejecutándose en http://{settings.HOST}:{settings.PORT}")
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,  # Solo para desarrollo
        log_level=settings.LOG_LEVEL.lower()
    )
