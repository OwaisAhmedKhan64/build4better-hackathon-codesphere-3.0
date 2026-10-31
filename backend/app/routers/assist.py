import base64
import traceback
from typing import Optional
from fastapi import APIRouter, Request, UploadFile, File, Form, Body, HTTPException, status
from pydantic import BaseModel, Field
from app.services.groq_service import transcribe_audio, analyze_screen_and_query
from app.services.tts_service import synthesize_speech_base64

router = APIRouter(prefix="/api/assist", tags=["Assist (Multimodal AI)"])


class AssistJSONPayload(BaseModel):
    image: str = Field(
        ...,
        description="Base64 encoded screen snapshot (raw base64 string or data:image/...;base64,... Data URL)",
        example="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAP..."
    )
    audio: str = Field(
        ...,
        description="Base64 encoded voice recording (raw base64 string or data:audio/...;base64,... Data URL)",
        example="data:audio/mp3;base64,//NkxAAAAANIAAAAAExBTUV..."
    )
    language: str = Field(
        "ur",
        description="Response language: 'ur' for Urdu or 'en' for English",
        example="ur"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "image": "data:image/jpeg;base64,<PASTE_IMAGE_BASE64_HERE>",
                "audio": "data:audio/mp3;base64,<PASTE_AUDIO_BASE64_HERE>",
                "language": "ur"
            }
        }
    }


class AssistResponse(BaseModel):
    status: str = Field("success", example="success")
    transcript: str = Field(..., description="Transcribed spoken user query", example="پاس ورڈ غلط آ رہا ہے")
    ai_response: str = Field(..., description="Sober, direct AI guidance in authentic Urdu script stating error condition", example="اسکرین پر ایرر ہے: پاس ورڈ درست نہیں ہے۔ نیا پاس ورڈ درج کریں۔")
    audio_base64: str = Field(..., description="Base64 encoded MP3 speech audio Data URL", example="data:audio/mp3;base64,//NkxAAAAANIAAAAAExBTUV...")
    has_error: bool = Field(..., description="Whether an error/blocker was detected on screen", example=True)
    is_scam_warning: bool = Field(..., description="Whether a security scam/phishing threat was detected", example=False)
    suggested_action: str = Field(..., description="Concise recommended action", example="Follow voice guidance")


def decode_base64_data(data: str) -> bytes:
    """Decodes base64 string, handling data URL prefix if present."""
    if not data or not isinstance(data, str):
        return b""
    clean_data = data.strip()
    if "," in clean_data:
        clean_data = clean_data.split(",", 1)[1]
    return base64.b64decode(clean_data)


async def execute_assist_pipeline(image_bytes: bytes, audio_bytes: bytes, language: str = "ur") -> dict:
    """Core multimodal processing pipeline."""
    if not image_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty image data received. Please provide a screen capture snapshot."
        )

    if not audio_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty audio data received. Please provide recorded voice audio."
        )

    # 1. Transcribe voice audio via Groq Whisper
    try:
        transcript = transcribe_audio(audio_bytes)
        if not transcript or not transcript.strip():
            transcript = "اسکرین پر مدد چاہیے" if language == "ur" else "Need help on this screen"
    except Exception as e:
        print(f"[WARN] Audio transcription failed ({e}), using default fallback.")
        transcript = "اسکرین پر مدد چاہیے" if language == "ur" else "Need help on this screen"

    # 2. Inspect screen & query with Groq Qwen Vision (Sober Direct Prompt)
    ai_result = analyze_screen_and_query(
        image_bytes=image_bytes,
        user_query=transcript,
        language=language
    )
    ai_response_text = ai_result.get(
        "ai_response",
        "اسکرین پر کوئی خرابی نہیں ہے۔ اگلا قدم دیکھ کر آگے بڑھیں۔" if language == "ur" else "No error on screen. Follow next step."
    )

    # 3. Synthesize spoken guidance via Edge-TTS into base64 Data URL
    try:
        audio_base64 = await synthesize_speech_base64(ai_response_text, language=language)
    except Exception as tts_err:
        print(f"[WARN] TTS synthesis failed: {tts_err}")
        audio_base64 = ""

    return {
        "status": "success",
        "transcript": transcript,
        "ai_response": ai_response_text,
        "audio_base64": audio_base64,
        "has_error": ai_result.get("has_error", False),
        "is_scam_warning": ai_result.get("is_scam_warning", False),
        "suggested_action": ai_result.get("suggested_action", "Follow voice guidance")
    }


@router.post(
    "",
    response_model=AssistResponse,
    status_code=status.HTTP_200_OK,
    summary="Multimodal Assist (JSON Base64 or FormData)",
    description="Main pipeline: Accepts either JSON (base64 image/audio) or Multipart FormData (image/audio blobs). Returns sober guidance, error detection, and synthesized speech."
)
async def assist_endpoint(request: Request):
    """
    Dual-mode handler:
    1. If Content-Type is application/json: decodes base64 image and audio.
    2. If Content-Type is multipart/form-data: reads uploaded image and audio blobs.
    """
    try:
        content_type = request.headers.get("content-type", "")

        if "application/json" in content_type:
            body = await request.json()
            image_raw = body.get("image") or body.get("image_base64") or ""
            audio_raw = body.get("audio") or body.get("audio_base64") or ""
            language = body.get("language") or "ur"

            image_bytes = decode_base64_data(image_raw)
            audio_bytes = decode_base64_data(audio_raw)
        else:
            form = await request.form()
            img_field = form.get("image") or form.get("image_base64")
            aud_field = form.get("audio") or form.get("audio_base64")
            language = str(form.get("language") or "ur")

            if hasattr(img_field, "read"):
                image_bytes = await img_field.read()
            elif isinstance(img_field, str):
                image_bytes = decode_base64_data(img_field)
            else:
                image_bytes = b""

            if hasattr(aud_field, "read"):
                audio_bytes = await aud_field.read()
            elif isinstance(aud_field, str):
                audio_bytes = decode_base64_data(aud_field)
            else:
                audio_bytes = b""

        return await execute_assist_pipeline(image_bytes, audio_bytes, language)
    except HTTPException:
        raise
    except Exception as err:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Assist processing failed: {str(err)}"
        )


@router.post(
    "/upload",
    response_model=AssistResponse,
    status_code=status.HTTP_200_OK,
    summary="Assist with File Upload (Interactive Swagger / Form)",
    description="Easily test in Swagger docs by picking a screenshot file (JPEG/PNG) and an audio file (MP3/WAV/WEBM) directly from your computer."
)
async def assist_upload(
    image: UploadFile = File(..., description="Screen snapshot image (PNG or JPEG)"),
    audio: UploadFile = File(..., description="Spoken voice clip (MP3, WAV, or WEBM)"),
    language: str = Form("ur", description="Response language ('ur' or 'en')")
):
    """Allows uploading raw files directly (convenient for Swagger UI testing)."""
    try:
        image_bytes = await image.read()
        audio_bytes = await audio.read()
        return await execute_assist_pipeline(image_bytes, audio_bytes, language)
    except HTTPException:
        raise
    except Exception as err:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Assist upload processing failed: {str(err)}"
        )
