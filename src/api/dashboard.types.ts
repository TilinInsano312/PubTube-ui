export interface DashboardCounts {
  scheduled: number
  published: number
  failed: number
}

export interface DashboardCountsResponse {
  status: 'ok'
  data: DashboardCounts
}

export type DashboardErrorCode =
  | 'UNAUTHORIZED'
  | 'INVALID_DATE_RANGE'
  | 'RATE_LIMIT_EXCEEDED'
  | 'DASHBOARD_ERROR'
  | 'DASHBOARD_UNAVAILABLE'
  | 'DASHBOARD_TIMEOUT'
  | 'NETWORK_ERROR'
  | 'INVALID_RESPONSE'

export type DashboardHttpStatus = 401 | 422 | 429 | 500 | 503 | 504
