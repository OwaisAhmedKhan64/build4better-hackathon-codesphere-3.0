from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Body
from app.db import get_supabase
from app.schemas.note import NoteCreate

router = APIRouter(tags=["System & Diagnostics"])

@router.get("/health")
@router.get("/api/system/health")
def health_check():
    """Simple liveness probe for monitoring and deployments."""
    return {"status": "ok"}

@router.get("/test-db")
def test_supabase_read():
    """Verify live read connection to the Supabase 'notes' table."""
    try:
        client = get_supabase()
        response = client.table("notes").select("*").execute()
        return {
            "status": "connected",
            "data": response.data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test-db")
def test_supabase_write(
    title: Optional[str] = Query(None, description="Optional title as query parameter"),
    payload: Optional[NoteCreate] = Body(None, description="Optional note object in request body")
):
    """
    Verify live write connection to the Supabase 'notes' table.
    Supports both query parameter (?title=...) and JSON request body ({"title": "..."}).
    """
    note_title = None
    if payload and payload.title:
        note_title = payload.title
    elif title:
        note_title = title

    if not note_title:
        raise HTTPException(status_code=400, detail="Missing note title in query parameter or request body")

    try:
        client = get_supabase()
        response = client.table("notes").insert({"title": note_title}).execute()
        return {
            "status": "inserted",
            "data": response.data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
