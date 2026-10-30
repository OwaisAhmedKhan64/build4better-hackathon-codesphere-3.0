import logging
from typing import Optional
from supabase import create_client, Client
from app.core.config import settings

logger = logging.getLogger("uvicorn")

supabase: Optional[Client] = None

if settings.SUPABASE_URL and settings.SUPABASE_SECRET_KEY:
    try:
        supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_SECRET_KEY)
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {e}")
else:
    logger.warning(
        "SUPABASE_URL or SUPABASE_SECRET_KEY is missing. "
        "Database endpoints will return an error until configured in .env."
    )

def get_supabase() -> Client:
    if supabase is None:
        raise RuntimeError("Supabase is not configured. Please set SUPABASE_URL and SUPABASE_SECRET_KEY in .env.")
    return supabase