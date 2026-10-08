import { afterEach, describe, expect, it, vi } from 'vitest'
import { ApiError, apiRequest } from './http'
import { duplicateContentId } from '../../features/studio/api/content.api'

afterEach(() => {
  vi.unstubAllGlobals()
  vi.unstubAllEnvs()
})

describe('errores de la API de contenido', () => {
  it('extrae el id existente de una respuesta 409 DUPLICATE_CONTENT', () => {
    const error = new ApiError('Contenido duplicado', 409, {
      statusCode: 409,
      error: 'DUPLICATE_CONTENT',
      existingContentId: 'content-123',
    })

    expect(duplicateContentId(error)).toBe('content-123')
  })

  it('no confunde otros errores 409 con contenido duplicado', () => {
    expect(duplicateContentId(new ApiError('Conflicto', 409, { error: 'OTHER' }))).toBeNull()
  })

  it('conserva el código y el contentId enviados por NestJS en el body 409', async () => {
    vi.stubEnv('VITE_API_BASE_URL', 'http://localhost:8000')
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: false,
      status: 409,
      text: async () => JSON.stringify({
        statusCode: 409,
        error: 'DUPLICATE_CONTENT',
        message: 'Este video ya existe en el catálogo',
        existingContentId: 'backend-content-77',
      }),
    }))

    let caught: unknown
    try {
      await apiRequest('/api/content/init', { method: 'POST', body: '{}' })
    } catch (error) {
      caught = error
    }

    expect(caught).toBeInstanceOf(ApiError)
    expect(duplicateContentId(caught)).toBe('backend-content-77')
  })
})
