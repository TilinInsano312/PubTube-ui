<script setup lang="ts">
import type { PublicationStatus, PublicationStatusFilter } from '../dashboard.types'
import { STATUS_LABELS } from '../dashboard.types'

defineProps<{
  counts: Record<PublicationStatus, number>
  activeStatus: PublicationStatusFilter
}>()

const emit = defineEmits<{
  select: [status: PublicationStatusFilter]
}>()

const cards: { status: PublicationStatusFilter; label: string; icon: string }[] = [
  { status: 'all', label: 'Total publicaciones', icon: '▦' },
  { status: 'scheduled', label: STATUS_LABELS.scheduled, icon: '◷' },
  { status: 'published', label: STATUS_LABELS.published, icon: '✓' },
  { status: 'failed', label: STATUS_LABELS.failed, icon: '!' },
]
</script>

<template>
  <section class="summary-grid" aria-label="Resumen de publicaciones">
    <button
      v-for="card in cards"
      :key="card.status"
      class="summary-card"
      :class="{ 'is-active': activeStatus === card.status }"
      :data-status="card.status"
      type="button"
      :aria-pressed="activeStatus === card.status"
      @click="emit('select', card.status)"
    >
      <span class="summary-card-header">
        <span>{{ card.label }}</span>
        <span class="summary-icon" aria-hidden="true">{{ card.icon }}</span>
      </span>
      <strong class="summary-count">
        {{ card.status === 'all' ? counts.scheduled + counts.published + counts.failed : counts[card.status] }}
      </strong>
      <span class="summary-caption">En el rango seleccionado</span>
    </button>
  </section>
</template>
