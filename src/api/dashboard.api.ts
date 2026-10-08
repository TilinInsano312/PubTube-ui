import type {
  DashboardCounts,
  DashboardCountsResponse,
  DashboardErrorCode,
  DashboardHttpStatus,
} from './dashboard.types'

export interface DashboardDateQuery {
  from?: string
  to?: string
}

const DASHBOARD_ERROR_CODES: Record<DashboardHttpStatus, DashboardErrorCode> = {
  401: 'UNAUTHORIZED',
  422: 'INVALID_DATE_RANGE',
  429: 'RATE_LIMIT_EXCEEDED',
  500: 'DASHBOARD_ERROR',
  503: 'DASHBOARD_UNAVAILABLE',
  504: 'DASHBOARD_TIMEOUT',
}

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? '/api').replace(/\/+$/, '')

export class DashboardApiError extends Error {
  readonly code: DashboardErrorCode
  readonly status?: number

  constructor(code: DashboardErrorCode, status?: number) {
    super(code)
    this.name = 'DashboardApiError'
    this.code = code
    this.status = status
  }
}

function isDashboardHttpStatus(status: number): status is DashboardHttpStatus {
  return status in DASHBOARD_ERROR_CODES
}

function isDashboardCountsResponse(value: unknown): value is DashboardCountsResponse {
  if (typeof value !== 'object' || value === null) {
    return false
  }

  const response = value as Record<string, unknown>
  const data = response.data

  if (response.status !== 'ok' || typeof data !== 'object' || data === null) {
    return false
  }

  const counts = data as Record<string, unknown>
  return (
    typeof counts.scheduled === 'number' &&
    typeof counts.published === 'number' &&
    typeof counts.failed === 'number'
  )
}

function buildDashboardUrl(query: DashboardDateQuery = {}): string {
  const params = new URLSearchParams()

  if (query.from) {
    params.set('from', query.from)
  }

  if (query.to) {
    params.set('to', query.to)
  }

  const queryString = params.toString()
  const endpoint = `${API_BASE_URL}/dashboard`
  return queryString ? `${endpoint}?${queryString}` : endpoint
}

export async function getDashboardCounts(
  query: DashboardDateQuery = {},
  signal?: AbortSignal,
): Promise<DashboardCounts> {
  let response: Response

  try {
    response = await fetch(buildDashboardUrl(query), {
      headers: {
        Accept: 'application/json',
      },
      method: 'GET',
      signal,
    })
  } catch {
    throw new DashboardApiError('NETWORK_ERROR')
  }

  if (!response.ok) {
    const code = isDashboardHttpStatus(response.status)
      ? DASHBOARD_ERROR_CODES[response.status]
      : 'DASHBOARD_ERROR'
    throw new DashboardApiError(code, response.status)
  }

  let payload: unknown

  try {
    payload = await response.json()
  } catch {
    throw new DashboardApiError('INVALID_RESPONSE', response.status)
  }

  if (!isDashboardCountsResponse(payload)) {
    throw new DashboardApiError('INVALID_RESPONSE', response.status)
  }

  return payload.data
}
