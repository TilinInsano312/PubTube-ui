import type { DashboardDateFilters, Publication } from './dashboard.types'

const MOCK_PUBLICATIONS: Publication[] = [
  {
    id: 'PUB-1042',
    title: 'Cómo crear una estrategia de contenido sostenible',
    channel: 'YouTube',
    owner: 'Equipo editorial',
    status: 'published',
    date: '2026-09-02',
    time: '09:30',
  },
  {
    id: 'PUB-1043',
    title: 'Behind the scenes: grabación de septiembre',
    channel: 'YouTube',
    owner: 'Camila Rojas',
    status: 'published',
    date: '2026-09-05',
    time: '16:45',
  },
  {
    id: 'PUB-1044',
    title: 'Entrevista con la comunidad de creadores',
    channel: 'YouTube',
    owner: 'Equipo editorial',
    status: 'scheduled',
    date: '2026-09-12',
    time: '18:00',
  },
  {
    id: 'PUB-1045',
    title: 'Guía rápida para optimizar tus miniaturas',
    channel: 'YouTube',
    owner: 'Sebastián Díaz',
    status: 'scheduled',
    date: '2026-09-15',
    time: '11:00',
  },
  {
    id: 'PUB-1046',
    title: 'Novedades de la plataforma PubTube',
    channel: 'YouTube',
    owner: 'Equipo producto',
    status: 'failed',
    date: '2026-09-18',
    time: '14:15',
    error: 'La publicación no pudo completar la validación del canal.',
  },
  {
    id: 'PUB-1047',
    title: 'Resumen semanal: métricas y aprendizajes',
    channel: 'YouTube',
    owner: 'Camila Rojas',
    status: 'published',
    date: '2026-09-21',
    time: '10:00',
  },
  {
    id: 'PUB-1048',
    title: 'Preguntas frecuentes sobre programación',
    channel: 'YouTube',
    owner: 'Equipo editorial',
    status: 'scheduled',
    date: '2026-09-25',
    time: '17:30',
  },
  {
    id: 'PUB-1049',
    title: 'Caso de estudio: crecer con una audiencia nicho',
    channel: 'YouTube',
    owner: 'Sebastián Díaz',
    status: 'published',
    date: '2026-09-29',
    time: '13:00',
  },
]

function wait(milliseconds: number): Promise<void> {
  return new Promise((resolve) => window.setTimeout(resolve, milliseconds))
}

/**
 * Local data source used until the publications API contract is available.
 * Keeping the mock behind an async function makes the loading/error states
 * exercise the same boundary that a real API client will use later.
 */
export async function getMockPublications(filters: DashboardDateFilters): Promise<Publication[]> {
  await wait(280)

  if (filters.from && filters.to && filters.from > filters.to) {
    throw new Error('El inicio del rango debe ser anterior o igual al final.')
  }

  return MOCK_PUBLICATIONS.filter((publication) => {
    const afterStart = !filters.from || publication.date >= filters.from
    const beforeEnd = !filters.to || publication.date <= filters.to
    return afterStart && beforeEnd
  })
}
