export type PublicationStatus = 'scheduled' | 'published' | 'failed'

export type PublicationStatusFilter = PublicationStatus | 'all'

export interface PublicationListItem {
  id: string
  contentLabel: string
  contentId?: string
  status: PublicationStatus
  scheduledAt: string
}

export interface DashboardDateFilters {
  from: string
  to: string
}
