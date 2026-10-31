from fastapi import APIRouter, HTTPException, Query, Response, status
from pydantic import BaseModel, Field
from app.services.tts_service import synthesize_speech_bytes

router = APIRouter(prefix="/api/tts", tags=["TTS (Text to Speech)"])

class TTSRequest(BaseModel):
    text: str = Field(..., description="Text to be converted to speech", min_length=1)
    language: str = Field("ur", description="Response language: 'ur' for Urdu or 'en' for English")

@router.post("", status_code=status.HTTP_200_OK)
async def text_to_speech_post(payload: TTSRequest):
    """
    Convert text into natural spoken audio via POST request.
    Returns raw streaming MP3 audio (audio/mpeg).
    """
    try:
        audio_bytes = await synthesize_speech_bytes(payload.text, payload.language)
        if not audio_bytes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to generate speech from provided text."
            )
        return Response(
            content=audio_bytes,
            media_type="audio/mpeg",
            headers={"Content-Disposition": "inline; filename=speech.mp3"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Speech synthesis failed: {str(e)}"
        )

@router.get("", status_code=status.HTTP_200_OK)
async def text_to_speech_get(
    text: str = Query(..., description="Text to speak", min_length=1),
    language: str = Query("ur", description="Language: 'ur' or 'en'")
):
    """
    Convert text into natural spoken audio via GET request.
    Allows direct playback in browser or HTML5 <audio src="..."> element.
    """
    try:
        audio_bytes = await synthesize_speech_bytes(text, language)
        if not audio_bytes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to generate speech from provided text."
            )
        return Response(
            content=audio_bytes,
            media_type="audio/mpeg",
            headers={"Content-Disposition": "inline; filename=speech.mp3"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Speech synthesis failed: {str(e)}"
        )
