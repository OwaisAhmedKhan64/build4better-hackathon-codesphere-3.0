import io
import sys
import base64
import asyncio
from PIL import Image, ImageDraw, ImageFont
from starlette.testclient import TestClient
from app.main import app

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def generate_test_screen(has_error_text: bool = True) -> str:
    """Generates a sample screen image as base64 string."""
    img = Image.new("RGB", (800, 600), color=(30, 30, 40))
    draw = ImageDraw.Draw(img)
    
    # Draw simulated UI
    draw.rectangle([50, 50, 750, 100], fill=(50, 50, 70))
    draw.text((70, 70), "Login Portal - Black Mesa", fill=(255, 255, 255))
    
    if has_error_text:
        # Draw error banner
        draw.rectangle([100, 150, 700, 230], fill=(180, 40, 40))
        draw.text((120, 180), "ERROR: Invalid username or password. Please try again.", fill=(255, 255, 255))
        draw.text((120, 260), "Please enter your registered email address.", fill=(200, 200, 200))
    else:
        # Draw normal screen
        draw.rectangle([100, 150, 700, 230], fill=(40, 140, 60))
        draw.text((120, 180), "Welcome back! Please enter your password to continue.", fill=(255, 255, 255))
        draw.text((120, 260), "Click 'Login' to proceed to your dashboard.", fill=(200, 200, 200))

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=80)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


def get_sample_audio_base64() -> str:
    """Loads existing test_speech.mp3 or generates small wav."""
    try:
        with open("test_speech.mp3", "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode("utf-8")
    except Exception:
        # fallback minimal dummy audio
        return base64.b64encode(b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00D\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00").decode("utf-8")


def run_tests():
    client = TestClient(app)
    
    print("\n--- Test 1: Testing Health Endpoint ---")
    res = client.get("/api/system/health")
    print("Health Status:", res.status_code, res.json())
    assert res.status_code == 200

    print("\n--- Test 2: Testing /api/assist (Urdu, Screen with Error) ---")
    img_b64 = generate_test_screen(has_error_text=True)
    aud_b64 = get_sample_audio_base64()

    payload = {
        "image": f"data:image/jpeg;base64,{img_b64}",
        "audio": f"data:audio/mp3;base64,{aud_b64}",
        "language": "ur"
    }

    res = client.post("/api/assist", json=payload)
    print("Status Code:", res.status_code)
    data = res.json()
    print("Transcript:", data.get("transcript"))
    print("AI Response:", data.get("ai_response"))
    print("Has Error Detected:", data.get("has_error"))
    print("Is Scam Warning:", data.get("is_scam_warning"))
    print("Audio Base64 prefix:", (data.get("audio_base64") or "")[:45])
    print("Audio Base64 length:", len(data.get("audio_base64") or ""))

    assert res.status_code == 200
    assert "status" in data and data["status"] == "success"
    assert "audio_base64" in data and len(data["audio_base64"]) > 50
    assert "ai_response" in data and len(data["ai_response"]) > 0

    print("\n--- Test 3: Testing /api/assist (English, Screen without Error) ---")
    img_normal_b64 = generate_test_screen(has_error_text=False)
    payload_en = {
        "image": img_normal_b64,
        "audio": aud_b64,
        "language": "en"
    }
    res_en = client.post("/api/assist", json=payload_en)
    print("Status Code:", res_en.status_code)
    data_en = res_en.json()
    print("Transcript (EN):", data_en.get("transcript"))
    print("AI Response (EN):", data_en.get("ai_response"))
    print("Has Error Detected (EN):", data_en.get("has_error"))
    print("Audio Base64 length (EN):", len(data_en.get("audio_base64") or ""))

    assert res_en.status_code == 200
    assert "audio_base64" in data_en and len(data_en["audio_base64"]) > 50

    print("\n--- Test 4: Testing /api/assist (Multipart Form-Data File Upload) ---")
    img_raw_bytes = base64.b64decode(img_b64)
    aud_raw_bytes = base64.b64decode(aud_b64)

    files = {
        "image": ("screenshot.jpg", img_raw_bytes, "image/jpeg"),
        "audio": ("voice.mp3", aud_raw_bytes, "audio/mpeg"),
    }
    data_form = {"language": "ur"}
    res_form = client.post("/api/assist/upload", files=files, data=data_form)
    print("Status Code (Multipart):", res_form.status_code)
    data_res_form = res_form.json()
    print("AI Response (Multipart):", data_res_form.get("ai_response"))
    print("Audio Base64 Length (Multipart):", len(data_res_form.get("audio_base64") or ""))
    assert res_form.status_code == 200
    assert "audio_base64" in data_res_form and len(data_res_form["audio_base64"]) > 50

    print("\n>>> ALL TESTS PASSED SUCCESSFULLY! <<<")


if __name__ == "__main__":
    run_tests()
