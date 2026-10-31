// src/utils/media.ts

// 1. Screen frame -> image bytes (JPEG Blob)
export function frameToBlob(
  video: HTMLVideoElement,
  maxWidth = 1280,
  quality = 0.8,
): Promise<Blob> {
  return new Promise((resolve, reject) => {
    if (!video.videoWidth || !video.videoHeight) {
      return reject(new Error('video_not_ready'))
    }
    const scale = Math.min(1, maxWidth / video.videoWidth)
    const canvas = document.createElement('canvas')
    canvas.width = Math.round(video.videoWidth * scale)
    canvas.height = Math.round(video.videoHeight * scale)
    const ctx = canvas.getContext('2d')
    if (!ctx) return reject(new Error('canvas_failed'))
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
    canvas.toBlob(
      (blob) => (blob ? resolve(blob) : reject(new Error('frame_failed'))),
      'image/jpeg',
      quality,
    )
  })
}

// 2. Recorded sound (Blob) -> base64 string
export function audioBlobToBase64(blob: Blob): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onloadend = () => resolve(reader.result as string)
    reader.onerror = () => reject(new Error('audio_convert_failed'))
    reader.readAsDataURL(blob)
  })
}

// 3. Backend's audio_base64 -> play the sound
export async function playBase64Audio(dataUrl: string): Promise<HTMLAudioElement> {
  const audio = new Audio(dataUrl)
  try {
    await audio.play()
  } catch {
    throw new Error('playback_blocked')
  }
  return audio
}