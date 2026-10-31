import { defineStore } from 'pinia'
import { ref, computed, shallowRef } from 'vue'
import type { Language, AssistantWorkflowState, ErrorCode, AssistResponse } from '@/types'
import api from '@/api/client'

export const useAssistantStore = defineStore('assistant', () => {
    // 1. Core Language & Settings (Default: English)
    const language = ref<Language>('en')

    // Configurable App Name Placeholder (can be customized anytime)
    const appName = ref<string>('Hamqadam')
    const appNameUrdu = ref<string>('ہمقدم')

    const currentAppName = computed(() => {
        return language.value === 'ur' ? appNameUrdu.value : appName.value
    })

    // 2. Real Workflow State & Error Code
    const workflowState = ref<AssistantWorkflowState>('idle')
    const errorCode = ref<ErrorCode>(null)
    const isBackendReachable = ref<boolean>(true)

    // 3. Media Streams & Hardware Handles
    const displayStream = shallowRef<MediaStream | null>(null)
    const micStream = shallowRef<MediaStream | null>(null)
    const mediaRecorder = shallowRef<MediaRecorder | null>(null)
    const audioChunks = ref<Blob[]>([])
    const audioPlayer = shallowRef<HTMLAudioElement | null>(null)

    // 4. Document Picture-in-Picture Floating Window State
    const pipWindow = shallowRef<Window | null>(null)
    const isPipOpen = ref<boolean>(false)
    const pipMountTarget = shallowRef<HTMLElement | null>(null)
    const pipUnsupportedNotice = ref<boolean>(false)

    // 5. Conversation / Response Data (Only populated upon real backend response)
    const transcript = ref<string>('')
    const aiResponse = ref<string>('')
    const suggestedAction = ref<string>('')
    const isScamWarning = ref<boolean>(false)
    const audioBase64 = ref<string | null>(null)

    // 6. Complete Typed Translations (No external i18n package needed)
    const translations = {
        en: {
            brandName: 'Your Digital Companion',
            brandTagline: 'Your Digital Companion',
            heroHeading: "Technology can be simple. We're here to help.",
            heroSupporting:
                'Speak naturally in your own words. We will watch your screen and guide you step-by-step with warm, patient voice instructions.',
            startAssistant: 'Start Assistant',
            tapToSpeak: 'Tap to Speak',
            tapToFinish: 'Tap to Finish',
            processingButton: 'Thinking...',
            statusIdle: 'Click Start Assistant to begin',
            statusPermissions: 'Requesting screen & microphone access...',
            statusReady: 'Ready to help',
            statusListening: 'Listening... Speak naturally',
            statusProcessing: 'Processing your request...',
            statusError: 'An issue occurred',
            stopAssistant: 'Stop Assistant',
            userSaid: 'What you asked',
            aiSaid: 'Assistant Guidance',
            repeatResponse: 'Repeat Response',
            askAnother: 'Ask Another Question',
            nextStep: 'Next Step',
            scamNoticeTitle: 'Security Notice: Suspicious Activity Detected',
            scamNoticeText:
                "Don't worry, your device is safe as long as you do not click suspicious links or share sensitive information.",
            scamNoticeAdvice:
                'Do not tap on this link or button, and never share any passwords or one-time passcodes (OTP).',
            errorPermissionDenied:
                'Screen or microphone permission was not granted. Please allow access to let the assistant see and hear your request.',
            errorScreenStopped:
                'Screen sharing was ended. Tap Start Assistant when you are ready to resume.',
            errorNetwork:
                'Could not connect to the backend assistance service. Please ensure the backend server is running.',
            errorUnsupported:
                'Screen sharing is not supported in this browser. Please use Chrome, Edge, or a desktop browser.',
            errorGeneric:
                'An unexpected error occurred while processing your request. Please try again.',
            dismiss: 'Dismiss',
            systemStatus: 'System Status',
            connectionProblem: 'Connection problem',
            screenSharingActive: 'Screen is being shared',
            hintIdle: 'Tap Start Assistant to begin.',
            hintReady: "Tap the button, then tell us what's confusing.",
            hintListening: "Speak naturally, then tap again when you're done.",
            hintProcessing: "Please wait a moment, we're looking at your screen.",
            pipUnsupportedHint: 'For an always-on-top floating window, use Google Chrome or Microsoft Edge.',
            pipSwitchHint: 'Switch to the page you need help with. The assistant stays on top.',
            pipActiveHeading: 'Assistant is floating on your screen',
            bringControlsBack: 'Return Controls to Tab',
            reopenPip: 'Open Floating Window',
            pipShortScamTitle: 'Security Alert',
            pipShortScamNotice: 'Suspicious activity detected on screen. Do not tap unknown links or give OTPs.',
        },
        ur: {
            brandName: 'آپ کا ڈیجیٹل ساتھی',
            brandTagline: 'آپ کا ڈیجیٹل ساتھی',
            heroHeading: 'ٹیکنالوجی آسان ہو سکتی ہے۔ ہم آپ کی مدد کے لیے حاضر ہیں۔',
            heroSupporting:
                'اپنی زبان میں آرام سے بات کریں۔ ہم آپ کی اسکرین دیکھ کر مرحلہ وار اور تحمل کے ساتھ آپ کی رہنمائی کریں گے۔',
            startAssistant: 'اسسٹنٹ شروع کریں',
            tapToSpeak: 'بولنے کے لیے ٹیپ کریں',
            tapToFinish: 'ختم کرنے کے لیے ٹیپ کریں',
            processingButton: 'سوچ رہا ہے...',
            statusIdle: 'شروع کرنے کے لیے کلک کریں',
            statusPermissions: 'اسکرین اور مائیکروفون کی اجازت لی جا رہی ہے...',
            statusReady: 'مدد کے لیے تیار ہے',
            statusListening: 'سن رہا ہے... آرام سے بولیں',
            statusProcessing: 'آپ کی درخواست پر کام ہو رہا ہے...',
            statusError: 'کوئی مسئلہ پیش آ گیا',
            stopAssistant: 'اسسٹنٹ بند کریں',
            userSaid: 'آپ کا سوال',
            aiSaid: 'مددگار کا جواب',
            repeatResponse: 'دوبارہ سنیں',
            askAnother: 'نیا سوال پوچھیں',
            nextStep: 'اگلا قدم',
            scamNoticeTitle: 'حفاظتی انتباہ: مشکوک مواد کا خطرہ',
            scamNoticeText:
                'گھبرائیے مت، جب تک آپ مشکوک لنک نہیں کھولیں گے یا خفیہ کوڈ نہیں دیں گے، آپ کا فون مکمل محفوظ ہے۔',
            scamNoticeAdvice:
                'اس لنک یا بٹن پر ہرگز کلک نہ کریں اور اپنا پاسورڈ یا او ٹی پی (OTP) کسی کو نہ بتائیں۔',
            errorPermissionDenied:
                'اسکرین یا مائیکروفون کی اجازت نہیں ملی۔ رہنمائی حاصل کرنے کے لیے برائے مہربانی اجازت دیں۔',
            errorScreenStopped:
                'اسکرین شیئرنگ بند ہو گئی۔ جب آپ تیار ہوں، دوبارہ اسسٹنٹ شروع کریں۔',
            errorNetwork:
                'اسسٹنٹ سروس سے رابطہ نہیں ہو سکا۔ برائے مہربانی اپنا انٹرنیٹ اور سرور چیک کریں۔',
            errorUnsupported:
                'اس براؤزر میں اسکرین شیئرنگ کی سہولت دستیاب نہیں ہے۔ برائے مہربانی کروم یا ایج براؤزر استعمال کریں۔',
            errorGeneric:
                'درخواست پر عمل کرتے ہوئے کوئی مسئلہ پیش آیا۔ برائے مہربانی دوبارہ کوشش کریں۔',
            dismiss: 'بند کریں',
            systemStatus: 'سسٹم اسٹیٹس',
            connectionProblem: 'رابطے میں مسئلہ',
            screenSharingActive: 'اسکرین شیئر ہو رہی ہے',
            hintIdle: 'شروع کرنے کے لیے اسسٹنٹ کا بٹن دبائیں۔',
            hintReady: 'بٹن پر ٹیپ کریں، پھر بتائیں کہ آپ کو کیا سمجھ نہیں آ رہا۔',
            hintListening: 'آرام سے بولیں، اور بات مکمل ہونے پر دوبارہ ٹیپ کریں۔',
            hintProcessing: 'ایک لمحہ انتظار کریں، ہم آپ کی اسکرین دیکھ رہے ہیں۔',
            pipUnsupportedHint: 'دیگر ٹیبز کے اوپر تیرتی ہوئی ونڈو کے لیے گوگل کروم یا مائیکروسافٹ ایج استعمال کریں۔',
            pipSwitchHint: 'جس صفحے پر مدد درکار ہے وہاں جائیں۔ اسسٹنٹ اوپر ہی رہے گا۔',
            pipActiveHeading: 'اسسٹنٹ آپ کی اسکرین کے اوپر موجود ہے',
            bringControlsBack: 'کنٹرولز واپس ٹیب میں لائیں',
            reopenPip: 'فلوٹنگ ونڈو کھولیں',
            pipShortScamTitle: 'حفاظتی انتباہ',
            pipShortScamNotice: 'اسکرین پر مشکوک مواد نظر آ رہا ہے۔ کسی لنک پر کلک نہ کریں اور OTP مت دیں۔',
        },
    }

    const t = computed(() => translations[language.value])
    const isUrdu = computed(() => language.value === 'ur')
    const hasResponse = computed(() => Boolean(aiResponse.value))
    const isListening = computed(() => workflowState.value === 'listening')
    const isProcessing = computed(() => workflowState.value === 'processing')
    const isReady = computed(() => workflowState.value === 'ready')

    // Screen sharing live check
    const isScreenSharing = computed(() => {
        return Boolean(
            displayStream.value &&
                displayStream.value.active &&
                displayStream.value.getVideoTracks().some((track) => track.readyState === 'live')
        )
    })

    // Dynamic error message resolution based on active language (eliminates translation bug)
    const errorMessage = computed(() => {
        if (!errorCode.value) return null
        switch (errorCode.value) {
            case 'permission_denied':
                return t.value.errorPermissionDenied
            case 'screen_stopped':
                return t.value.errorScreenStopped
            case 'network':
                return t.value.errorNetwork
            case 'unsupported':
                return t.value.errorUnsupported
            case 'generic':
            default:
                return t.value.errorGeneric
        }
    })

    // Next-Step Hint driven by real assistant state
    const nextStepHint = computed(() => {
        switch (workflowState.value) {
            case 'idle':
                return t.value.hintIdle
            case 'requesting_permissions':
                return t.value.hintIdle
            case 'ready':
                return t.value.hintReady
            case 'listening':
                return t.value.hintListening
            case 'processing':
                return t.value.hintProcessing
            case 'error':
                return t.value.hintIdle
            default:
                return t.value.hintIdle
        }
    })

    // Dynamic button label based on application state
    const buttonText = computed(() => {
        switch (workflowState.value) {
            case 'idle':
            case 'error':
                return t.value.startAssistant
            case 'requesting_permissions':
            case 'processing':
                return t.value.processingButton
            case 'ready':
                return t.value.tapToSpeak
            case 'listening':
                return t.value.tapToFinish
            default:
                return t.value.startAssistant
        }
    })

    // Single status line text reflecting real state
    const currentStatusText = computed(() => {
        if (errorMessage.value) return errorMessage.value
        switch (workflowState.value) {
            case 'idle':
                return t.value.statusIdle
            case 'requesting_permissions':
                return t.value.statusPermissions
            case 'ready':
                return t.value.statusReady
            case 'listening':
                return t.value.statusListening
            case 'processing':
                return t.value.statusProcessing
            default:
                return t.value.statusIdle
        }
    })

    // Language switch with document direction update (both main tab and PiP window)
    function setLanguage(lang: Language) {
        language.value = lang
        if (typeof document !== 'undefined') {
            document.documentElement.dir = lang === 'ur' ? 'rtl' : 'ltr'
            document.documentElement.lang = lang
        }
        if (pipWindow.value && !pipWindow.value.closed) {
            try {
                pipWindow.value.document.documentElement.dir = lang === 'ur' ? 'rtl' : 'ltr'
                pipWindow.value.document.documentElement.lang = lang
                pipWindow.value.document.body.style.fontFamily =
                    lang === 'ur' ? "'Noto Nastaliq Urdu', serif" : "'Inter', sans-serif"
            } catch (e) {
                console.warn('Could not update PiP window language direction:', e)
            }
        }
    }

    // Copy fonts, stylesheets, and base styling into PiP window
    function copyStylesToPip(pipWin: Window) {
        const head = pipWin.document.head

        // 1. Copy Google Fonts and link tags
        document.head.querySelectorAll('link[rel="stylesheet"], link[rel="preconnect"]').forEach((el) => {
            head.appendChild(el.cloneNode(true))
        })

        // 2. Copy all document style sheets (Tailwind, app styles, etc.)
        Array.from(document.styleSheets).forEach((sheet) => {
            try {
                if (sheet.href) {
                    const link = pipWin.document.createElement('link')
                    link.rel = 'stylesheet'
                    link.href = sheet.href
                    head.appendChild(link)
                } else if (sheet.cssRules) {
                    const style = pipWin.document.createElement('style')
                    for (const rule of sheet.cssRules) {
                        style.appendChild(pipWin.document.createTextNode(rule.cssText))
                    }
                    head.appendChild(style)
                }
            } catch {
                if (sheet.href) {
                    const link = pipWin.document.createElement('link')
                    link.rel = 'stylesheet'
                    link.href = sheet.href
                    head.appendChild(link)
                }
            }
        })

        // 3. Copy any raw style tags from head
        document.head.querySelectorAll('style').forEach((st) => {
            const style = pipWin.document.createElement('style')
            style.textContent = st.textContent
            head.appendChild(style)
        })

        // 4. Set document attributes and base body styles
        pipWin.document.title = currentAppName.value + ' - Floating Assistant'
        pipWin.document.documentElement.dir = language.value === 'ur' ? 'rtl' : 'ltr'
        pipWin.document.documentElement.lang = language.value
        pipWin.document.body.style.backgroundColor = '#F7F1E7'
        pipWin.document.body.style.color = '#3D2B20'
        pipWin.document.body.style.margin = '0'
        pipWin.document.body.style.padding = '12px'
        pipWin.document.body.style.boxSizing = 'border-box'
        pipWin.document.body.style.overflowX = 'hidden'
        pipWin.document.body.style.fontFamily =
            language.value === 'ur' ? "'Noto Nastaliq Urdu', serif" : "'Inter', sans-serif"
    }

    // Open Document Picture-in-Picture window
    async function openPipWindow() {
        if (!window.documentPictureInPicture || typeof window.documentPictureInPicture.requestWindow !== 'function') {
            pipUnsupportedNotice.value = true
            return
        }

        // Close existing PiP window if already open
        closePipWindow()

        try {
            const pipWin = await window.documentPictureInPicture.requestWindow({
                width: 280,
                height: 180,
            })

            // Copy typography and stylesheets
            copyStylesToPip(pipWin)

            // Create target mount element
            const mountContainer = pipWin.document.createElement('div')
            mountContainer.id = 'pip-control-root'
            pipWin.document.body.appendChild(mountContainer)

            // Handle window close event (controls seamlessly return to the tab)
            pipWin.addEventListener('pagehide', () => {
                isPipOpen.value = false
                pipMountTarget.value = null
                pipWindow.value = null
            })

            pipWindow.value = pipWin
            pipMountTarget.value = mountContainer
            isPipOpen.value = true
            pipUnsupportedNotice.value = false
        } catch (err) {
            console.warn('Failed to open Document Picture-in-Picture window:', err)
            pipUnsupportedNotice.value = true
            isPipOpen.value = false
            pipMountTarget.value = null
            pipWindow.value = null
        }
    }

    // Close Document Picture-in-Picture window
    function closePipWindow() {
        if (pipWindow.value && !pipWindow.value.closed) {
            try {
                pipWindow.value.close()
            } catch (e) {
                console.warn('Error closing PiP window:', e)
            }
        }
        pipWindow.value = null
        pipMountTarget.value = null
        isPipOpen.value = false
    }

    // Helper: Capture a single keyframe snapshot from the screen stream
    // Uses ImageCapture(track).grabFrame() to prevent background tab freezing, with <video> fallback.
    async function captureScreenFrame(stream: MediaStream): Promise<Blob> {
        const videoTrack = stream.getVideoTracks()[0]
        if (!videoTrack) {
            throw new Error('No video track available in screen stream')
        }

        // 1. Primary approach: ImageCapture(track).grabFrame() directly from track
        if (typeof (window as any).ImageCapture === 'function') {
            try {
                const imageCapture = new (window as any).ImageCapture(videoTrack)
                const bitmap: ImageBitmap = await imageCapture.grabFrame()

                let width = bitmap.width
                let height = bitmap.height
                if (width > 1280) {
                    height = Math.round((height * 1280) / width)
                    width = 1280
                }

                const canvas = document.createElement('canvas')
                canvas.width = width
                canvas.height = height
                const ctx = canvas.getContext('2d')
                if (ctx) {
                    ctx.drawImage(bitmap, 0, 0, width, height)
                }

                bitmap.close?.()

                return await new Promise<Blob>((resolve, reject) => {
                    canvas.toBlob(
                        (blob) => {
                            if (blob) resolve(blob)
                            else reject(new Error('Failed to create frame blob from ImageBitmap'))
                        },
                        'image/jpeg',
                        0.85
                    )
                })
            } catch (err) {
                console.warn('ImageCapture.grabFrame failed, falling back to video element:', err)
            }
        }

        // 2. Fallback: offscreen <video> + <canvas>
        return new Promise(async (resolve, reject) => {
            try {
                const video = document.createElement('video')
                video.srcObject = stream
                video.muted = true
                video.playsInline = true
                await video.play()

                // Allow 120ms for video frame rendering
                await new Promise((r) => setTimeout(r, 120))

                let width = video.videoWidth || 1280
                let height = video.videoHeight || 720
                if (width > 1280) {
                    height = Math.round((height * 1280) / width)
                    width = 1280
                }

                const canvas = document.createElement('canvas')
                canvas.width = width
                canvas.height = height
                const ctx = canvas.getContext('2d')
                if (ctx) {
                    ctx.drawImage(video, 0, 0, width, height)
                }

                video.pause()
                video.srcObject = null

                canvas.toBlob(
                    (blob) => {
                        if (blob) resolve(blob)
                        else reject(new Error('Failed to capture screen image blob'))
                    },
                    'image/jpeg',
                    0.85
                )
            } catch (err) {
                reject(err)
            }
        })
    }

    // Audio Playback
    function playAudio(audioSrc: string) {
        try {
            if (audioPlayer.value) {
                audioPlayer.value.pause()
                audioPlayer.value = null
            }
            const audio = new Audio(audioSrc)
            audioPlayer.value = audio
            audio.play().catch((e) => console.warn('Audio autoplay prevented:', e))
        } catch (e) {
            console.warn('Playback error:', e)
        }
    }

    // Repeat response audio or speech synthesis
    function repeatResponse() {
        if (audioPlayer.value) {
            audioPlayer.value.currentTime = 0
            audioPlayer.value.play().catch(() => {})
        } else if (audioBase64.value) {
            playAudio(audioBase64.value)
        } else if (typeof window !== 'undefined' && 'speechSynthesis' in window && aiResponse.value) {
            const utterance = new SpeechSynthesisUtterance(aiResponse.value)
            utterance.lang = language.value === 'ur' ? 'ur-PK' : 'en-US'
            window.speechSynthesis.speak(utterance)
        }
    }

    // Check backend health quietly
    async function checkBackendHealth() {
        try {
            await api.get('/', { timeout: 4000 })
            isBackendReachable.value = true
        } catch (err: any) {
            if (err.code === 'ERR_NETWORK' || !err.response) {
                isBackendReachable.value = false
            }
        }
    }

    // Workflow Step 1: Start Assistant, Request Permissions, and Open PiP
    async function startAssistantWorkflow() {
        errorCode.value = null
        workflowState.value = 'requesting_permissions'

        if (!navigator.mediaDevices || !navigator.mediaDevices.getDisplayMedia) {
            errorCode.value = 'unsupported'
            workflowState.value = 'error'
            return
        }

        try {
            // 1. Request Screen Share
            const screen = await navigator.mediaDevices.getDisplayMedia({
                video: { cursor: 'always' } as any,
                audio: false,
            })
            displayStream.value = screen

            // Listen if user stops screen sharing from browser bar
            const track = screen.getVideoTracks()[0]
            if (track) {
                track.onended = () => {
                    handleScreenShareEnded()
                }
            }

            // 2. Request Microphone
            const mic = await navigator.mediaDevices.getUserMedia({
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                },
            })
            micStream.value = mic

            workflowState.value = 'ready'

            // 3. Open Document Picture-in-Picture floating window
            await openPipWindow()
        } catch (err: any) {
            stopAssistant()
            workflowState.value = 'idle'
            errorCode.value = 'permission_denied'
        }
    }

    // Workflow Step 2: Start Recording Voice
    function startListening() {
        if (!micStream.value) {
            startAssistantWorkflow()
            return
        }

        errorCode.value = null
        audioChunks.value = []

        try {
            const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
                ? 'audio/webm;codecs=opus'
                : 'audio/webm'

            const recorder = new MediaRecorder(micStream.value, { mimeType })
            recorder.ondataavailable = (event) => {
                if (event.data && event.data.size > 0) {
                    audioChunks.value.push(event.data)
                }
            }

            recorder.start(100)
            mediaRecorder.value = recorder
            workflowState.value = 'listening'
        } catch (err: any) {
            errorCode.value = 'generic'
            workflowState.value = 'ready'
        }
    }

    // Workflow Step 3: Stop Recording, Capture Frame, and Submit to Backend
    async function stopListeningAndSubmit() {
        if (workflowState.value !== 'listening' || !mediaRecorder.value) return

        workflowState.value = 'processing'
        const recorder = mediaRecorder.value

        recorder.onstop = async () => {
            try {
                const audioBlob = new Blob(audioChunks.value, { type: 'audio/webm' })

                if (!displayStream.value) {
                    throw new Error('Screen stream not active')
                }

                // Capture one sharp screenshot from display stream (ImageCapture / Video fallback)
                const imageBlob = await captureScreenFrame(displayStream.value)

                // Build Multipart Form Data
                const formData = new FormData()
                formData.append('image', imageBlob, 'screenshot.jpg')
                formData.append('audio', audioBlob, 'recording.webm')
                formData.append('language', language.value)

                // Call Backend POST /api/assist
                const response = await api.post<AssistResponse>('/api/assist', formData, {
                    headers: { 'Content-Type': 'multipart/form-data' },
                    timeout: 45000,
                })

                isBackendReachable.value = true

                if (response.data) {
                    transcript.value = response.data.transcript || ''
                    aiResponse.value = response.data.ai_response || ''
                    suggestedAction.value = response.data.suggested_action || ''
                    isScamWarning.value = Boolean(response.data.is_scam_warning)
                    audioBase64.value = response.data.audio_base64 || null

                    if (audioBase64.value) {
                        playAudio(audioBase64.value)
                    }
                }

                workflowState.value = 'ready'
            } catch (err: any) {
                console.error('Assistance request failed:', err)
                if (err.code === 'ERR_NETWORK' || !err.response) {
                    isBackendReachable.value = false
                    errorCode.value = 'network'
                } else {
                    errorCode.value = 'generic'
                }
                workflowState.value = 'ready'
            }
        }

        try {
            recorder.stop()
        } catch (e) {
            workflowState.value = 'ready'
        }
    }

    // Main Microphone Button Trigger Handler
    function handleMainAction() {
        if (workflowState.value === 'idle' || workflowState.value === 'error') {
            startAssistantWorkflow()
        } else if (workflowState.value === 'ready') {
            startListening()
        } else if (workflowState.value === 'listening') {
            stopListeningAndSubmit()
        }
    }

    // Ask Another Question
    function askAnother() {
        errorCode.value = null
        workflowState.value = 'ready'
    }

    // Screen sharing stopped by user (browser toolbar)
    function handleScreenShareEnded() {
        stopAssistant()
        errorCode.value = 'screen_stopped'
    }

    // Stop Assistant and release all tracks/resources and close PiP
    function stopAssistant() {
        closePipWindow()

        if (mediaRecorder.value && mediaRecorder.value.state !== 'inactive') {
            try {
                mediaRecorder.value.stop()
            } catch {}
        }
        mediaRecorder.value = null

        if (micStream.value) {
            micStream.value.getTracks().forEach((track) => track.stop())
            micStream.value = null
        }

        if (displayStream.value) {
            displayStream.value.getTracks().forEach((track) => track.stop())
            displayStream.value = null
        }

        if (audioPlayer.value) {
            audioPlayer.value.pause()
            audioPlayer.value = null
        }

        workflowState.value = 'idle'
    }

    return {
        language,
        appName,
        appNameUrdu,
        currentAppName,
        workflowState,
        errorCode,
        errorMessage,
        isBackendReachable,
        isScreenSharing,
        pipWindow,
        isPipOpen,
        pipMountTarget,
        pipUnsupportedNotice,
        transcript,
        aiResponse,
        suggestedAction,
        isScamWarning,
        audioBase64,
        t,
        isUrdu,
        hasResponse,
        isListening,
        isProcessing,
        isReady,
        buttonText,
        currentStatusText,
        nextStepHint,
        setLanguage,
        handleMainAction,
        startAssistantWorkflow,
        startListening,
        stopListeningAndSubmit,
        repeatResponse,
        askAnother,
        stopAssistant,
        checkBackendHealth,
        openPipWindow,
        closePipWindow,
    }
})
