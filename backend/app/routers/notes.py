from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, status
from app.db import get_supabase
from app.schemas.note import NoteCreate, NoteResponse

router = APIRouter(prefix="/api/notes", tags=["Notes (REST API)"])

@router.get("", response_model=Dict[str, Any])
def list_notes():
    """Retrieve all notes from the database."""
    try:
        client = get_supabase()
        response = client.table("notes").select("*").order("created_at", desc=True).execute()
        return {
            "status": "success",
            "count": len(response.data) if response.data else 0,
            "data": response.data or []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("", status_code=status.HTTP_201_CREATED)
def create_note(payload: NoteCreate):
    """Create a new note with a validated JSON request body."""
    try:
        client = get_supabase()
        response = client.table("notes").insert({"title": payload.title}).execute()
        return {
            "status": "created",
            "data": response.data[0] if response.data else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{note_id}")
def delete_note(note_id: int):
    """Delete a note by ID."""
    try:
        client = get_supabase()
        response = client.table("notes").delete().eq("id", note_id).execute()
        return {
            "status": "deleted",
            "data": response.data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
