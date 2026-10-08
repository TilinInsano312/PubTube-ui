<script setup lang="ts">
import { computed, ref } from 'vue'
import { CalendarDays, CheckCircle2, ChevronLeft, ChevronRight, CircleDashed, Clock3, RefreshCw, Video } from '@lucide/vue'
import { LIBRARY_FIXTURES, formatFileSize, type LibraryItem, type LibraryStatus } from '../data/library.fixtures'

const emit = defineEmits<{
  openDemo: [item: LibraryItem]
  editById: []
}>()

const from = ref('2026-10-01')
const to = ref('2026-10-31')
const appliedFrom = ref(from.value)
const appliedTo = ref(to.value)
const activeFilter = ref<'all' | LibraryStatus>('all')
const currentPage = ref(1)
const loading = ref(false)
const pageSize = 6
const filters = [
  { id: 'all', label: 'Todas' },
  { id: 'scheduled', label: 'Programadas' },
  { id: 'draft', label: 'Borrador' },
  { id: 'published', label: 'Publicadas' },
] as const

const filteredItems = computed(() => LIBRARY_FIXTURES.filter((item) => {
  const date = item.updatedAt.slice(0, 10)
  return date >= appliedFrom.value && date <= appliedTo.value && (activeFilter.value === 'all' || item.status === activeFilter.value)
}))
const pageCount = computed(() => Math.max(1, Math.ceil(filteredItems.value.length / pageSize)))
const pageItems = computed(() => filteredItems.value.slice((currentPage.value - 1) * pageSize, currentPage.value * pageSize))
const stats = computed(() => ({
  scheduled: filteredItems.value.filter((item) => item.status === 'scheduled').length,
  published: filteredItems.value.filter((item) => item.status === 'published').length,
  draft: filteredItems.value.filter((item) => item.status === 'draft').length,
}))

function applyFilters(): void {
  currentPage.value = 1
  loading.value = true
  appliedFrom.value = from.value
  appliedTo.value = to.value
  window.setTimeout(() => { loading.value = false }, 220)
}

function formatDate(value: string): string {
  return new Intl.DateTimeFormat('es-ES', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', hour12: false })
    .format(new Date(value))
}
</script>

<template>
  <div class="library-screen">
    <section class="period-card" aria-label="Filtrar por período">
      <div class="period-label"><CalendarDays :size="18" /> <span>Período</span></div>
      <label class="date-control"><span>Desde</span><input v-model="from" type="date" aria-label="Fecha inicial" /></label>
      <label class="date-control"><span>Hasta</span><input v-model="to" type="date" aria-label="Fecha final" /></label>
      <button class="icon-button" type="button" aria-label="Actualizar resultados" :disabled="loading" @click="applyFilters"><RefreshCw :size="18" /></button>
      <button class="button button-primary" type="button" :disabled="loading || from > to" @click="applyFilters">Aplicar</button>
    </section>

    <div class="demo-notice" role="note">
      <CircleDashed :size="17" />
      <span><strong>Datos de demostración.</strong> El backend aún no ofrece catálogo paginado ni contadores; esta biblioteca usa fixtures locales.</span>
    </div>

    <section class="stats-card" aria-label="Resumen de la biblioteca">
      <article class="stat-item stat-scheduled"><div><Clock3 :size="17" /><span>Programadas</span><span class="stat-caption">En cola</span></div><strong>{{ stats.scheduled }}</strong><small>videos listos</small></article>
      <article class="stat-item stat-published"><div><CheckCircle2 :size="17" /><span>Publicadas</span><span class="stat-caption">Activas</span></div><strong>{{ stats.published }}</strong><small>en la biblioteca</small></article>
      <article class="stat-item stat-draft"><div><Video :size="17" /><span>En borrador</span></div><strong>{{ stats.draft }}</strong><small>sin programar</small></article>
    </section>

    <section class="library-card" aria-labelledby="library-title">
      <header class="library-heading">
        <div><h1 id="library-title">Publicaciones</h1><p>Del período seleccionado · {{ filteredItems.length }} resultados</p></div>
        <button class="edit-id-link" type="button" @click="emit('editById')">Editar por ID</button>
        <div class="status-tabs" role="group" aria-label="Filtrar publicaciones por estado">
          <button v-for="filter in filters" :key="filter.id" type="button" :aria-pressed="activeFilter === filter.id" :class="{ active: activeFilter === filter.id }" @click="activeFilter = filter.id; currentPage = 1">{{ filter.label }} <span>{{ filter.id === 'all' ? filteredItems.length : filteredItems.filter((item) => filter.id === item.status).length }}</span></button>
        </div>
      </header>

      <div class="table-scroll">
        <table>
          <thead><tr><th scope="col">Contenido</th><th scope="col">Estado</th><th scope="col">Fecha / actualizado</th><th scope="col" class="action-heading">Acciones</th></tr></thead>
          <tbody v-if="loading"><tr><td colspan="4" class="table-state" role="status">Actualizando la biblioteca…</td></tr></tbody>
          <tbody v-else-if="pageItems.length">
            <tr v-for="item in pageItems" :key="item.id">
              <td><div class="video-cell"><span class="video-thumb" :class="`tone-${item.thumbnailTone}`" aria-hidden="true"><Video :size="18" /></span><span class="video-copy"><strong>{{ item.title }}</strong><small>{{ item.filename }} <i>·</i> {{ formatFileSize(item.sizeBytes) }}</small></span></div></td>
              <td><span class="status-pill" :class="`status-${item.status}`">{{ item.status === 'scheduled' ? 'Programada' : item.status === 'published' ? 'Publicada' : 'Borrador' }}</span></td>
              <td class="date-cell">{{ formatDate(item.updatedAt) }}</td>
              <td class="action-cell"><button class="button button-soft" type="button" @click="emit('openDemo', item)">{{ item.status === 'published' ? 'Gestionar' : 'Abrir' }}</button></td>
            </tr>
          </tbody>
          <tbody v-else><tr><td colspan="4" class="table-state"><strong>No hay videos para estos filtros</strong><span>Prueba otro período o estado.</span></td></tr></tbody>
        </table>
      </div>

      <footer class="table-footer">
        <span>Mostrando {{ pageItems.length ? (currentPage - 1) * pageSize + 1 : 0 }}–{{ Math.min(currentPage * pageSize, filteredItems.length) }} de {{ filteredItems.length }} videos</span>
        <nav class="pagination" aria-label="Paginación de publicaciones">
          <button type="button" aria-label="Página anterior" :disabled="currentPage <= 1" @click="currentPage--"><ChevronLeft :size="17" /></button>
          <button v-for="page in pageCount" :key="page" type="button" :aria-label="`Página ${page}`" :aria-current="currentPage === page ? 'page' : undefined" :class="{ selected: currentPage === page }" @click="currentPage = page">{{ page }}</button>
          <button type="button" aria-label="Página siguiente" :disabled="currentPage >= pageCount" @click="currentPage++"><ChevronRight :size="17" /></button>
        </nav>
      </footer>
    </section>
  </div>
</template>

<style scoped>
.library-screen { display: grid; gap: 14px; }
.period-card,.stats-card,.library-card { background: var(--color-background-surface); border: 1px solid var(--color-border-default); border-radius: var(--radius-lg); }
.period-card { display: flex; align-items: center; gap: 10px; padding: 12px 16px; }
.period-label { display: flex; align-items: center; gap: 8px; color: var(--color-text-secondary); margin-right: 4px; white-space: nowrap; }
.date-control { display: flex; align-items: center; gap: 8px; border: 1px solid var(--color-border-default); border-radius: var(--radius-md); padding: 6px 9px; color: var(--color-text-secondary); font-size: var(--font-size-small); }
.date-control input { min-width: 135px; border: 0; outline: 0; background: transparent; color: var(--color-text-primary); }
.icon-button,.pagination button { display: inline-grid; place-items: center; background: transparent; border: 1px solid var(--color-border-default); border-radius: var(--radius-md); color: var(--color-text-secondary); min-width: 38px; min-height: 38px; cursor: pointer; }
.button { border: 1px solid transparent; border-radius: var(--radius-md); padding: 9px 16px; font-weight: var(--font-weight-semibold); cursor: pointer; }
.button-primary { background: var(--color-action-primary); color: var(--color-action-primary-content); }
.button-primary:hover { background: var(--color-action-primary-hover); }
.button-soft { background: var(--color-action-primary-soft); color: var(--color-action-primary); }
.button-soft:hover { background: var(--color-action-primary-soft-strong); }
.demo-notice { display: flex; gap: 9px; align-items: center; color: var(--color-status-info-text); background: var(--color-status-info-soft); padding: 10px 14px; border-radius: var(--radius-md); font-size: var(--font-size-small); }
.demo-notice svg { flex: 0 0 auto; }
.stats-card { display: grid; grid-template-columns: repeat(3,minmax(0,1fr)); overflow: hidden; }
.stat-item { min-height: 102px; padding: 18px 22px; }
.stat-item + .stat-item { border-left: 1px solid var(--color-border-default); }
.stat-item div { display: flex; align-items: center; gap: 8px; color: var(--color-text-secondary); font-size: var(--font-size-small); }
.stat-item strong { display: block; font-size: 28px; line-height: 1.1; margin-top: 10px; }
.stat-item small,.stat-caption { color: var(--color-text-secondary); font-size: var(--font-size-caption); }
.stat-scheduled svg,.stat-scheduled .stat-caption { color: var(--color-status-info-text); }
.stat-published svg,.stat-published .stat-caption { color: var(--color-status-success-text); }
.stat-draft svg { color: var(--color-status-warning-text); }
.library-card { overflow: hidden; }
.library-heading { display: flex; justify-content: space-between; align-items: center; gap: 16px; padding: 16px 20px; }
.library-heading h1 { margin: 0 0 4px; font-size: var(--font-size-heading-2); }
.library-heading p { margin: 0; color: var(--color-text-secondary); font-size: var(--font-size-small); }
.status-tabs { display: flex; flex-wrap: wrap; gap: 4px; }
.status-tabs button { border: 0; background: transparent; color: var(--color-text-secondary); border-radius: var(--radius-md); padding: 8px 11px; cursor: pointer; }
.status-tabs button.active { color: var(--color-action-primary); background: var(--color-action-primary-soft); font-weight: var(--font-weight-semibold); }
.edit-id-link { border: 0; padding: 8px 0; background: transparent; color: var(--color-action-primary); white-space: nowrap; cursor: pointer; }
.status-tabs button span { margin-left: 4px; }
.table-scroll { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; text-align: left; }
th { background: var(--color-background-canvas); color: var(--color-text-secondary); font-size: var(--font-size-caption); font-weight: var(--font-weight-semibold); text-transform: uppercase; letter-spacing: .04em; padding: 11px 16px; }
td { padding: 9px 16px; border-top: 1px solid var(--color-border-default); }
tbody tr:hover { background: var(--color-background-canvas); }
.action-heading,.action-cell { text-align: right; }
.video-cell { display: flex; align-items: center; gap: 12px; min-width: 280px; }
.video-thumb { display: grid; place-items: center; width: 48px; height: 40px; border-radius: var(--radius-sm); flex: 0 0 auto; }
.tone-purple { color: #6d35d9; background: #f1e7ff; }.tone-blue { color: #2265a2; background: #eaf3fc; }.tone-slate { color: #5e6174; background: #eeeef5; }.tone-rose { color: #a33a3a; background: #fff0ef; }
.video-copy { display: grid; gap: 4px; }.video-copy strong { font-size: var(--font-size-small); font-weight: var(--font-weight-medium); }.video-copy small { color: var(--color-text-secondary); font: var(--font-size-caption) var(--font-family-mono); }.video-copy i { font-style: normal; padding: 0 3px; }
.status-pill { display: inline-flex; align-items: center; border-radius: var(--radius-full); padding: 5px 9px; font-size: var(--font-size-caption); white-space: nowrap; }
.status-scheduled { color: var(--color-status-info-text); background: var(--color-status-info-soft); }.status-published { color: var(--color-status-success-text); background: var(--color-status-success-soft); }.status-draft { color: var(--color-text-secondary); background: var(--color-background-sunken); }
.date-cell { white-space: nowrap; font-size: var(--font-size-small); }
.table-state { text-align: center; padding: 42px 16px; color: var(--color-text-secondary); }.table-state strong,.table-state span { display: block; }.table-state strong { color: var(--color-text-primary); margin-bottom: 6px; }
.table-footer { display: flex; justify-content: space-between; align-items: center; gap: 14px; padding: 12px 18px; color: var(--color-text-secondary); font-size: var(--font-size-small); }
.pagination { display: flex; align-items: center; gap: 5px; }.pagination button { min-width: 34px; min-height: 34px; border-color: transparent; color: var(--color-action-primary); }.pagination button.selected { color: white; background: var(--color-action-primary); }.pagination button:disabled { opacity: .45; cursor: not-allowed; }
@media (max-width: 850px) { .period-card { flex-wrap: wrap; }.period-label { width: 100%; }.library-heading { align-items: flex-start; flex-direction: column; }.stats-card { grid-template-columns: 1fr; }.stat-item + .stat-item { border-left: 0; border-top: 1px solid var(--color-border-default); }.date-cell { min-width: 160px; } }
@media (max-width: 540px) { .date-control { width: 100%; justify-content: space-between; }.date-control input { min-width: 0; width: 62%; }.period-card .button-primary { flex: 1; }.table-footer { align-items: flex-start; flex-direction: column; }.video-cell { min-width: 230px; } }
</style>
