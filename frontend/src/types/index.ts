export interface Note {
    id: number
    title: string
    created_at: string
}

export interface ApiResponse<T = any> {
    status: string
    message?: string
    data?: T
    detail?: string
}

export type HealthStatus = 'loading' | 'connected' | 'error'

export type Language = 'en' | 'ur'

export type AssistantWorkflowState =
    | 'idle'
    | 'requesting_permissions'
    | 'ready'
    | 'listening'
    | 'processing'
    | 'error'

export type ErrorCode =
    | 'permission_denied'
    | 'screen_stopped'
    | 'network'
    | 'unsupported'
    | 'generic'
    | null

export interface AssistResponse {
    status: string
    transcript: string
    ai_response: string
    audio_base64?: string
    is_scam_warning: boolean
    suggested_action?: string
}

// Document Picture-in-Picture API TypeScript Declarations
export interface DocumentPictureInPictureOptions {
    width?: number
    height?: number
    disallowReturnToOpener?: boolean
}

export interface DocumentPictureInPictureEvent extends Event {
    window: Window
}

export interface DocumentPictureInPicture extends EventTarget {
    window: Window | null
    requestWindow(options?: DocumentPictureInPictureOptions): Promise<Window>
    onenter?: (event: DocumentPictureInPictureEvent) => void
}

declare global {
    interface Window {
        documentPictureInPicture?: DocumentPictureInPicture
    }
}
