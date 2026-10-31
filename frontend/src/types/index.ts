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
