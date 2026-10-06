<script setup lang="ts">
import type { Publication } from '../dashboard.types'
import { STATUS_LABELS } from '../dashboard.types'

defineProps<{
  publications: Publication[]
  statusLabel: string
}>()

const emit = defineEmits<{
  clearFilters: []
}>()

function formatDate(date: string): string {
  return new Intl.DateTimeFormat('es-CL', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  }).format(new Date(`${date}T12:00:00`))
}

function initials(title: string): string {
  return title
    .split(' ')
    .slice(0, 2)
    .map((word) => word[0])
    .join('')
    .toUpperCase()
}
</script>

<template>
  <section class="publication-panel" aria-labelledby="publications-title">
    <div class="publication-heading">
      <div>
        <h2 id="publications-title">Detalle de publicaciones</h2>
        <p>{{ publications.length }} resultados · {{ statusLabel }}</p>
      </div>
      <span class="sync-dot" title="Datos mock cargados" aria-label="Datos cargados"></span>
    </div>

    <ul v-if="publications.length" class="publication-list">
      <li v-for="publication in publications" :key="publication.id" class="publication-row">
        <div class="publication-title">
          <span class="publication-avatar" aria-hidden="true">{{ initials(publication.title) }}</span>
          <div class="publication-main">
            <h3>{{ publication.title }}</h3>
            <p class="publication-meta">
              <strong>{{ publication.id }}</strong> · {{ publication.owner }} · {{ publication.channel }}
            </p>
          </div>
        </div>

        <div class="publication-date publication-meta-column">
          <span class="publication-column-label">Fecha</span>
          <span class="publication-date-detail">{{ formatDate(publication.date) }}</span>
          <span class="publication-date-detail">{{ publication.time }} hrs</span>
        </div>

        <p v-if="publication.error" class="publication-meta publication-meta-column">
          {{ publication.error }}
        </p>
        <span v-else class="publication-meta publication-meta-column">Destino verificado</span>

        <span class="status-badge" :class="`status-badge--${publication.status}`">
          {{ STATUS_LABELS[publication.status] }}
        </span>
      </li>
    </ul>

    <div v-else class="state-card">
      <span class="state-icon state-icon--empty" aria-hidden="true">⌕</span>
      <h2>No hay publicaciones para estos filtros</h2>
      <p>Prueba con un rango de fechas más amplio o muestra todos los estados.</p>
      <button class="secondary-button" type="button" @click="emit('clearFilters')">
        Limpiar filtros
      </button>
    </div>
  </section>
</template>
