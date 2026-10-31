import os
import io
import base64
from typing import Optional
from PIL import Image
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    # Gracefully warn if key is not yet set
    print("[WARNING] GROQ_API_KEY not found in environment variables.")

client = Groq(api_key=API_KEY) if API_KEY else None

VISION_MODEL = "qwen/qwen3.8-27b"
STT_MODEL = "whisper-large-v3-turbo"


def get_client() -> Groq:
    global client
    if not client:
        key = os.getenv("GROQ_API_KEY")
        if not key:
            raise ValueError("GROQ_API_KEY is missing in your .env file.")
        client = Groq(api_key=key)
    return client


def optimize_image(image_bytes: bytes, max_dimension: int = 800) -> str:
    """
    Downsamples and compresses the image to keep Groq vision token usage low
    and avoid 'Request too big' or TPM rate-limit errors.
    Returns base64 encoded string.
    """
    image = Image.open(io.BytesIO(image_bytes))
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Resize so largest side is max_dimension (preserves aspect ratio)
    image.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)

    output_buffer = io.BytesIO()
    # Quality 70 keeps image sharp for OCR while drastically shrinking base64 payload
    image.save(output_buffer, format="JPEG", quality=70, optimize=True)
    output_buffer.seek(0)

    return base64.b64encode(output_buffer.read()).decode("utf-8")


def detect_audio_filename(audio_bytes: bytes, default: str = "recording.webm") -> str:
    """Detects audio container format from header magic bytes."""
    if not audio_bytes:
        return default
    if audio_bytes.startswith(b"\x1a\x45\xdf\xa3"):
        return "recording.webm"
    elif audio_bytes.startswith(b"RIFF"):
        return "recording.wav"
    elif audio_bytes.startswith(b"ID3") or audio_bytes[:2] in (b"\xff\xfb", b"\xff\xf3", b"\xff\xf2"):
        return "recording.mp3"
    elif b"ftyp" in audio_bytes[:16]:
        return "recording.mp4"
    return default


def transcribe_audio(audio_bytes: bytes, filename: Optional[str] = None) -> str:
    """
    Transcribes spoken voice audio using Groq Whisper.
    Automatically detects audio container (webm, wav, mp3, mp4) from payload bytes.
    """
    groq_client = get_client()

    if not filename or filename == "recording.wav":
        filename = detect_audio_filename(audio_bytes)

    # Whisper expects a tuple: (filename, bytes_data)
    result = groq_client.audio.transcriptions.create(
        file=(filename, audio_bytes),
        model=STT_MODEL,
        response_format="json",
        language=None  # Auto-detect Urdu or English
    )
    return result.text.strip() if hasattr(result, "text") else str(result).strip()


def analyze_screen_and_query(image_bytes: bytes, user_query: str, language: str = "ur") -> dict:
    """
    Analyzes the screen frame alongside the user's spoken confusion.
    Outputs simplified step-by-step guidance in Urdu or English.
    """
    groq_client = get_client()

    # 1. Optimize image to prevent 'Request too big' token limit errors
    optimized_b64 = optimize_image(image_bytes, max_dimension=800)

    # 2. Sober, direct technical assistant system prompt
    if language == "ur":
        system_prompt = """
آپ ایک سنجیدہ، بااصول اور براہِ راست رہنمائی کرنے والے ڈیجیٹل ٹیکنیکل اسسٹنٹ ہیں۔ آپ صارف کی اسکرین اور ان کا سوال دیکھ کر سیدھا اصل مدعے پر آتے ہیں۔

انتہائی اہم ہدایت:
آپ کا پورا جواب لازماً اصل اور خالص اردو رسم الخط (اردو فونٹ / حروفِ تہجی) میں ہونا چاہیے۔ رومن اردو یا انگریزی رسم الخط بالکل استعمال نہ کریں۔

قواعد:
1۔ سب سے پہلے صاف اور واضح الفاظ میں بتائیں کہ اسکرین پر کوئی ایرر یا خرابی موجود ہے یا نہیں:
   - اگر اسکرین پر کوئی خرابی، وارننگ یا رکاوٹ موجود ہے: تو سیدھا بتائیں کہ کیا ایرر ہے (مثلاً: "اسکرین پر ایرر ہے: پاس ورڈ درست نہیں ہے۔" یا "اسکرین پر سیشن ٹائم آؤٹ کا ایرر ہے")۔
   - اگر اسکرین پر کوئی ایرر نہیں ہے: تو واضح بتائیں (مثلاً: "اسکرین پر کوئی خرابی یا ایرر نہیں ہے، سب ٹھیک ہے۔")۔
2۔ اس کے بعد فوراً اگلا سیدھا اور آسان قدم بتائیں (زیادہ سے زیادہ 1 یا 2 واضح اقدامات)۔
3۔ اندازِ گفتگو سنجیدہ، باوقار اور دو ٹوک رکھیں۔ کوئی فالتو، جذباتی یا غیر ضروری بات نہ کریں۔ پیچیدہ تکنیکی الفاظ سے پرہیز کریں۔
4۔ اگر اسکرین پر کوئی فراڈ، دھوکہ دہی، جعلی انعام یا مشکوک لنک نظر آئے، تو فوراً خبردار کریں: "یہ مشکوک لنک ہے، اس پر کلک نہ کریں۔"
5۔ جواب مختصر اور جامع رکھیں (زیادہ سے زیادہ 2 سے 3 جملے)۔
"""
    else:
        system_prompt = """
You are a sober, direct, and objective digital technical assistant. You inspect the user's screen snapshot and listen to their query, getting straight to the point.

Core Instructions:
1. First, explicitly state whether there is an error or issue present on the screen:
   - If an error, warning, or blocker is visible: Clearly state the error (e.g., "There is an error on screen: Incorrect password" or "A session timeout error is displayed").
   - If no error is present: State it directly (e.g., "There is no error on your screen. The form is ready to submit").
2. Next, provide direct, concrete next action(s) (maximum 1 or 2 clear steps).
3. Maintain a sober, calm, professional, and concise tone. Avoid unnecessary fluff or emotional padding. Avoid complex technical jargon.
4. If a scam, fake alert, phishing message, or suspicious link is visible, directly state: "This appears to be a suspicious link/scam, do not click it."
5. Keep your total response concise (2 to 3 sentences maximum).
"""

    user_text_prompt = (
        f"صارف کا سوال: {user_query}\nبراہ کرم اسکرین شاٹ کا معائنہ کریں۔ سب سے پہلے بتائیں کہ کیا اسکرین پر کوئی ایرر ہے، پھر اصل اردو رسم الخط میں مرحلہ وار رہنمائی کریں۔"
        if language == "ur"
        else f"User's Question: {user_query}\nPlease inspect the current screen snapshot. First state if there is an error, then provide direct step-by-step guidance."
    )

    messages = [
        {"role": "system", "content": system_prompt.strip()},
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": user_text_prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{optimized_b64}"
                    }
                }
            ]
        }
    ]

    try:
        response = groq_client.chat.completions.create(
            model=VISION_MODEL,
            messages=messages,
            temperature=0.2,
            max_completion_tokens=400
        )
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[WARN] Vision model {VISION_MODEL} call failed: {e}. Retrying with compressed payload...")
        # Retry with lower resolution thumbnail if token payload was too large
        compressed_b64 = optimize_image(image_bytes, max_dimension=600)
        messages[1]["content"][1]["image_url"]["url"] = f"data:image/jpeg;base64,{compressed_b64}"
        response = groq_client.chat.completions.create(
            model=VISION_MODEL,
            messages=messages,
            temperature=0.2,
            max_completion_tokens=300
        )
        answer = response.choices[0].message.content.strip()

    # Heuristic to detect if screen contains an error (supports both native Urdu script and English)
    lower_ans = answer.lower()
    has_error = (
        # Native Urdu error markers
        ("ایرر ہے" in answer or "خرابی ہے" in answer or "مسئلہ ہے" in answer or "غلط ہے" in answer or "ناکام" in answer) or
        # English / Roman error markers
        (("error" in lower_ans and "koi error nahi" not in lower_ans and "no error" not in lower_ans and "not an error" not in lower_ans) or
         ("masla hai" in lower_ans and "koi masla nahi" not in lower_ans) or
         ("galat" in lower_ans or "ghalat" in lower_ans) or
         ("failed" in lower_ans or "failure" in lower_ans))
    )
    if any(neg in answer for neg in ["کوئی ایرر نہیں", "کوئی خرابی نہیں", "کوئی مسئلہ نہیں", "سب ٹھیک ہے"]):
        has_error = False

    # Heuristic to detect if security warning was triggered
    is_scam = (
        any(w in answer for w in ["دھوکہ", "مشکوک", "فراڈ", "جعلی", "کلک نہ کریں", "ٹیپ نہ کریں"]) or
        any(w in lower_ans for w in ["scam", "dhoka", "mashkook", "fraud", "phishing", "suspicious", "fake link", "mat tap", "na karein"])
    )

    return {
        "ai_response": answer,
        "has_error": has_error,
        "is_scam_warning": is_scam,
        "suggested_action": "Follow voice guidance"
    }
