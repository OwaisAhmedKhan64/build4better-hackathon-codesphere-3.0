import io
import base64
import asyncio
import edge_tts

# Primary Voices
VOICES = {
    "ur": "ur-PK-UzmaNeural",
    "en": "en-US-JennyNeural",
}

# Fallback Voices (alternate Microsoft edge neural voices)
FALLBACK_VOICES = {
    "ur": "ur-PK-AsadNeural",
    "en": "en-US-GuyNeural",
}


async def synthesize_speech_bytes(text: str, language: str = "ur", max_retries: int = 3) -> bytes:
    """
    Synthesize text into speech using edge-tts with automatic retry logic
    to recover from transient 'connection forcibly closed' socket resets.
    """
    if not text or not text.strip():
        return b""

    clean_text = text.strip()[:600]
    primary_voice = VOICES.get(language, VOICES["ur"])
    fallback_voice = FALLBACK_VOICES.get(language, primary_voice)

    last_error = None

    for attempt in range(1, max_retries + 1):
        # Rotate voice on later attempts if remote host dropped connection
        voice_to_use = primary_voice if attempt < max_retries else fallback_voice
        try:
            communicate = edge_tts.Communicate(clean_text, voice=voice_to_use)
            audio_buffer = io.BytesIO()

            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_buffer.write(chunk["data"])

            audio_data = audio_buffer.getvalue()
            if audio_data and len(audio_data) > 0:
                return audio_data

        except Exception as e:
            last_error = e
            print(f"[WARN] TTS attempt {attempt}/{max_retries} failed ({e}). Retrying in {attempt * 0.5}s...")
            await asyncio.sleep(attempt * 0.5)

    # Secondary Fallback: If gTTS is installed, use Google Translate TTS
    try:
        from gtts import gTTS
        print("[INFO] Edge-TTS dropped connection; falling back to gTTS...")
        gtts_lang = "ur" if language == "ur" else "en"
        buf = io.BytesIO()
        tts = gTTS(text=clean_text, lang=gtts_lang)
        tts.write_to_fp(buf)
        return buf.getvalue()
    except ImportError:
        pass
    except Exception as gtts_err:
        print(f"[ERROR] gTTS fallback failed: {gtts_err}")

    raise RuntimeError(
        f"Speech synthesis failed after {max_retries} attempts: {str(last_error)}"
    )


async def synthesize_speech_base64(text: str, language: str = "ur") -> str:
    """
    Synthesize text into speech and return a base64 Data URL.
    Returns format: "data:audio/mp3;base64,..."
    """
    audio_bytes = await synthesize_speech_bytes(text, language)
    if not audio_bytes:
        return ""
    b64_audio = base64.b64encode(audio_bytes).decode("utf-8")
    return f"data:audio/mp3;base64,{b64_audio}"
