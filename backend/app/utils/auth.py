# app/utils/auth.py
from typing import Optional
from app.core.config import settings

def validate_token(token: Optional[str]) -> bool:
    """Valida si el token es válido"""
    if not token:
        return False
    return token in settings.VALID_TOKENS

def validate_client_id(client_id: str) -> bool:
    """Valida que el client_id tenga un formato válido"""
    if not client_id or len(client_id.strip()) == 0:
        return False
    
    # Validaciones adicionales si es necesario
    if len(client_id) > 50:  # Límite de longitud
        return False
        
    return True
