export type LibraryStatus = 'scheduled' | 'published' | 'draft'

export interface LibraryItem {
  id: string
  title: string
  filename: string
  sizeBytes: number
  status: LibraryStatus
  updatedAt: string
  thumbnailTone: 'purple' | 'blue' | 'slate' | 'rose'
}

// Demostración visual solamente: el backend no ofrece catálogo paginado ni agregados.
export const LIBRARY_FIXTURES: LibraryItem[] = [
  { id: 'demo-01', title: 'Introducción a PubTube', filename: 'introduccion.mp4', sizeBytes: 193986560, status: 'published', updatedAt: '2026-10-10T10:00:00', thumbnailTone: 'purple' },
  { id: 'demo-02', title: 'Flujo de publicación automática', filename: 'pipeline_v2.mp4', sizeBytes: 335544320, status: 'scheduled', updatedAt: '2026-10-14T18:30:00', thumbnailTone: 'blue' },
  { id: 'demo-03', title: 'Demo Sprint 2', filename: 'demo_preview.mp4', sizeBytes: 99614720, status: 'draft', updatedAt: '2026-10-18T09:15:00', thumbnailTone: 'slate' },
  { id: 'demo-04', title: 'Resumen semanal del proyecto', filename: 'recap_semana_42.mp4', sizeBytes: 220200960, status: 'published', updatedAt: '2026-10-21T11:00:00', thumbnailTone: 'purple' },
  { id: 'demo-05', title: 'Guía rápida de integración API', filename: 'api_quickstart.mp4', sizeBytes: 148897792, status: 'scheduled', updatedAt: '2026-10-25T16:45:00', thumbnailTone: 'blue' },
  { id: 'demo-06', title: 'Tutorial de renderizado por lotes', filename: 'batch_render_err.mp4', sizeBytes: 536870912, status: 'draft', updatedAt: '2026-10-28T14:20:00', thumbnailTone: 'rose' },
  { id: 'demo-07', title: 'Diseño de una cola editorial', filename: 'cola_editorial.mp4', sizeBytes: 186646528, status: 'published', updatedAt: '2026-10-29T12:00:00', thumbnailTone: 'slate' },
  { id: 'demo-08', title: 'Automatización para equipos pequeños', filename: 'automatizacion.mp4', sizeBytes: 287309824, status: 'scheduled', updatedAt: '2026-10-30T15:30:00', thumbnailTone: 'purple' },
  { id: 'demo-09', title: 'Entrevista con el equipo de producto', filename: 'entrevista.mp4', sizeBytes: 408944640, status: 'published', updatedAt: '2026-10-12T10:45:00', thumbnailTone: 'blue' },
  { id: 'demo-10', title: 'Primeros pasos con la biblioteca', filename: 'primeros_pasos.mp4', sizeBytes: 127926272, status: 'draft', updatedAt: '2026-10-16T08:30:00', thumbnailTone: 'rose' },
  { id: 'demo-11', title: 'Planificación de contenidos', filename: 'planificacion.mp4', sizeBytes: 251658240, status: 'published', updatedAt: '2026-10-23T17:00:00', thumbnailTone: 'slate' },
  { id: 'demo-12', title: 'Publicación de principio a fin', filename: 'end_to_end.mp4', sizeBytes: 310378496, status: 'scheduled', updatedAt: '2026-10-31T09:00:00', thumbnailTone: 'purple' },
]

export function formatFileSize(bytes: number): string {
  return `${(bytes / (1024 * 1024)).toFixed(0)} MB`
}
