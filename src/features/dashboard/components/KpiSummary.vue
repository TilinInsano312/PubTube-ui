<script setup lang="ts">
import { CheckCircle2, CircleX, Clock3 } from '@lucide/vue'
import { KpiItem } from '../../../shared/ui'
import type { DashboardCounts } from '../../../api/dashboard.types'

withDefaults(
  defineProps<{
    counts: DashboardCounts
    loading?: boolean
  }>(),
  {
    loading: false,
  },
)

const cards = [
  { key: 'scheduled', label: 'Programadas', status: 'info', icon: Clock3 },
  { key: 'published', label: 'Publicadas', status: 'success', icon: CheckCircle2 },
  { key: 'failed', label: 'Fallidas', status: 'danger', icon: CircleX },
] as const
</script>

<template>
  <section
    class="kpi-summary"
    :aria-label="loading ? 'Cargando resumen de publicaciones' : 'Resumen de publicaciones'"
    :aria-busy="loading"
    :aria-live="loading ? 'polite' : undefined"
    :role="loading ? 'status' : undefined"
  >
    <template v-if="loading">
      <div
        v-for="card in cards"
        :key="card.key"
        class="kpi-summary__skeleton"
        aria-hidden="true"
      >
        <span class="kpi-summary__skeleton-icon"></span>
        <span class="kpi-summary__skeleton-copy">
          <span class="kpi-summary__skeleton-label"></span>
          <span class="kpi-summary__skeleton-value"></span>
        </span>
      </div>
    </template>

    <KpiItem
      v-for="card in cards"
      v-else
      :key="card.key"
      :label="card.label"
      :value="counts[card.key]"
      :status="card.status"
      :icon="card.icon"
    />
  </section>
</template>

<style scoped>
.kpi-summary {
  display: grid;
  gap: var(--space-4);
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.kpi-summary__skeleton {
  align-items: center;
  background: var(--color-background-surface);
  border: var(--border-width-default) solid var(--color-border-default);
  border-radius: var(--radius-lg);
  display: flex;
  gap: var(--space-3);
  min-height: var(--space-16);
  padding: var(--space-4);
}

.kpi-summary__skeleton-icon {
  background: var(--color-background-sunken);
  border-radius: var(--radius-md);
  flex: 0 0 auto;
  height: var(--control-height-standard);
  width: var(--control-height-standard);
}

.kpi-summary__skeleton-copy {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.kpi-summary__skeleton-label,
.kpi-summary__skeleton-value {
  background: var(--color-background-sunken);
  border-radius: var(--radius-sm);
  display: block;
}

.kpi-summary__skeleton-label {
  height: var(--space-2);
  width: var(--space-16);
}

.kpi-summary__skeleton-value {
  height: var(--space-4);
  width: var(--space-10);
}

@media (max-width: 899px) {
  .kpi-summary {
    grid-template-columns: 1fr;
  }
}
</style>
