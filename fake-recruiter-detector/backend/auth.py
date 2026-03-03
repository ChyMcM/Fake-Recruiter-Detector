import os
from typing import Optional

from fastapi import Depends, Header, HTTPException, status


def get_api_key(x_api_key: Optional[str] = Header(None)) -> str:
    """
    Dependency that validates API key from X-API-Key header.
    If AUTH_ENABLED=false, this is bypassed (development mode).
    """
    auth_enabled = os.getenv("AUTH_ENABLED", "true").lower() == "true"
    if not auth_enabled:
        return "development-mode"

    valid_keys = [k.strip() for k in os.getenv("VALID_API_KEYS", "").split(",") if k.strip()]

    if not valid_keys:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server misconfigured: no valid API keys set",
        )

    if not x_api_key or x_api_key not in valid_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return x_api_key
