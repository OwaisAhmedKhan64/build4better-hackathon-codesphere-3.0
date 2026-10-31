
import os
import io
import base64
import tempfile

import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write, read
from dotenv import load_dotenv
from groq import Groq
from mss import mss
from PIL import Image


# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

AUDIO_DURATION = 7
SAMPLE_RATE = 16000

VISION_MODEL = "qwen/qwen3.8-27b"
STT_MODEL = "whisper-large-v3-turbo"
TTS_MODEL = "canopylabs/orpheus-v1-english"

ENABLE_TTS = True
TTS_VOICE = "troy"


# --------------------------------------------------
# INITIALIZE GROQ
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY not found. Check your .env file."
    )

client = Groq(api_key=api_key)


# --------------------------------------------------
# RECORD USER VOICE
# No permanent voice.wav file is created.
# --------------------------------------------------

def record_voice():

    print("\nSpeak now. Describe your problem...")

    audio = sd.rec(
        int(AUDIO_DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    if audio.size == 0:
        raise ValueError("No audio was recorded.")

    if np.max(np.abs(audio)) == 0:
        raise ValueError(
            "Recording is silent. Check your microphone."
        )

    # Store WAV audio temporarily in memory
    audio_buffer = io.BytesIO()

    write(
        audio_buffer,
        SAMPLE_RATE,
        audio
    )

    audio_buffer.seek(0)

    print("Voice recorded successfully.")

    return audio_buffer


# --------------------------------------------------
# CONVERT VOICE TO TEXT USING WHISPER
# --------------------------------------------------

def voice_to_text(audio_buffer):

    print("\nTranscribing your voice...")

    result = client.audio.transcriptions.create(
        file=("recording.wav", audio_buffer.read()),
        model=STT_MODEL,
        response_format="json"
    )

    text = result.text.strip()

    print("\nYou said:")
    print(text)

    if not text:
        raise ValueError("No speech was detected.")

    return text


# --------------------------------------------------
# CAPTURE COMPUTER SCREEN
# --------------------------------------------------

def capture_screen():

    print("\nCapturing your screen...")

    with mss() as screenshot:

        monitor = screenshot.monitors[1]

        image = screenshot.grab(monitor)

        screen_image = Image.frombytes(
            "RGB",
            image.size,
            image.rgb
        )

    # Resize large screenshots
    screen_image.thumbnail((1600, 1600))

    # Compress screenshot in memory
    image_buffer = io.BytesIO()

    screen_image.save(
        image_buffer,
        format="JPEG",
        quality=80
    )

    image_buffer.seek(0)

    encoded_image = base64.b64encode(
        image_buffer.read()
    ).decode("utf-8")

    print("Screen captured successfully.")

    return encoded_image


# --------------------------------------------------
# AI REASONING: VOICE + SCREEN
# --------------------------------------------------

def analyze_problem(user_text, screen_image):

    print("\nAI is analyzing your problem and screen...")

    response = client.chat.completions.create(

        model=VISION_MODEL,

        messages=[
            {
                "role": "system",

                "content": """
You are a sober, direct, and objective computer support assistant.

You receive:
1. The user's spoken problem, converted into text.
2. A screenshot of the user's current screen.

Core Instructions:
1. First, explicitly state whether there is an error or blocker shown on the screen (e.g. "There is an error on screen: ..." or "There is no error on your screen.").
2. Give clear, direct, and concise step-by-step instructions (maximum 1 or 2 steps).
3. Maintain a sober, calm, professional tone with zero unnecessary fluff or emotional language.
4. If a suspicious link, scam, or phishing attempt is visible, alert the user directly.
5. Keep your response concise (2 to 3 sentences maximum).
"""
            },

            {
                "role": "user",

                "content": [

                    {
                        "type": "text",

                        "text": (
                            "Here is my problem:\n"
                            + user_text
                            + "\n\nPlease inspect my current "
                            "screen and help me solve it."
                        )
                    },

                    {
                        "type": "image_url",

                        "image_url": {
                            "url": (
                                "data:image/jpeg;base64,"
                                + screen_image
                            )
                        }
                    }
                ]
            }
        ],

        temperature=0.4,

        max_completion_tokens=1200
    )

    answer = response.choices[0].message.content

    print("\nAI SUPPORT ASSISTANT:")
    print("----------------------------------")
    print(answer)
    print("----------------------------------")

    return answer


# --------------------------------------------------
# SPEAK AI RESPONSE USING ORPHEUS TTS
# --------------------------------------------------


def speak_response(text):

    if not ENABLE_TTS:
        return

    print("\nGenerating spoken response...")

    # Limit speech to approximately 450 characters
    text = text[:450]

    temp_path = None

    try:

        response = client.audio.speech.create(
            model=TTS_MODEL,
            voice=TTS_VOICE,
            input=text,
            response_format="wav"
        )

        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        ) as temp_file:

            temp_path = temp_file.name

        response.write_to_file(temp_path)

        sample_rate, audio_data = read(temp_path)

        sd.play(audio_data, sample_rate)
        sd.wait()

        print("Finished speaking.")

    except Exception as error:

        print("Speech generation failed:", error)
        print("You can still read the AI response above.")

    finally:

        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

# --------------------------------------------------
# MAIN AGENT
# --------------------------------------------------

def main():

    print("\n====================================")
    print("      AI SCREEN VOICE ASSISTANT")
    print("====================================")

    print("\nPress ENTER to start a new session.")
    print("Type q and press ENTER to quit.")

    while True:

        command = input("\nReady? ")

        if command.lower() == "q":
            print("Assistant stopped.")
            break

        try:

            # Step 1: Record user voice
            audio = record_voice()

            # Step 2: Convert voice to text
            user_text = voice_to_text(audio)

            # Step 3: Capture current screen
            screen_image = capture_screen()

            # Step 4: Analyze voice and screen together
            answer = analyze_problem(
                user_text,
                screen_image
            )

            # Step 5: Speak the answer
            speak_response(answer)
        except Exception as error:

            print("\nERROR TYPE:", type(error).__name__)
            print("ERROR DETAILS:", repr(error))

    import traceback
    traceback.print_exc()

    print("\nPlease check the error above.")


# --------------------------------------------------
# START PROGRAM
# --------------------------------------------------

if __name__ == "__main__":
    main()
