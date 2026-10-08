import { ApiError, apiRequest } from '../../../shared/api/http'

export type VideoVisibility = 'public' | 'unlisted' | 'private'

export interface ContentMetadata {
  id: string
  version: number
  title: string
  description: string | null
  tags: string[] | null
  visibility: VideoVisibility
  createdAt: string
}

export interface ContentHistoryResponse {
  status: number
  contentId: string
  metadata: ContentMetadata | null
  historial: ContentMetadata[]
}

export interface MetadataPayload {
  title: string
  description: string
  tags: string[]
  visibility: VideoVisibility
}

interface MetadataResponse {
  status: number
  contentId: string
  metadata: ContentMetadata
}

export interface InitUploadResponse {
  status: number
  uploadSessionId: string
}

export interface UploadPart {
  PartNumber: number
  ETag: string
  Size?: number
}

interface UploadStatusResponse {
  status: number
  parts: UploadPart[]
}

interface PresignedUrlResponse {
  url: string
}

interface CompleteUploadResponse {
  status: number
  contentId: string
  checksumSha256: string
}

export function duplicateContentId(error: unknown): string | null {
  if (
    error instanceof ApiError &&
    error.status === 409 &&
    error.code === 'DUPLICATE_CONTENT' &&
    typeof error.body.existingContentId === 'string'
  ) {
    return error.body.existingContentId
  }

  return null
}

export function getContentHistory(
  contentId: string,
): Promise<ContentHistoryResponse> {
  return apiRequest<ContentHistoryResponse>(
    `/api/content/${encodeURIComponent(contentId)}`,
  )
}

export function getMetadataVersion(
  contentId: string,
  version: number,
): Promise<MetadataResponse> {
  return apiRequest<MetadataResponse>(
    `/api/content/${encodeURIComponent(contentId)}/metadata/versions/${version}`,
  )
}

export function updateMetadata(
  contentId: string,
  payload: MetadataPayload,
): Promise<MetadataResponse> {
  return apiRequest<MetadataResponse>(
    `/api/content/${encodeURIComponent(contentId)}/metadata`,
    {
      method: 'PUT',
      body: JSON.stringify(payload),
    },
  )
}

export interface UploadProgress {
  phase: 'checksum' | 'upload'
  percent: number
  uploadedBytes: number
  totalBytes: number
}

const PART_SIZE = 8 * 1024 * 1024

async function calculateSha256(
  file: File,
  onProgress: (percent: number) => void,
  signal?: AbortSignal,
): Promise<string> {
  // Streaming keeps memory bounded for the backend's 2 GB maximum file size.
  const { sha256 } = await import('@noble/hashes/sha256')
  const hasher = sha256.create()

  for (let offset = 0; offset < file.size; offset += PART_SIZE) {
    if (signal?.aborted)
      throw new DOMException('Carga cancelada en este navegador.', 'AbortError')
    const chunk = new Uint8Array(
      await file.slice(offset, offset + PART_SIZE).arrayBuffer(),
    )
    hasher.update(chunk)
    onProgress(
      Math.round(
        (Math.min(offset + chunk.byteLength, file.size) / file.size) * 100,
      ),
    )
  }

  return Array.from(hasher.digest(), (byte) =>
    byte.toString(16).padStart(2, '0'),
  ).join('')
}

export async function uploadVideo(
  file: File,
  onProgress: (progress: UploadProgress) => void,
  signal?: AbortSignal,
): Promise<{ contentId: string; checksumSha256: string }> {
  const extension = file.name.toLowerCase().split('.').pop()
  const mimeType =
    file.type ||
    (extension === 'mov'
      ? 'video/quicktime'
      : extension === 'mp4'
        ? 'video/mp4'
        : '')
  if (mimeType !== 'video/mp4' && mimeType !== 'video/quicktime') {
    throw new Error('El backend solo acepta archivos MP4 o MOV.')
  }

  const checksum = await calculateSha256(
    file,
    (percent) => {
      onProgress({
        phase: 'checksum',
        percent,
        uploadedBytes: 0,
        totalBytes: file.size,
      })
    },
    signal,
  )

  const initialized = await apiRequest<InitUploadResponse>(
    '/api/content/init',
    {
      method: 'POST',
      body: JSON.stringify({
        filename: file.name,
        mimeType,
        sizeBytes: file.size,
        checksum,
      }),
      signal,
    },
  )
  const sessionId = initialized.uploadSessionId
  const status = await apiRequest<UploadStatusResponse>(
    `/api/content/upload/${encodeURIComponent(sessionId)}/status`,
    { signal },
  )
  const completedParts = new Map(
    status.parts.map((part) => [part.PartNumber, part]),
  )
  const partCount = Math.ceil(file.size / PART_SIZE)
  let uploadedBytes = status.parts.reduce(
    (total, part) => total + (part.Size ?? 0),
    0,
  )

  for (let partNumber = 1; partNumber <= partCount; partNumber += 1) {
    if (signal?.aborted)
      throw new DOMException('Carga cancelada en este navegador.', 'AbortError')
    const existingPart = completedParts.get(partNumber)
    if (existingPart) {
      if (!existingPart.Size)
        uploadedBytes += Math.min(
          PART_SIZE,
          file.size - (partNumber - 1) * PART_SIZE,
        )
      onProgress({
        phase: 'upload',
        percent: Math.round((uploadedBytes / file.size) * 100),
        uploadedBytes,
        totalBytes: file.size,
      })
      continue
    }

    const start = (partNumber - 1) * PART_SIZE
    const chunk = file.slice(start, Math.min(start + PART_SIZE, file.size))
    const signed = await apiRequest<PresignedUrlResponse>(
      `/api/content/${encodeURIComponent(sessionId)}/part/${partNumber}`,
      { signal },
    )
    const response = await fetch(signed.url, {
      method: 'PUT',
      body: chunk,
      signal,
    })
    if (!response.ok) {
      throw new Error(
        `Garage rechazó la parte ${partNumber} (${response.status}).`,
      )
    }

    const etag = response.headers.get('ETag')
    if (!etag) {
      throw new Error(
        'Garage no expuso el ETag de la parte. Revisa la configuración CORS del bucket.',
      )
    }

    completedParts.set(partNumber, { PartNumber: partNumber, ETag: etag })
    uploadedBytes += chunk.size
    onProgress({
      phase: 'upload',
      percent: Math.round((uploadedBytes / file.size) * 100),
      uploadedBytes,
      totalBytes: file.size,
    })
  }

  const parts = Array.from(completedParts.values()).sort(
    (a, b) => a.PartNumber - b.PartNumber,
  )
  const completed = await apiRequest<CompleteUploadResponse>(
    `/api/content/upload/${encodeURIComponent(sessionId)}/complete`,
    {
      method: 'POST',
      body: JSON.stringify({
        parts: parts.map(({ PartNumber, ETag }) => ({ PartNumber, ETag })),
      }),
      signal,
    },
  )

  return {
    contentId: completed.contentId,
    checksumSha256: completed.checksumSha256,
  }
}
