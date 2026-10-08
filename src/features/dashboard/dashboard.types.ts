export type PublicationStatus = 'scheduled' | 'published' | 'failed'

export type PublicationStatusFilter = PublicationStatus | 'all'

export interface Publication {
  id: string
  title: string
  channel: string
  owner: string
  status: PublicationStatus
  date: string
  time: string
  error?: string
}

export interface DashboardDateFilters {
  from: string
  to: string
}

export const STATUS_LABELS: Record<PublicationStatus, string> = {
  scheduled: 'Programadas',
  published: 'Publicadas',
  failed: 'Fallidas',
}

export const STATUS_FILTER_LABELS: Record<PublicationStatusFilter, string> = {
  all: 'Todos los estados',
  ...STATUS_LABELS,
}
