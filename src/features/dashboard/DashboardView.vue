<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import DashboardFilters from './components/DashboardFilters.vue'
import PublicationList from './components/PublicationList.vue'
import StatusSummary from './components/StatusSummary.vue'
import { getMockPublications } from './dashboard.mock'
import type {
  DashboardDateFilters,
  Publication,
  PublicationStatus,
  PublicationStatusFilter,
} from './dashboard.types'
import { STATUS_FILTER_LABELS } from './dashboard.types'

const defaultFilters: DashboardDateFilters = {
  from: '2026-09-01',
  to: '2026-09-30',
}

const filters = reactive<DashboardDateFilters>({ ...defaultFilters })
const publications = ref<Publication[]>([])
const activeStatus = ref<PublicationStatusFilter>('all')
const isLoading = ref(false)
const hasLoaded = ref(false)
const errorMessage = ref('')
let requestSequence = 0

const counts = computed<Record<PublicationStatus, number>>(() => ({
  scheduled: publications.value.filter(({ status }) => status === 'scheduled').length,
  published: publications.value.filter(({ status }) => status === 'published').length,
  failed: publications.value.filter(({ status }) => status === 'failed').length,
}))

const visiblePublications = computed(() => {
  if (activeStatus.value === 'all') {
    return publications.value
  }

  return publications.value.filter(({ status }) => status === activeStatus.value)
})

const activeStatusLabel = computed(() => STATUS_FILTER_LABELS[activeStatus.value])

async function loadDashboard(): Promise<void> {
  const currentRequest = ++requestSequence
  isLoading.value = true
  errorMessage.value = ''
  hasLoaded.value = false

  try {
    const nextPublications = await getMockPublications(filters)

    if (currentRequest !== requestSequence) {
      return
    }

    publications.value = nextPublications
    hasLoaded.value = true
  } catch (error) {
    if (currentRequest !== requestSequence) {
      return
    }

    publications.value = []
    errorMessage.value = error instanceof Error ? error.message : 'No fue posible cargar las publicaciones.'
  } finally {
    if (currentRequest === requestSequence) {
      isLoading.value = false
    }
  }
}

function resetFilters(): void {
  filters.from = defaultFilters.from
  filters.to = defaultFilters.to
  activeStatus.value = 'all'
  void loadDashboard()
}

onMounted(() => {
  void loadDashboard()
})
</script>

<template>
  <div class="dashboard-page">
    <header class="topbar">
      <div class="brand" aria-label="PubTube panel editorial">
        <span class="brand-mark" aria-hidden="true">PT</span>
        <span class="brand-name">PubTube</span>
        <span class="brand-context">Panel editorial</span>
      </div>
      <div class="environment">
        <span class="environment-dot" aria-hidden="true"></span>
        Entorno local · Datos de demostración
      </div>
    </header>

    <main class="dashboard-main">
      <section class="page-heading" aria-labelledby="page-title">
        <div>
          <p class="eyebrow">Módulo 4 · Publicaciones</p>
          <h1 id="page-title">Dashboard editorial</h1>
          <p class="page-description">
            Visualiza el estado de tus publicaciones y encuentra rápidamente los elementos que necesitan atención.
          </p>
        </div>
        <button class="primary-button" type="button" :disabled="isLoading" @click="loadDashboard">
          <span class="icon" aria-hidden="true">↻</span>
          Actualizar datos
        </button>
      </section>

      <StatusSummary
        v-if="!isLoading && !errorMessage"
        :counts="counts"
        :active-status="activeStatus"
        @select="activeStatus = $event"
      />

      <DashboardFilters
        :from="filters.from"
        :to="filters.to"
        :disabled="isLoading"
        @update:from="filters.from = $event"
        @update:to="filters.to = $event"
        @reset="resetFilters"
        @apply="loadDashboard"
      />

      <section v-if="isLoading" class="state-card" role="status" aria-live="polite">
        <span class="loading-spinner" aria-hidden="true"></span>
        <h2>Cargando publicaciones</h2>
        <div class="skeleton-stack" aria-hidden="true">
          <span class="skeleton-line"></span>
          <span class="skeleton-line"></span>
          <span class="skeleton-line"></span>
        </div>
      </section>

      <section v-else-if="errorMessage" class="state-card" role="alert">
        <span class="state-icon state-icon--error" aria-hidden="true">!</span>
        <h2>No pudimos cargar el dashboard</h2>
        <p>Revisa el rango seleccionado e inténtalo nuevamente.</p>
        <p class="error-detail">{{ errorMessage }}</p>
        <button class="secondary-button" type="button" @click="loadDashboard">Reintentar</button>
      </section>

      <PublicationList
        v-else
        :publications="visiblePublications"
        :status-label="activeStatusLabel"
        @clear-filters="resetFilters"
      />

      <p v-if="hasLoaded" class="filter-hint" aria-live="polite">
        <span class="filter-hint-dot" aria-hidden="true"></span>
        Vista actualizada con {{ visiblePublications.length }} publicaciones.
      </p>
    </main>
  </div>
</template>
