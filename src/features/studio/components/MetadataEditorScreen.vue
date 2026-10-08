<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { AlertCircle, CalendarClock, Check, Clock3, Eye, FileVideo2, History, Plus, Upload, X } from '@lucide/vue'
import { ApiError } from '../../../shared/api/http'
import { getContentHistory, getMetadataVersion, updateMetadata, type ContentMetadata, type VideoVisibility } from '../api/content.api'
import { formatFileSize, type LibraryItem } from '../data/library.fixtures'

const props = defineProps<{
  initialContentId: string | null
  demoItem: LibraryItem | null
}>()

const emit = defineEmits<{
  back: []
  upload: []
}>()

const contentId = ref('')
const title = ref('')
const description = ref('')
const tags = ref<string[]>([])
const tagDraft = ref('')
const visibility = ref<VideoVisibility>('public')
const history = ref<ContentMetadata[]>([])
const demoMode = ref(false)
const currentVersion = ref<number | null>(null)
const loading = ref(false)
const saving = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const tagError = ref('')
const scheduledDate = ref('')
const scheduledTime = ref('12:00')
const fileInputId = 'content-id'

const isDemo = computed(() => demoMode.value)
const isHistoricalVersion = computed(() => currentVersion.value !== null && currentVersion.value !== latestVersion.value)
const latestVersion = computed(() => history.value[0]?.version ?? null)
const titleValid = computed(() => title.value.trim().length > 0 && title.value.length <= 100)
const descriptionValid = computed(() => description.value.length <= 5000)
const canSave = computed(() => !isDemo.value && Boolean(contentId.value.trim()) && titleValid.value && descriptionValid.value && !saving.value && !loading.value && !isHistoricalVersion.value)

function fill(metadata: ContentMetadata | null): void {
  title.value = metadata?.title ?? ''
  description.value = metadata?.description ?? ''
  tags.value = [...(metadata?.tags ?? [])]
  visibility.value = metadata?.visibility ?? 'private'
  currentVersion.value = metadata?.version ?? null
}

function loadDemo(item: LibraryItem): void {
  demoMode.value = true
  contentId.value = item.id
  const current: ContentMetadata = {
    id: `${item.id}-metadata-v3`, version: 3, title: item.title,
    description: 'Descripción de demostración. Los datos de esta publicación pertenecen a fixtures locales y no se guardarán en el backend.',
    tags: ['demostración', 'PubTube'], visibility: 'public', createdAt: item.updatedAt,
  }
  fill(current)
  history.value = [current, { ...current, id: `${item.id}-metadata-v2`, version: 2, createdAt: '2026-10-15T16:08:00Z' }, { ...current, id: `${item.id}-metadata-v1`, version: 1, createdAt: '2026-10-12T09:31:00Z' }]
  errorMessage.value = ''
  successMessage.value = ''
}

async function loadContent(id = contentId.value): Promise<void> {
  const normalizedId = id.trim()
  if (!normalizedId) {
    errorMessage.value = 'Introduce el ID real del contenido para consultar sus metadatos.'
    return
  }
  contentId.value = normalizedId
  demoMode.value = false
  loading.value = true
  errorMessage.value = ''
  successMessage.value = ''
  currentVersion.value = null
  try {
    const result = await getContentHistory(normalizedId)
    history.value = result.historial
    fill(result.metadata)
    if (!result.metadata) successMessage.value = 'El video existe, pero todavía no tiene metadatos. Completa el formulario para crear la primera versión.'
  } catch (error) {
    history.value = []
    fill(null)
    errorMessage.value = error instanceof Error ? error.message : 'No se pudieron cargar los metadatos.'
  } finally {
    loading.value = false
  }
}

function switchToRealContent(): void {
  demoMode.value = false
  contentId.value = ''
  history.value = []
  currentVersion.value = null
  fill(null)
  errorMessage.value = ''
  successMessage.value = ''
}

async function openVersion(version: number): Promise<void> {
  if (isDemo.value) return
  loading.value = true
  errorMessage.value = ''
  try {
    const result = await getMetadataVersion(contentId.value, version)
    fill(result.metadata)
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'No se pudo cargar esa versión.'
  } finally {
    loading.value = false
  }
}

async function saveMetadata(): Promise<void> {
  if (!canSave.value) return
  saving.value = true
  errorMessage.value = ''
  successMessage.value = ''
  try {
    await updateMetadata(contentId.value, {
      title: title.value.trim(), description: description.value,
      tags: [...tags.value], visibility: visibility.value,
    })
    await loadContent(contentId.value)
    successMessage.value = 'Metadatos guardados como una nueva versión. El video no se ha programado.'
  } catch (error) {
    errorMessage.value = error instanceof ApiError && error.status === 401
      ? 'La API requiere una sesión válida para guardar metadatos.'
      : error instanceof Error ? error.message : 'No se pudieron guardar los metadatos.'
  } finally {
    saving.value = false
  }
}

function addTag(): void {
  const value = tagDraft.value.trim()
  tagError.value = ''
  if (!value) return
  if (value.length > 50) { tagError.value = 'Cada etiqueta admite hasta 50 caracteres.'; return }
  if (tags.value.includes(value)) { tagError.value = 'Esa etiqueta ya está en la lista.'; return }
  if (tags.value.length >= 15) { tagError.value = 'El backend admite hasta 15 etiquetas.'; return }
  tags.value.push(value)
  tagDraft.value = ''
}

function removeTag(value: string): void { tags.value = tags.value.filter((tag) => tag !== value) }

function handleTagKeydown(event: KeyboardEvent): void {
  if (event.key === 'Enter' || event.key === ',') {
    event.preventDefault()
    addTag()
  }
}

function formatVersionDate(value: string): string {
  return new Intl.DateTimeFormat('es-ES', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' }).format(new Date(value))
}

watch(
  () => [props.initialContentId, props.demoItem] as const,
  ([nextId, demo]) => {
    if (demo) loadDemo(demo)
    else if (nextId) { contentId.value = nextId; void loadContent(nextId) }
    else { demoMode.value = false; contentId.value = ''; history.value = []; fill(null) }
  },
  { immediate: true },
)
</script>

<template>
  <div class="editor-screen">
    <nav class="breadcrumbs" aria-label="Ruta de navegación"><button type="button" @click="emit('back')">Biblioteca</button><span>/</span><span>{{ title || 'Contenido' }}</span><span>/</span><strong>Editar</strong></nav>
    <header class="screen-title"><div><h1>Editar y preparar publicación</h1><p>Prepara los detalles del video y revisa la intención de publicación.</p></div><button class="button button-secondary" type="button" @click="emit('upload')"><Upload :size="17" /> Subir video</button></header>

    <div v-if="isDemo" class="notice notice-info" role="status"><AlertCircle :size="18" /><span><strong>Vista de demostración.</strong> No se harán llamadas ni se guardarán cambios para este elemento ficticio. Puedes cargar un contenido real mediante su ID.</span><button class="text-button" type="button" @click="switchToRealContent">Cambiar a ID real</button></div>

    <form class="content-id-bar" @submit.prevent="loadContent()">
      <label :for="fileInputId">ID real del contenido</label>
      <input :id="fileInputId" v-model="contentId" autocomplete="off" placeholder="Pega aquí el contentId UUID" :disabled="loading || isDemo" />
      <button class="button button-secondary" type="submit" :disabled="loading || !contentId.trim() || isDemo">{{ loading ? 'Cargando…' : 'Cargar contenido' }}</button>
      <button v-if="isDemo" class="text-button" type="button" @click="emit('upload')">Usar un video propio</button>
    </form>

    <div v-if="errorMessage" class="notice notice-error" role="alert"><AlertCircle :size="18" /><span>{{ errorMessage }}</span></div>
    <div v-if="successMessage" class="notice notice-success" role="status"><Check :size="18" /><span>{{ successMessage }}</span></div>

    <div class="editor-grid">
      <main class="editor-main">
        <form class="form-card" @submit.prevent="saveMetadata">
          <section class="form-section">
            <div class="field-heading"><label for="video-title">Título</label><span>{{ title.length }} / 100 caracteres</span></div>
            <input id="video-title" v-model="title" maxlength="100" required :disabled="loading || isHistoricalVersion" placeholder="Escribe un título" />
            <p v-if="!titleValid && title" class="field-error">El título es obligatorio y admite hasta 100 caracteres.</p>
          </section>
          <section class="form-section">
            <div class="field-heading"><label for="video-description">Descripción</label><span>{{ description.length }} / 5.000 caracteres</span></div>
            <textarea id="video-description" v-model="description" maxlength="5000" rows="5" :disabled="loading || isHistoricalVersion" placeholder="Describe el contenido del video" />
            <p v-if="!descriptionValid" class="field-error">La descripción supera el máximo permitido.</p>
          </section>
          <section class="form-section">
            <label for="tag-entry">Etiquetas</label>
            <div class="tag-field"><span v-for="tag in tags" :key="tag" class="tag-chip">{{ tag }}<button type="button" :aria-label="`Quitar etiqueta ${tag}`" :disabled="loading || isHistoricalVersion" @click="removeTag(tag)"><X :size="13" /></button></span><input id="tag-entry" v-model="tagDraft" maxlength="50" :disabled="loading || isHistoricalVersion || tags.length >= 15" placeholder="Añadir etiqueta" @keydown="handleTagKeydown" /><button class="add-tag" type="button" :disabled="loading || isHistoricalVersion" @click="addTag"><Plus :size="14" /> Añadir</button></div>
            <p class="field-help">Hasta 15 etiquetas, máximo 50 caracteres cada una.</p><p v-if="tagError" class="field-error">{{ tagError }}</p>
          </section>
          <fieldset class="form-section visibility-fieldset" :disabled="loading || isHistoricalVersion">
            <legend>Visibilidad</legend>
            <div class="visibility-options">
              <label v-for="option in [{ id: 'public', name: 'Público', hint: 'Cualquiera puede verlo.' }, { id: 'unlisted', name: 'No listado', hint: 'Solo quien tenga el enlace.' }, { id: 'private', name: 'Privado', hint: 'Solo tú y quienes invites.' }]" :key="option.id" class="visibility-option" :class="{ selected: visibility === option.id }"><input v-model="visibility" type="radio" name="visibility" :value="option.id" /><span><strong>{{ option.name }}</strong><small>{{ option.hint }}</small></span></label>
            </div>
          </fieldset>
          <footer class="form-footer"><div><span v-if="latestVersion">Versión actual: {{ latestVersion }}</span><span v-else>Guardar crea una nueva versión de metadatos.</span><small>Guardar cambios no publica ni programa el video.</small></div><button class="button button-primary" type="submit" :disabled="!canSave">{{ saving ? 'Guardando…' : 'Guardar cambios' }}</button></footer>
        </form>

        <section class="history-card" aria-labelledby="history-title"><header><h2 id="history-title"><History :size="18" /> Historial <span v-if="history.length">· {{ history.length }} versiones</span></h2><button v-if="isHistoricalVersion" class="text-button" type="button" @click="loadContent()">Volver a la versión actual</button></header><div v-if="loading" class="history-empty" role="status">Cargando historial…</div><div v-else-if="!history.length" class="history-empty">El historial aparecerá cuando cargues un contenido real con versiones.</div><ol v-else class="history-list"><li v-for="entry in history" :key="entry.id" :class="{ 'history-current': currentVersion === entry.version }"><time>{{ formatVersionDate(entry.createdAt) }}</time><span><strong>Versión {{ entry.version }}</strong><small>{{ entry.title }}</small></span><button class="text-button" type="button" :disabled="isDemo || loading" @click="openVersion(entry.version)">Ver versión</button></li></ol></section>
      </main>

      <aside class="editor-aside">
        <section class="file-card"><div class="file-heading"><span class="file-icon"><FileVideo2 :size="22" /></span><div><strong>{{ demoItem?.filename || 'Información del archivo' }}</strong><small v-if="demoItem">{{ formatFileSize(demoItem.sizeBytes) }} · datos de demostración</small><small v-else-if="contentId">ID: {{ contentId }}</small><small v-else>Se muestra al cargar contenido real</small></div></div><button class="preview-button" type="button" disabled :title="'El backend no expone una URL de vista previa.'"><Eye :size="16" /> Vista previa no disponible</button><p>La API consultada no incluye nombre, tamaño ni URL de reproducción.</p></section>

        <section class="schedule-card"><header><CalendarClock :size="20" /><h2>Programar publicación</h2></header><span class="not-ready"><span></span> Programación no disponible</span><p>La programación existe parcialmente en servicios internos, pero el backend aún no ofrece un endpoint HTTP para guardarla.</p><label>Fecha<input v-model="scheduledDate" type="date" disabled /></label><label>Hora<input v-model="scheduledTime" type="time" disabled /></label><div class="schedule-warning"><Clock3 :size="16" /> Esta fecha es solo una referencia visual; no se enviará ni persistirá.</div><button class="button button-primary schedule-action" type="button" disabled>Programar publicación</button><small>Primero guarda los metadatos cuando tengas un ID real.</small></section>
      </aside>
    </div>
  </div>
</template>

<style scoped>
.editor-screen { display: grid; gap: 14px; }
.breadcrumbs { display: flex; align-items: center; gap: 9px; color: var(--color-text-secondary); font-size: var(--font-size-small); }.breadcrumbs button,.text-button { border: 0; padding: 0; background: transparent; color: var(--color-action-primary); cursor: pointer; }.breadcrumbs strong { color: var(--color-text-primary); font-weight: var(--font-weight-medium); }
.screen-title { display: flex; justify-content: space-between; align-items: center; gap: 16px; }.screen-title h1 { font-size: var(--font-size-heading-1); margin: 0 0 5px; }.screen-title p { margin: 0; color: var(--color-text-secondary); }
.button { display: inline-flex; justify-content: center; align-items: center; gap: 8px; padding: 10px 15px; border-radius: var(--radius-md); border: 1px solid transparent; font-weight: var(--font-weight-semibold); cursor: pointer; }.button-primary { background: var(--color-action-primary); color: white; }.button-primary:disabled { opacity: .55; cursor: not-allowed; }.button-secondary { color: var(--color-text-primary); background: var(--color-background-surface); border-color: var(--color-border-default); }
.notice { display: flex; align-items: flex-start; gap: 10px; padding: 12px 14px; border-radius: var(--radius-md); font-size: var(--font-size-small); }.notice svg { flex: 0 0 auto; }.notice-info { color: var(--color-status-info-text); background: var(--color-status-info-soft); }.notice-success { color: var(--color-status-success-text); background: var(--color-status-success-soft); }.notice-error { color: var(--color-status-danger-text); background: var(--color-status-danger-soft); }
.content-id-bar { display: flex; align-items: center; gap: 10px; padding: 12px; border: 1px solid var(--color-border-default); background: var(--color-background-surface); border-radius: var(--radius-md); }.content-id-bar label { color: var(--color-text-secondary); font-size: var(--font-size-small); }.content-id-bar input { flex: 1; min-width: 120px; border: 1px solid var(--color-border-default); border-radius: var(--radius-sm); padding: 9px 10px; }.content-id-bar .text-button { white-space: nowrap; }
.editor-grid { display: grid; grid-template-columns: minmax(0,1.55fr) minmax(290px,.9fr); align-items: start; gap: 16px; }.editor-main,.editor-aside { display: grid; gap: 14px; min-width: 0; }.form-card,.history-card,.file-card,.schedule-card { background: var(--color-background-surface); border: 1px solid var(--color-border-default); border-radius: var(--radius-lg); overflow: hidden; }.form-section { display: grid; gap: 8px; padding: 17px 19px; border-bottom: 1px solid var(--color-border-default); }.form-section label,.visibility-fieldset legend { font-weight: var(--font-weight-medium); }.field-heading { display: flex; justify-content: space-between; align-items: center; gap: 12px; }.field-heading span,.field-help { color: var(--color-text-secondary); font-size: var(--font-size-caption); }.form-section input:not([type=radio]),.form-section textarea { border: 1px solid var(--color-border-default); border-radius: var(--radius-md); padding: 10px 11px; width: 100%; background: var(--color-background-surface); }.form-section textarea { resize: vertical; line-height: 1.5; }.field-help,.field-error { margin: 0; }.field-error { color: var(--color-status-danger-text); font-size: var(--font-size-caption); }.tag-field { min-height: 44px; display: flex; flex-wrap: wrap; align-items: center; gap: 6px; border: 1px solid var(--color-border-default); border-radius: var(--radius-md); padding: 5px 8px; }.tag-field input:not([type=radio]) { flex: 1 1 120px; width: auto; min-width: 80px; padding: 5px; border: 0; outline: 0; }.tag-chip { display: inline-flex; align-items: center; gap: 4px; padding: 4px 7px; border-radius: var(--radius-sm); background: var(--color-action-primary-soft); color: var(--color-action-primary); font-size: var(--font-size-caption); }.tag-chip button { display: grid; place-items: center; border: 0; padding: 0; background: transparent; color: inherit; cursor: pointer; }.add-tag { display: inline-flex; align-items: center; gap: 4px; border: 0; padding: 5px; background: transparent; color: var(--color-action-primary); cursor: pointer; }
.visibility-fieldset { border: 0; margin: 0; }.visibility-fieldset legend { padding: 0; }.visibility-options { display: grid; grid-template-columns: repeat(3,minmax(0,1fr)); gap: 8px; }.visibility-option { display: flex; align-items: flex-start; gap: 8px; border: 1px solid var(--color-border-default); border-radius: var(--radius-md); padding: 11px 9px; cursor: pointer; }.visibility-option.selected { border-color: var(--color-action-primary); background: var(--color-action-primary-soft); }.visibility-option input { margin: 3px 0 0; accent-color: var(--color-action-primary); }.visibility-option span { display: grid; gap: 5px; }.visibility-option strong { font-weight: var(--font-weight-medium); }.visibility-option small { color: var(--color-text-secondary); font-size: var(--font-size-caption); line-height: 1.4; }
.form-footer { display: flex; justify-content: space-between; align-items: center; gap: 16px; padding: 14px 19px; }.form-footer div { display: grid; gap: 4px; color: var(--color-text-secondary); font-size: var(--font-size-small); }.form-footer small { font-size: var(--font-size-caption); }.history-card { padding: 16px 19px; }.history-card header { display: flex; justify-content: space-between; align-items: center; gap: 12px; }.history-card h2 { display: flex; align-items: center; gap: 8px; font-size: var(--font-size-heading-3); margin: 0; }.history-card h2 span { color: var(--color-text-secondary); font-weight: var(--font-weight-regular); }.history-list { list-style: none; margin: 12px 0 0; padding: 0; }.history-list li { display: grid; grid-template-columns: 110px minmax(0,1fr) auto; align-items: center; gap: 10px; padding: 11px 0; border-top: 1px solid var(--color-border-default); }.history-list li.history-current { background: var(--color-action-primary-soft); }.history-list time,.history-list small { color: var(--color-text-secondary); font-size: var(--font-size-caption); }.history-list span { display: grid; gap: 3px; min-width: 0; }.history-list span strong { font-size: var(--font-size-small); }.history-list small { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }.history-empty { padding: 22px 0 5px; color: var(--color-text-secondary); font-size: var(--font-size-small); }
.file-card { padding: 16px; }.file-heading { display: flex; align-items: center; gap: 11px; }.file-icon { display: grid; place-items: center; width: 42px; height: 42px; border-radius: var(--radius-md); color: var(--color-action-primary); background: var(--color-action-primary-soft); }.file-heading div { display: grid; gap: 4px; min-width: 0; }.file-heading strong { overflow-wrap: anywhere; }.file-heading small,.file-card p { color: var(--color-text-secondary); font-size: var(--font-size-caption); }.file-card p { margin: 9px 0 0; }.preview-button { margin-top: 13px; width: 100%; display: flex; align-items: center; justify-content: center; gap: 7px; padding: 9px; border: 1px solid var(--color-border-default); border-radius: var(--radius-md); background: var(--color-background-surface); color: var(--color-text-secondary); }.preview-button:disabled { cursor: not-allowed; opacity: .8; }
.schedule-card { padding: 17px; }.schedule-card header { display: flex; align-items: center; gap: 9px; color: var(--color-action-primary); }.schedule-card h2 { color: var(--color-text-primary); font-size: var(--font-size-heading-3); margin: 0; }.not-ready { display: inline-flex; align-items: center; gap: 6px; margin: 13px 0 9px; color: var(--color-status-warning-text); background: var(--color-status-warning-soft); border-radius: var(--radius-full); padding: 5px 9px; font-size: var(--font-size-caption); }.not-ready span { width: 6px; height: 6px; border-radius: 50%; background: currentColor; }.schedule-card p,.schedule-card>small { color: var(--color-text-secondary); font-size: var(--font-size-small); line-height: 1.5; }.schedule-card label { display: block; margin-top: 10px; font-size: var(--font-size-small); }.schedule-card input { display: block; width: 100%; margin-top: 5px; padding: 9px; border: 1px solid var(--color-border-default); border-radius: var(--radius-sm); background: var(--color-background-canvas); }.schedule-warning { display: flex; gap: 7px; margin: 12px 0; padding: 9px; color: var(--color-status-warning-text); background: var(--color-status-warning-soft); border-radius: var(--radius-sm); font-size: var(--font-size-caption); }.schedule-action { width: 100%; margin-bottom: 8px; }.schedule-card>small { display: block; text-align: center; font-size: var(--font-size-caption); }
@media (max-width: 900px) { .editor-grid { grid-template-columns: minmax(0,1fr); }.editor-aside { grid-template-columns: repeat(2,minmax(0,1fr)); } }
@media (max-width: 640px) { .screen-title,.content-id-bar { align-items: stretch; flex-direction: column; }.screen-title { align-items: flex-start; }.editor-aside { grid-template-columns: 1fr; }.visibility-options { grid-template-columns: 1fr; }.form-footer { align-items: stretch; flex-direction: column; }.form-footer .button { width: 100%; }.history-list li { grid-template-columns: 1fr auto; }.history-list time { grid-column: 1 / -1; }.content-id-bar input { width: 100%; }.tag-field input:not([type=radio]) { flex-basis: 100%; }.screen-title .button { align-self: flex-start; } }
</style>
