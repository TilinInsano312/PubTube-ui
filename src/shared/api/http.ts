export interface ApiErrorBody {
  statusCode?: number
  error?: string
  message?: string | string[]
  existingContentId?: string
  [key: string]: unknown
}

export class ApiError extends Error {
  readonly status: number
  readonly body: ApiErrorBody

  constructor(
    message: string,
    status: number,
    body: ApiErrorBody,
  ) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.body = body
  }

  get code(): string | undefined {
    return this.body.error
  }
}

function correlationId(): string {
  return globalThis.crypto?.randomUUID?.() ?? `ui-${Date.now()}-${Math.random().toString(16).slice(2)}`
}

function backendUrl(path: string): string {
  const baseUrl = import.meta.env.VITE_API_BASE_URL?.trim().replace(/\/+$/, '')
  if (!baseUrl) {
    throw new Error('Configura VITE_API_BASE_URL para conectar con la API de PubTube.')
  }

  return `${baseUrl}${path}`
}

export async function apiRequest<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers)
  headers.set('x-correlation-id', correlationId())
  if (init.body && !headers.has('content-type')) {
    headers.set('content-type', 'application/json')
  }

  const response = await fetch(backendUrl(path), { ...init, headers })
  const text = await response.text()
  let body: unknown = undefined

  if (text) {
    try {
      body = JSON.parse(text)
    } catch {
      body = { message: text }
    }
  }

  if (!response.ok) {
    const errorBody = (body && typeof body === 'object' ? body : {}) as ApiErrorBody
    const message = Array.isArray(errorBody.message)
      ? errorBody.message.join(' ')
      : errorBody.message || `La API respondió con estado ${response.status}.`
    throw new ApiError(message, response.status, errorBody)
  }

  return body as T
}
