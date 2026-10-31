# AGENTS.md — [Name not Finalized] Project Guide

> **Build4Better Hackathon | CodeSphere 3.0**  
> **Organised by:** Department of Software Engineering, NED University of Engineering and Technology  
> **Team:** Black Mesa (Owais Ahmed Khan, Barira Waris, Naveed Zahir)  
> **Build Window:** Saturday, 31 October 2026 (9:00 AM – 5:00 PM PKT)

---

## 1. Project Overview & Hackathon Purpose

### The Problem
Technology is built for digital natives, leaving parents, grandparents, and non-tech-savvy adults feeling intimidated, anxious, and dependent. Common roadblocks like confusing forms, unexpected session logouts, verification OTPs, or scam messages make them afraid of breaking their devices or losing money. When stuck, they panic or quietly avoid essential digital tools.

### The Solution: [Name not Finalized] (MVP Focus)
**[Name not Finalized]** is a real-time, voice-and-screen AI digital companion designed specifically for non-tech-native users.
* Instead of doing tasks *for* them (which teaches nothing), [Name not Finalized] **sees what they see on screen** and **listens to their spoken confusion**.
* [Name not Finalized] responds with **warm, patient, conversational speech in Urdu (or simple English)**, guiding them step-by-step on where to click, explaining why an error happened, reassuring them that their device is safe, and warning them of scams.
* **MVP Philosophy:** 100% focused on the live real-time interaction loop. No database overhead or sign-ins are required, ensuring zero friction, privacy-first assistance, and lightning-fast execution.

---

## 2. Technology Stack (Lean MVP)

### Frontend (`frontend/`)
* **Framework:** Vue 3 (Composition API `<script setup lang="ts">`)
* **Build Tool:** Vite + TypeScript
* **Styling:** Tailwind CSS v4 (vanilla CSS tokens, clean modern aesthetics)
* **State Management:** Pinia
* **Routing:** Vue Router
* **Media & Browser APIs:**
  * `navigator.mediaDevices.getDisplayMedia` — screen video stream capture.
  * `navigator.mediaDevices.getUserMedia` / `MediaRecorder` — microphone audio capture.
  * `<canvas>` API — on-demand snapshot frame extraction.
  * HTML5 Audio (`new Audio()`) — instant playback of synthesized speech.

### Backend (`backend/`)
* **Framework:** FastAPI (Python 3.12.7) — stateless, high-performance async backend.
* **Server:** Uvicorn
* **AI & Speech Engine:**
  * **Groq API:**
    * Vision & Multimodal Reasoning: `qwen/qwen3.8-27b` (fallback: `llama-3.2-11b-vision-preview`).
    * Speech-to-Text (STT): `whisper-large-v3` on Groq.
  * **Text-to-Speech (TTS):** `edge-tts` (voices: `ur-PK-UzmaNeural` for Urdu, `en-US-JennyNeural` for English).

---

## 3. End-to-End System Architecture

```text
[User Screen Stream] ────────────────┐
                                     │ (When user speaks or taps mic)
[User Microphone] ──(Audio Blob)───► [Vue.js Single-Page Frontend]
                                     │ 
                                     │ Extracts 1 sharp frame from <canvas>
                                     ▼
                        POST /api/assist (FastAPI)
                                     │
           ┌─────────────────────────┴────────────────────────┐
           ▼                                                  ▼
1. Groq Whisper API (STT)                        2. Groq Qwen3.8-27b (Vision)
   Audio -> Transcribed Question                    Screen Frame + User Question
           │                                                  │
           └─────────────────────────┬────────────────────────┘
                                     ▼
                            3. AI Explanation & Guidance
                               (Empathetic Urdu Persona)
                                     │
                                     ▼
                            4. Edge-TTS Synthesis
                               Generates warm MP3 audio
                               (ur-PK-UzmaNeural / en-US-JennyNeural)
                                     │
                                     ▼
                   [FastAPI Returns JSON with Audio Data URL]
                                     │
                                     ▼
                 [Vue.js Auto-Plays Voice Guidance + Shows Captions]
```

---

## 4. API Specifications

All endpoints are hosted on the FastAPI backend under `/api`.

### 1. `POST /api/assist`
* **Description:** Main multimodal processing pipeline. Accepts a screen snapshot frame and the user's voice audio, performs speech recognition and visual reasoning via Groq, synthesizes spoken advice via Edge-TTS, and returns the audio and captions.
* **Content-Type:** `multipart/form-data`
* **Form Fields:**
  * `image`: Screen frame image file (`image/jpeg` or `image/png`).
  * `audio`: User's recorded voice clip (`audio/webm` or `audio/wav`).
  * `language`: Preferred language code (`"ur"` or `"en"`, defaults to `"ur"`).
* **Response Body (`application/json`):**
  ```json
  {
    "status": "success",
    "transcript": "Mera account logout ho gaya, kya karun?",
    "ai_response": "Pareshan na hon, aapka balance mehfooz hai. Screen ke darmiyan mein 'Login' button par tap karein.",
    "audio_base64": "data:audio/mp3;base64,//uQxAAAAAAAAAAAAAAAA...",
    "is_scam_warning": false,
    "suggested_action": "Tap 'Login' to re-authenticate"
  }
  ```

### 2. `GET /api/system/health`
* **Description:** Diagnostic heartbeat confirming FastAPI runtime.

---

## 5. Architecture Strategy: Stateless MVP

* **No Database Requirement for MVP:** The core live assistance loop is completely real-time and stateless.
* **Benefits:**
  * **Zero Setup Overhead:** No database tables, migrations, or Supabase connection debugging.
  * **Privacy by Design:** Screen frames and spoken queries are processed strictly in-memory and never persisted on any database server.
  * **Speed to Delivery:** The team can dedicate 100% of the build window to refining the real-time AI response quality, voice naturalness, and elder-friendly UI interactions.

---

## 6. Frontend UI/UX Guidelines (Pure Single-Page Experience)

To eliminate anxiety for non-tech-native users, the frontend UI is strictly minimalist:

1. **One Primary Action:** The main view features a large, friendly center button:
   * **OFF state:** Clear label *"Start Assistant / شروع کریں"* with subtle guidance text.
   * **ON state:** Pulsing soundwave animation with *"Listening... Speak anytime / سن رہا ہوں..."*.
2. **Accessible Visuals:**
   * High contrast text, large typography, and zero confusing technical jargon.
   * Prominent Urdu and English toggle switch.
3. **Live Reassurance Area:**
   * When [Name not Finalized] speaks, display clear captions with highlighted key terms (e.g., *"Tap the blue button"*).
4. **Instant Spoken Guidance:**
   * Automatically play the synthesized voice as soon as the response arrives.

---

## 7. AI System Prompt Persona (Qwen on Groq)

The system prompt for `qwen/qwen3.8-27b` must strictly follow these rules:

* **Role:** You are a sober, direct, and objective digital technical assistant helping users navigate their screen.
* **Error Assessment (Mandatory First Step):** Explicitly state whether there is an error or issue on the screen:
  - If an error, warning, or blocker is visible: Clearly specify what error is shown.
  - If no error is present: State directly that there is no error and screen is normal.
* **Tone & Language:** Sober, professional, direct to the point. No unnecessary fluff or emotional padding. Fluent conversational Urdu (or simple English). Avoid technical jargon (e.g. "API", "authentication").
* **Safety & Scams:** If the screen shows a phishing link, fake prize, or suspicious element, warn directly: *"Yeh mashkook link hai, is par click na karein"*.
* **Simplicity:** Provide **only 1 or 2 concrete, direct steps at a time**. Keep answers concise (2 to 3 sentences maximum).

---

## 8. Development Rules & Hackathon Submission Checklist

1. **Keep Development Commits Regular:** Per the rulebook, commit progress regularly during the official build window; avoid large monolithic single commits.
2. **Groq Rate-Limiting Guard:**
   * Never stream continuous video to Groq.
   * Only send **one keyframe snapshot** when the user speaks or requests guidance.
3. **Demo Video Constraints (Mandatory):**
   * Maximum **2 minutes**.
   * Clearly present: Target user problem $\rightarrow$ Live single-button turn-on $\rightarrow$ Spoken query on a confusing screen $\rightarrow$ Instant Urdu speech response and live captions.
4. **Final README Update:**
   * Identify the final submitted commit hash in `README.md` before 5:00 PM PKT.
   * Disclose AI tools and dependencies (Groq API, Edge-TTS, Vue 3, FastAPI).
