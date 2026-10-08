<script setup lang="ts">
import { RotateCcw } from '@lucide/vue'
import { Button, DateField, IconButton } from '../../../shared/ui'

withDefaults(
  defineProps<{
    from: string
    to: string
    disabled?: boolean
    fromError?: string
    toError?: string
  }>(),
  {
    disabled: false,
    fromError: '',
    toError: '',
  },
)

const emit = defineEmits<{
  'update:from': [value: string]
  'update:to': [value: string]
  apply: []
  reset: []
}>()
</script>

<template>
  <section class="dashboard-filters" aria-labelledby="dashboard-filters-title">
    <div class="dashboard-filters__heading">
      <div>
        <p class="dashboard-filters__eyebrow">Período</p>
        <h2 id="dashboard-filters-title" class="dashboard-filters__title">
          Filtra las publicaciones por fecha
        </h2>
      </div>

      <IconButton
        :icon="RotateCcw"
        label="Restablecer filtros"
        title="Restablecer filtros"
        size="small"
        :disabled="disabled"
        @click="emit('reset')"
      />
    </div>

    <div class="dashboard-filters__controls">
      <DateField
        id="dashboard-date-from"
        label="Desde"
        :model-value="from"
        :disabled="disabled"
        :error="fromError"
        @update:model-value="emit('update:from', $event)"
      />
      <DateField
        id="dashboard-date-to"
        label="Hasta"
        :model-value="to"
        :disabled="disabled"
        :error="toError"
        @update:model-value="emit('update:to', $event)"
      />
      <Button variant="primary" :disabled="disabled" @click="emit('apply')">
        Aplicar
      </Button>
    </div>
  </section>
</template>

<style scoped>
.dashboard-filters {
  background: var(--color-background-surface);
  border: var(--border-width-default) solid var(--color-border-default);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
}

.dashboard-filters__heading {
  align-items: flex-start;
  display: flex;
  gap: var(--space-4);
  justify-content: space-between;
}

.dashboard-filters__eyebrow {
  color: var(--color-action-primary);
  font-size: var(--font-size-caption);
  font-weight: var(--font-weight-bold);
  margin: 0;
  text-transform: uppercase;
}

.dashboard-filters__title {
  color: var(--color-text-primary);
  font-size: var(--font-size-heading-3);
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-heading-3);
  margin: var(--space-1) 0 0;
}

.dashboard-filters__controls {
  align-items: end;
  display: grid;
  gap: var(--space-4);
  grid-template-columns: repeat(2, minmax(0, 1fr)) auto;
  margin-top: var(--space-5);
}

.dashboard-filters__controls :deep(.ui-button) {
  min-width: var(--space-16);
}

@media (max-width: 599px) {
  .dashboard-filters__controls {
    grid-template-columns: 1fr;
  }

  .dashboard-filters__controls :deep(.ui-button) {
    width: 100%;
  }
}
</style>
