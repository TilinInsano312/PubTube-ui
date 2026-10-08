<script setup lang="ts">
import { computed, onMounted, reactive } from 'vue'
import { Bell, RefreshCw } from '@lucide/vue'
import type { DashboardErrorCode } from '../../api/dashboard.types'
import AppShell from '../../layouts/AppShell.vue'
import { Button, IconButton } from '../../shared/ui'
import DashboardFilters from './components/DashboardFilters.vue'
import KpiSummary from './components/KpiSummary.vue'
import PublicationTable from './components/PublicationTable.vue'
import type { DashboardDateFilters } from './dashboard.types'
import { useDashboardCounts } from './useDashboardCounts'

const defaultFilters: DashboardDateFilters = {
  from: '',
  to: '',
}

const filters = reactive<DashboardDateFilters>({ ...defaultFilters })
const dashboard = useDashboardCounts()
const counts = dashboard.counts

const errorCopy: Record<DashboardErrorCode, { title: string; description: string }> = {
  UNAUTHORIZED: {
    title: 'Dashboard no autorizado',
    description: 'No tienes autorización para consultar los conteos de publicaciones.',
  },
  INVALID_DATE_RANGE: {
    title: 'Revisa el rango de fechas seleccionado.',
    description: 'Selecciona un rango válido e inténtalo nuevamente.',
  },
  RATE_LIMIT_EXCEEDED: {
    title: 'Se realizaron demasiadas solicitudes.',
    description: 'Intenta nuevamente en unos momentos.',
  },
  DASHBOARD_ERROR: {
    title: 'No pudimos cargar el dashboard.',
    description: 'Intenta nuevamente.',
  },
  DASHBOARD_UNAVAILABLE: {
    title: 'Dashboard no disponible',
    description: 'Los datos de publicaciones no están disponibles en este momento.',
  },
  DASHBOARD_TIMEOUT: {
    title: 'No pudimos cargar el dashboard.',
    description: 'Intenta nuevamente.',
  },
  NETWORK_ERROR: {
    title: 'No pudimos conectar con el dashboard.',
    description: 'Comprueba la conexión e inténtalo nuevamente.',
  },
  INVALID_RESPONSE: {
    title: 'No pudimos interpretar la respuesta del dashboard.',
    description: 'Intenta nuevamente.',
  },
}

const dateRangeError = computed(() => {
  if (!filters.from || !filters.to || filters.from <= filters.to) {
    return ''
  }

  return 'La fecha Desde debe ser anterior o igual a Hasta.'
})

const isBusy = computed(
  () => dashboard.state.value === 'idle' || dashboard.isLoading.value,
)

const hasCounts = computed(() => {
  const counts = dashboard.counts.value
  return counts.scheduled + counts.published + counts.failed > 0
})

const isError = computed(() => dashboard.state.value === 'error')

const currentErrorCopy = computed(
  () => errorCopy[dashboard.error.value?.code ?? 'NETWORK_ERROR'],
)

const detailEmptyTitle = computed(() =>
  hasCounts.value ? 'Detalle de publicaciones no disponible' : '',
)

const detailEmptyDescription = computed(() =>
  hasCounts.value
    ? 'Los conteos están disponibles; el backend aún no entrega publicaciones individuales.'
    : '',
)

async function loadDashboard(): Promise<void> {
  if (dateRangeError.value) {
    return
  }

  await dashboard.load({
    from: filters.from || undefined,
    to: filters.to || undefined,
  })
}

function resetFilters(): void {
  filters.from = defaultFilters.from
  filters.to = defaultFilters.to
  void loadDashboard()
}

onMounted(() => {
  void loadDashboard()
})
</script>

<template>
  <AppShell
    title="Dashboard editorial"
    description="Visualiza los conteos de publicaciones y el estado disponible de tu operación editorial."
  >
    <template #actions>
      <IconButton
        :icon="Bell"
        label="Notificaciones"
        title="Notificaciones no disponibles"
        disabled
      />
      <IconButton
        :icon="RefreshCw"
        label="Actualizar dashboard"
        :loading="isBusy"
        @click="loadDashboard"
      />
    </template>

    <div class="dashboard-workspace">
      <DashboardFilters
        :from="filters.from"
        :to="filters.to"
        :disabled="isBusy"
        :from-error="dateRangeError"
        :to-error="dateRangeError"
        @update:from="filters.from = $event"
        @update:to="filters.to = $event"
        @reset="resetFilters"
        @apply="loadDashboard"
      />

      <KpiSummary :counts="counts" :loading="isBusy" />

      <section v-if="isError" class="dashboard-error" role="alert" aria-labelledby="dashboard-error-title">
        <h2 id="dashboard-error-title" class="dashboard-error__title">
          {{ currentErrorCopy.title }}
        </h2>
        <p class="dashboard-error__description">{{ currentErrorCopy.description }}</p>
        <Button variant="secondary" :disabled="isBusy" @click="loadDashboard">
          Intentar nuevamente
        </Button>
      </section>

      <PublicationTable
        v-else
        :items="[]"
        :loading="isBusy"
        :empty-title="detailEmptyTitle"
        :empty-description="detailEmptyDescription"
      />
    </div>
  </AppShell>
</template>

<style scoped>
.dashboard-workspace {
  display: grid;
  gap: var(--space-6);
}

.dashboard-error {
  background: var(--color-status-danger-soft);
  border: var(--border-width-default) solid var(--color-status-danger-solid);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
}

.dashboard-error__title {
  color: var(--color-status-danger-text);
  font-size: var(--font-size-heading-3);
  line-height: var(--line-height-heading-3);
  margin: 0;
}

.dashboard-error__description {
  color: var(--color-text-primary);
  margin: var(--space-2) 0 var(--space-4);
}
</style>
