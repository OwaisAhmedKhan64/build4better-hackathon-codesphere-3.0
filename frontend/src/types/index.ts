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
