<script setup lang="ts">
import type { PublicationStatusFilter } from '../dashboard.types'
import { STATUS_FILTER_LABELS } from '../dashboard.types'

defineProps<{
  from: string
  to: string
  status: PublicationStatusFilter
  isLoading: boolean
}>()

const emit = defineEmits<{
  'update:from': [value: string]
  'update:to': [value: string]
  'update:status': [value: PublicationStatusFilter]
  reset: []
  refresh: []
}>()

const statusOptions = Object.entries(STATUS_FILTER_LABELS) as [PublicationStatusFilter, string][]
</script>

<template>
  <section class="filter-panel" aria-labelledby="filters-title">
    <div class="filter-heading">
      <div>
        <p class="eyebrow">Filtros</p>
        <h2 id="filters-title">Ajusta la vista del dashboard</h2>
      </div>
      <button class="quiet-button" type="button" :disabled="isLoading" @click="emit('reset')">
        Restablecer filtros
      </button>
    </div>

    <div class="filter-controls">
      <div class="field">
        <label for="date-from">Desde</label>
        <input
          id="date-from"
          type="date"
          :value="from"
          @input="emit('update:from', ($event.target as HTMLInputElement).value)"
        />
      </div>

      <div class="field">
        <label for="date-to">Hasta</label>
        <input
          id="date-to"
          type="date"
          :value="to"
          @input="emit('update:to', ($event.target as HTMLInputElement).value)"
        />
      </div>

      <div class="field">
        <label for="status-filter">Estado</label>
        <select
          id="status-filter"
          :value="status"
          @change="emit('update:status', ($event.target as HTMLSelectElement).value as PublicationStatusFilter)"
        >
          <option v-for="[value, label] in statusOptions" :key="value" :value="value">
            {{ label }}
          </option>
        </select>
      </div>

      <button class="secondary-button" type="button" :disabled="isLoading" @click="emit('refresh')">
        <span class="icon" aria-hidden="true">↻</span>
        Actualizar
      </button>
    </div>

    <p class="filter-hint">
      <span class="filter-hint-dot" aria-hidden="true"></span>
      Los datos se actualizan al cambiar el rango de fechas.
    </p>
  </section>
</template>
