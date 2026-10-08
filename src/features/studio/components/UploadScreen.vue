<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'
import {
  AlertCircle,
  ArrowRight,
  CheckCircle2,
  CircleHelp,
  FileVideo2,
  FolderOpen,
  Upload,
  X,
} from '@lucide/vue'
import {
  duplicateContentId,
  uploadVideo,
  type UploadProgress,
} from '../api/content.api'
import { formatFileSize } from '../data/library.fixtures'

const props = defineProps<{
  uploadFile: typeof uploadVideo
}>()

const emit = defineEmits<{
  back: []
  openContent: [contentId: string]
}>()

const file = ref<File | null>(null)
const state = ref<
  | 'ready'
  | 'checksum'
  | 'uploading'
  | 'duplicate'
  | 'error'
  | 'complete'
  | 'cancelled'
>('ready')
const progress = ref<UploadProgress>({
  phase: 'checksum',
  percent: 0,
  uploadedBytes: 0,
  totalBytes: 0,
})
const uploadPercent = ref(0)
const existingContentId = ref('')
const completedContentId = ref('')
const errorMessage = ref('')
const cancelNote = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)
let abortController: AbortController | null = null

const MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024
const busy = computed(
  () => state.value === 'checksum' || state.value === 'uploading',
)
const displayedProgress = computed(() =>
  state.value === 'checksum' ? progress.value.percent : uploadPercent.value,
)
const stateLabel = computed(
  () =>
    ({
      ready: 'Listo para iniciar',
      checksum: 'Verificando archivo',
      uploading: 'Subiendo partes',
      duplicate: 'Subida pausada',
      error: 'Error de carga',
      complete: 'Carga completada',
      cancelled: 'Carga detenida en este navegador',
    })[state.value],
)

function fileMimeType(selected: File): string | null {
  if (selected.type === 'video/mp4' || selected.type === 'video/quicktime')
    return selected.type
  const extension = selected.name.toLowerCase().split('.').pop()
  if (extension === 'mp4') return 'video/mp4'
  if (extension === 'mov') return 'video/quicktime'
  return null
}

function chooseFile(event: Event): void {
  const selected = (event.target as HTMLInputElement).files?.[0]
  if (!selected) return
  errorMessage.value = ''
  cancelNote.value = false
  existingContentId.value = ''
  completedContentId.value = ''
  const mimeType = fileMimeType(selected)
  if (!mimeType) {
    file.value = null
    state.value = 'error'
    errorMessage.value = 'El backend solo acepta archivos MP4 o MOV.'
    return
  }
  if (selected.size <= 0 || selected.size > MAX_FILE_SIZE) {
    file.value = null
    state.value = 'error'
    errorMessage.value =
      selected.size > MAX_FILE_SIZE
        ? 'El archivo supera el máximo del backend (2 GB).'
        : 'El archivo está vacío.'
    return
  }
  file.value = selected
  state.value = 'ready'
}

async function startUpload(): Promise<void> {
  if (!file.value || busy.value) return
  abortController = new AbortController()
  errorMessage.value = ''
  cancelNote.value = false
  state.value = 'checksum'
  uploadPercent.value = 0
  progress.value = {
    phase: 'checksum',
    percent: 0,
    uploadedBytes: 0,
    totalBytes: file.value.size,
  }

  try {
    const result = await props.uploadFile(
      file.value,
      (next) => {
        progress.value = next
        if (next.phase === 'upload') uploadPercent.value = next.percent
        state.value = next.phase === 'checksum' ? 'checksum' : 'uploading'
      },
      abortController.signal,
    )
    completedContentId.value = result.contentId
    state.value = 'complete'
  } catch (error) {
    const duplicateId = duplicateContentId(error)
    if (duplicateId) {
      existingContentId.value = duplicateId
      state.value = 'duplicate'
    } else if (error instanceof Error && error.name === 'AbortError') {
      state.value = 'cancelled'
      cancelNote.value = true
    } else {
      state.value = 'error'
      errorMessage.value =
        error instanceof Error
          ? error.message
          : 'No se pudo completar la carga.'
    }
  } finally {
    abortController = null
  }
}

function cancelUpload(): void {
  if (busy.value) {
    abortController?.abort()
    return
  }
  emit('back')
}

function chooseAnother(): void {
  abortController?.abort()
  file.value = null
  state.value = 'ready'
  existingContentId.value = ''
  completedContentId.value = ''
  errorMessage.value = ''
  cancelNote.value = false
  uploadPercent.value = 0
  if (fileInput.value) fileInput.value.value = ''
}

onBeforeUnmount(() => abortController?.abort())
</script>

<template>
  <div class="upload-screen">
    <nav class="breadcrumbs" aria-label="Ruta de navegación">
      <button type="button" @click="emit('back')">Biblioteca</button
      ><span>/</span><strong>Subir video</strong>
    </nav>
    <header class="screen-title">
      <div>
        <h1>Subir video</h1>
        <p>Añade un video a tu biblioteca para prepararlo y publicarlo.</p>
      </div>
    </header>

    <section class="upload-card" aria-labelledby="upload-file-title">
      <header class="upload-file-header">
        <span class="file-icon"><FileVideo2 :size="24" /></span>
        <div class="file-details">
          <h2 id="upload-file-title">
            {{ file?.name || 'Selecciona un archivo de video' }}
          </h2>
          <p>
            {{
              file
                ? `${formatFileSize(file.size)} · ${fileMimeType(file) === 'video/quicktime' ? 'Video MOV' : 'Video MP4'}`
                : 'MP4 o MOV · Máximo 2 GB'
            }}
          </p>
        </div>
        <span class="state-badge" :class="`badge-${state}`"
          ><span></span>{{ stateLabel }}</span
        >
      </header>

      <div
        v-if="
          !file ||
          state === 'ready' ||
          busy ||
          state === 'error' ||
          state === 'cancelled'
        "
        class="progress-area"
      >
        <div class="progress-copy">
          <span>{{
            state === 'checksum'
              ? 'Calculando SHA-256 por bloques para comprobar duplicados…'
              : busy
                ? 'Subida directa a Garage · los bytes no pasan por NestJS'
                : state === 'cancelled'
                  ? 'Se detuvo el envío desde este navegador.'
                  : state === 'error'
                    ? 'No se pudo continuar con este archivo.'
                    : 'Archivo preparado para cargar'
          }}</span
          ><strong v-if="busy">{{ displayedProgress }}%</strong
          ><strong v-else>0%</strong>
        </div>
        <progress
          :value="busy ? displayedProgress : 0"
          max="100"
          :aria-label="`Progreso de carga ${busy ? displayedProgress : 0}%`"
        ></progress>
        <p v-if="state === 'uploading'">
          {{ formatFileSize(progress.uploadedBytes) }} de
          {{ formatFileSize(progress.totalBytes) }} transferidos.
        </p>
        <div v-if="errorMessage" class="message message-error" role="alert">
          <AlertCircle :size="18" />{{ errorMessage }}
        </div>
        <div v-if="cancelNote" class="message message-warning" role="status">
          <CircleHelp :size="18" /><span
            >La API no tiene un endpoint para cancelar la sesión remota. Se
            detuvo el envío en el navegador; si ya había comenzado una sesión,
            el multipart incompleto queda sujeto a la limpieza automática del
            backend.</span
          >
        </div>
        <div class="progress-actions">
          <label class="button button-secondary file-picker" for="video-file"
            ><FolderOpen :size="17" />{{
              file ? 'Elegir otro video' : 'Elegir video'
            }}</label
          >
          <input
            id="video-file"
            ref="fileInput"
            class="visually-hidden"
            type="file"
            accept="video/mp4,video/quicktime,.mp4,.mov"
            :disabled="busy"
            @change="chooseFile"
          />
          <button
            v-if="
              file &&
              (state === 'ready' || state === 'error' || state === 'cancelled')
            "
            class="button button-primary"
            type="button"
            @click="startUpload"
          >
            <Upload :size="16" />{{
              state === 'error' || state === 'cancelled'
                ? 'Reintentar carga'
                : 'Iniciar carga'
            }}
          </button>
          <button
            v-if="busy"
            class="button button-danger"
            type="button"
            @click="cancelUpload"
          >
            <X :size="16" />Detener envío
          </button>
        </div>
      </div>

      <template v-else-if="state === 'duplicate'">
        <div class="duplicate-progress">
          <div>
            <span>Subida detenida para evitar duplicados</span
            ><strong>{{ uploadPercent }}%</strong>
          </div>
          <progress
            :value="uploadPercent"
            max="100"
            aria-label="Progreso de la carga antes de detectar el duplicado"
          ></progress>
        </div>
        <div class="duplicate-warning" role="alert">
          <AlertCircle :size="20" />
          <div>
            <strong>Este video ya existe en tu biblioteca</strong>
            <p>
              El backend encontró el mismo SHA-256 y detuvo la carga para evitar
              duplicados.
            </p>
          </div>
        </div>
        <div class="existing-content">
          <span class="existing-icon"><FileVideo2 :size="22" /></span>
          <div>
            <strong>Contenido existente detectado</strong>
            <p>
              ID del contenido: <code>{{ existingContentId }}</code>
            </p>
            <small
              >Referencia devuelta por la API. Los detalles completos solo
              aparecen al consultar ese ID.</small
            >
          </div>
          <button
            class="text-button"
            type="button"
            @click="emit('openContent', existingContentId)"
          >
            Consultar contenido <ArrowRight :size="16" />
          </button>
        </div>
        <div class="duplicate-actions">
          <div>
            <button
              class="button button-primary"
              type="button"
              @click="emit('openContent', existingContentId)"
            >
              Usar video existente
            </button>
            <p>
              Continuarás con el contenido existente; no se crea otra copia.
            </p>
          </div>
          <button
            class="button button-secondary"
            type="button"
            @click="chooseAnother"
          >
            Elegir otro video</button
          ><button
            class="text-button cancel-link"
            type="button"
            @click="cancelUpload"
          >
            Cancelar esta subida
          </button>
        </div>
      </template>

      <template v-else-if="state === 'complete'">
        <div class="message message-success" role="status">
          <CheckCircle2 :size="20" /><span
            ><strong>Video cargado.</strong> El backend lo guardó como borrador;
            no se ha publicado ni programado.</span
          >
        </div>
        <div class="existing-content">
          <span class="existing-icon"><FileVideo2 :size="22" /></span>
          <div>
            <strong>Contenido creado</strong>
            <p>
              ID: <code>{{ completedContentId }}</code>
            </p>
          </div>
          <button
            class="text-button"
            type="button"
            @click="emit('openContent', completedContentId)"
          >
            Editar metadatos <ArrowRight :size="16" />
          </button>
        </div>
        <div class="duplicate-actions">
          <button
            class="button button-primary"
            type="button"
            @click="emit('openContent', completedContentId)"
          >
            Preparar metadatos</button
          ><button
            class="button button-secondary"
            type="button"
            @click="chooseAnother"
          >
            Subir otro video
          </button>
        </div>
      </template>

      <footer
        v-if="state === 'duplicate' || state === 'complete'"
        class="upload-footer"
      >
        <span
          >Los videos nuevos se guardan como borradores al completar la carga.
          No se publican automáticamente.</span
        ><button type="button" class="text-button" @click="emit('back')">
          Volver a la biblioteca
        </button>
      </footer>
    </section>
    <p class="upload-footnote">
      <strong>Privacidad de la transferencia:</strong> el navegador envía las
      partes a URLs prefirmadas de Garage. NestJS solo recibe metadatos de la
      carga y las referencias de partes.
    </p>
  </div>
</template>

<style scoped>
.upload-screen {
  display: grid;
  gap: 14px;
}
.breadcrumbs {
  display: flex;
  align-items: center;
  gap: 9px;
  color: var(--color-text-secondary);
  font-size: var(--font-size-small);
}
.breadcrumbs button,
.text-button {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 0;
  border: 0;
  background: transparent;
  color: var(--color-action-primary);
  cursor: pointer;
}
.breadcrumbs strong {
  color: var(--color-text-primary);
  font-weight: var(--font-weight-medium);
}
.screen-title h1 {
  margin: 0 0 5px;
  font-size: var(--font-size-heading-1);
}
.screen-title p {
  margin: 0;
  color: var(--color-text-secondary);
}
.upload-card {
  background: var(--color-background-surface);
  border: 1px solid var(--color-border-default);
  border-radius: var(--radius-lg);
  overflow: hidden;
}
.upload-file-header {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 20px 22px;
}
.file-icon,
.existing-icon {
  display: grid;
  place-items: center;
  flex: 0 0 auto;
  width: 54px;
  height: 54px;
  border-radius: var(--radius-md);
  color: var(--color-action-primary);
  background: var(--color-action-primary-soft);
}
.file-details {
  flex: 1;
  min-width: 0;
}
.file-details h2 {
  margin: 0 0 5px;
  font-size: var(--font-size-heading-3);
  overflow-wrap: anywhere;
}
.file-details p {
  margin: 0;
  color: var(--color-text-secondary);
  font-size: var(--font-size-small);
}
.state-badge {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  border-radius: var(--radius-full);
  padding: 7px 10px;
  font-size: var(--font-size-caption);
  white-space: nowrap;
}
.state-badge > span {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}
.badge-ready,
.badge-complete {
  color: var(--color-status-success-text);
  background: var(--color-status-success-soft);
}
.badge-checksum,
.badge-uploading {
  color: var(--color-status-info-text);
  background: var(--color-status-info-soft);
}
.badge-duplicate,
.badge-cancelled {
  color: var(--color-status-warning-text);
  background: var(--color-status-warning-soft);
}
.badge-error {
  color: var(--color-status-danger-text);
  background: var(--color-status-danger-soft);
}
.progress-area {
  padding: 17px 22px 22px;
  border-top: 1px solid var(--color-border-default);
}
.progress-copy {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  color: var(--color-text-secondary);
  font-size: var(--font-size-small);
}
.progress-copy strong {
  color: var(--color-action-primary);
}
.progress-area progress {
  display: block;
  width: 100%;
  height: 8px;
  margin: 12px 0 8px;
  appearance: none;
  border: 0;
  border-radius: var(--radius-full);
  background: var(--color-action-primary-soft);
  overflow: hidden;
}
.progress-area progress::-webkit-progress-bar {
  background: var(--color-action-primary-soft);
}
.progress-area progress::-webkit-progress-value {
  background: var(--color-action-primary);
  border-radius: var(--radius-full);
}
.progress-area progress::-moz-progress-bar {
  background: var(--color-action-primary);
  border-radius: var(--radius-full);
}
.progress-area > p {
  margin: 0;
  color: var(--color-text-secondary);
  font-size: var(--font-size-caption);
}
.progress-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 16px;
}
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 15px;
  border-radius: var(--radius-md);
  border: 1px solid transparent;
  font-weight: var(--font-weight-semibold);
  cursor: pointer;
}
.button-primary {
  color: white;
  background: var(--color-action-primary);
}
.button-secondary {
  color: var(--color-text-primary);
  background: var(--color-background-surface);
  border-color: var(--color-border-strong);
}
.button-danger {
  color: var(--color-status-danger-text);
  background: var(--color-status-danger-soft);
}
.file-picker {
  cursor: pointer;
}
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
.duplicate-progress {
  padding: 16px 22px 13px;
  border-top: 1px solid var(--color-border-default);
}
.duplicate-progress > div {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  color: var(--color-text-secondary);
  font-size: var(--font-size-small);
}
.duplicate-progress strong {
  color: var(--color-action-primary);
}
.duplicate-progress progress {
  display: block;
  width: 100%;
  height: 8px;
  margin-top: 10px;
  appearance: none;
  border: 0;
  border-radius: var(--radius-full);
  overflow: hidden;
  background: var(--color-action-primary-soft);
}
.duplicate-progress progress::-webkit-progress-bar {
  background: var(--color-action-primary-soft);
}
.duplicate-progress progress::-webkit-progress-value {
  background: var(--color-action-primary);
  border-radius: var(--radius-full);
}
.duplicate-progress progress::-moz-progress-bar {
  background: var(--color-action-primary);
  border-radius: var(--radius-full);
}
.duplicate-warning {
  display: flex;
  gap: 11px;
  margin: 0 22px;
  padding: 16px;
  border-radius: var(--radius-md);
  color: var(--color-status-warning-text);
  background: var(--color-status-warning-soft);
}
.duplicate-warning svg {
  flex: 0 0 auto;
}
.duplicate-warning strong {
  display: block;
  margin-bottom: 5px;
}
.duplicate-warning p {
  margin: 0;
  font-size: var(--font-size-small);
}
.existing-content {
  display: flex;
  align-items: center;
  gap: 13px;
  margin: 16px 22px;
  padding: 14px;
  border: 1px solid var(--color-border-default);
  border-radius: var(--radius-md);
}
.existing-icon {
  width: 48px;
  height: 48px;
}
.existing-content > div {
  flex: 1;
  min-width: 0;
}
.existing-content p {
  margin: 4px 0;
  color: var(--color-text-secondary);
  font-size: var(--font-size-small);
}
.existing-content small {
  color: var(--color-text-secondary);
  font-size: var(--font-size-caption);
}
.existing-content code {
  overflow-wrap: anywhere;
  font-family: var(--font-family-mono);
}
.duplicate-actions {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 0 22px 18px;
}
.duplicate-actions > div {
  margin-right: auto;
}
.duplicate-actions p {
  margin: 7px 0 0;
  color: var(--color-text-secondary);
  font-size: var(--font-size-caption);
}
.upload-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 14px 22px;
  border-top: 1px solid var(--color-border-default);
  color: var(--color-text-secondary);
  font-size: var(--font-size-caption);
}
.upload-footnote {
  color: var(--color-text-secondary);
  font-size: var(--font-size-small);
  line-height: 1.5;
}
.upload-footnote strong {
  color: var(--color-text-primary);
}
.message {
  display: flex;
  align-items: flex-start;
  gap: 9px;
  padding: 12px 14px;
  margin-top: 12px;
  border-radius: var(--radius-md);
  font-size: var(--font-size-small);
}
.message svg {
  flex: 0 0 auto;
}
.message-error {
  color: var(--color-status-danger-text);
  background: var(--color-status-danger-soft);
}
.message-warning {
  color: var(--color-status-warning-text);
  background: var(--color-status-warning-soft);
}
.message-success {
  margin: 18px 22px 0;
  color: var(--color-status-success-text);
  background: var(--color-status-success-soft);
}
@media (max-width: 650px) {
  .upload-file-header {
    align-items: flex-start;
    flex-wrap: wrap;
    padding: 16px;
  }
  .file-details {
    flex-basis: calc(100% - 70px);
  }
  .state-badge {
    margin-left: 68px;
  }
  .progress-area {
    padding: 16px;
  }
  .duplicate-warning,
  .existing-content {
    margin-left: 16px;
    margin-right: 16px;
  }
  .existing-content {
    align-items: flex-start;
    flex-wrap: wrap;
  }
  .existing-content > div {
    flex-basis: calc(100% - 65px);
  }
  .existing-content > .text-button {
    margin-left: 60px;
  }
  .duplicate-actions {
    align-items: stretch;
    flex-direction: column;
    padding: 0 16px 16px;
  }
  .duplicate-actions > div {
    margin-right: 0;
  }
  .duplicate-actions .button {
    width: 100%;
  }
  .upload-footer {
    align-items: flex-start;
    flex-direction: column;
    padding: 13px 16px;
  }
  .progress-actions {
    flex-wrap: wrap;
  }
  .progress-actions .button,
  .progress-actions .file-picker {
    flex: 1;
  }
  .progress-copy {
    align-items: flex-start;
  }
}
</style>
