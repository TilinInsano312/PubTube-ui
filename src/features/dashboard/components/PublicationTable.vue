<script setup lang="ts">
import { computed, ref, useId } from 'vue'
import { StatusBadge, StatusTab } from '../../../shared/ui'
import type {
  PublicationListItem,
  PublicationStatus,
  PublicationStatusFilter,
} from '../dashboard.types'

const props = withDefaults(
  defineProps<{
    items: PublicationListItem[]
    loading?: boolean
    emptyTitle?: string
    emptyDescription?: string
  }>(),
  {
    loading: false,
    emptyTitle: '',
    emptyDescription: '',
  },
)

const emit = defineEmits<{
  select: [status: PublicationStatusFilter]
}>()

const activeStatus = ref<PublicationStatusFilter>('all')
const titleId = useId()

const statusMetadata: Record<
  PublicationStatus,
  { label: string; tabLabel: string; tone: 'info' | 'success' | 'danger' }
> = {
  scheduled: { label: 'Programada', tabLabel: 'Programadas', tone: 'info' },
  published: { label: 'Publicada', tabLabel: 'Publicadas', tone: 'success' },
  failed: { label: 'Fallida', tabLabel: 'Fallidas', tone: 'danger' },
}

const tabs: { status: PublicationStatusFilter; label: string }[] = [
  { status: 'all', label: 'Todas' },
  { status: 'scheduled', label: statusMetadata.scheduled.tabLabel },
  { status: 'published', label: statusMetadata.published.tabLabel },
  { status: 'failed', label: statusMetadata.failed.tabLabel },
]

const visibleItems = computed(() => {
  if (activeStatus.value === 'all') {
    return props.items
  }

  return props.items.filter((item) => item.status === activeStatus.value)
})

function countFor(status: PublicationStatusFilter): number {
  if (status === 'all') {
    return props.items.length
  }

  return props.items.filter((item) => item.status === status).length
}

function selectStatus(status: PublicationStatusFilter): void {
  activeStatus.value = status
  emit('select', status)
}

function emptyTitle(): string {
  if (props.emptyTitle) {
    return props.emptyTitle
  }

  if (activeStatus.value === 'all') {
    return 'No hay publicaciones en este período.'
  }

  return `No hay publicaciones ${statusMetadata[activeStatus.value].tabLabel.toLowerCase()} en este período.`
}

function emptyDescription(): string {
  if (props.emptyDescription) {
    return props.emptyDescription
  }

  return activeStatus.value === 'all'
    ? 'Prueba con otro rango de fechas.'
    : 'Prueba con otro estado o rango de fechas.'
}
</script>

<template>
  <section class="publication-table" :aria-labelledby="titleId">
    <div class="publication-table__heading">
      <div>
        <p class="publication-table__eyebrow">Publicaciones</p>
        <h2 :id="titleId" class="publication-table__title">
          Detalle de publicaciones
        </h2>
      </div>
    </div>

    <div
      class="publication-table__tabs"
      role="tablist"
      aria-label="Filtrar publicaciones por estado"
    >
      <StatusTab
        v-for="tab in tabs"
        :key="tab.status"
        :label="tab.label"
        :count="countFor(tab.status)"
        :active="activeStatus === tab.status"
        :disabled="props.loading"
        @select="selectStatus(tab.status)"
      />
    </div>

    <div
      v-if="props.loading"
      class="publication-table__loading"
      role="status"
      aria-live="polite"
    >
      <span class="publication-table__loading-label"
        >Cargando publicaciones</span
      >
      <span
        v-for="row in 3"
        :key="row"
        class="publication-table__skeleton-row"
        aria-hidden="true"
      >
        <span
          class="publication-table__skeleton-cell publication-table__skeleton-cell--wide"
        ></span>
        <span class="publication-table__skeleton-cell"></span>
        <span class="publication-table__skeleton-cell"></span>
      </span>
    </div>

    <div
      v-else-if="visibleItems.length === 0"
      class="publication-table__empty"
      role="status"
    >
      <h3>{{ emptyTitle() }}</h3>
      <p>{{ emptyDescription() }}</p>
    </div>

    <div v-else class="publication-table__scroll">
      <table>
        <caption class="publication-table__caption">
          Publicaciones del período seleccionado
        </caption>
        <thead>
          <tr>
            <th scope="col">Contenido</th>
            <th scope="col">Estado</th>
            <th scope="col">Fecha programada</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in visibleItems" :key="item.id">
            <th scope="row">
              <span class="publication-table__content-label">{{
                item.contentLabel
              }}</span>
              <span v-if="item.contentId" class="publication-table__content-id">
                {{ item.contentId }}
              </span>
            </th>
            <td>
              <StatusBadge
                :label="statusMetadata[item.status].label"
                :tone="statusMetadata[item.status].tone"
              />
            </td>
            <td>
              <time :datetime="item.scheduledAt">{{ item.scheduledAt }}</time>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<style scoped>
.publication-table {
  background: var(--color-background-surface);
  border: var(--border-width-default) solid var(--color-border-default);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.publication-table__heading {
  padding: var(--space-5) var(--space-5) var(--space-4);
}

.publication-table__eyebrow {
  color: var(--color-action-primary);
  font-size: var(--font-size-caption);
  font-weight: var(--font-weight-bold);
  margin: 0;
  text-transform: uppercase;
}

.publication-table__title {
  color: var(--color-text-primary);
  font-size: var(--font-size-heading-2);
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-heading-2);
  margin: var(--space-1) 0 0;
}

.publication-table__tabs {
  border-bottom: var(--border-width-default) solid var(--color-border-default);
  display: flex;
  gap: var(--space-1);
  overflow-x: auto;
  padding: 0 var(--space-4);
}

.publication-table__scroll {
  overflow-x: auto;
}

table {
  border-collapse: collapse;
  min-width: 100%;
  text-align: left;
}

th,
td {
  border-bottom: var(--border-width-default) solid var(--color-border-default);
  padding: var(--space-4) var(--space-5);
  vertical-align: middle;
}

thead th {
  color: var(--color-text-secondary);
  font-size: var(--font-size-caption);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
}

tbody th {
  color: var(--color-text-primary);
  font-weight: var(--font-weight-semibold);
}

tbody td {
  color: var(--color-text-secondary);
}

tbody tr:last-child th,
tbody tr:last-child td {
  border-bottom: 0;
}

.publication-table__caption {
  color: var(--color-text-secondary);
  font-size: var(--font-size-small);
  padding: var(--space-4) var(--space-5) 0;
  text-align: left;
}

.publication-table__content-label,
.publication-table__content-id {
  display: block;
}

.publication-table__content-id {
  color: var(--color-text-secondary);
  font-size: var(--font-size-caption);
  font-weight: var(--font-weight-regular);
  margin-top: var(--space-1);
}

.publication-table__loading,
.publication-table__empty {
  padding: var(--space-10) var(--space-5);
}

.publication-table__loading {
  display: grid;
  gap: var(--space-3);
}

.publication-table__loading-label {
  color: var(--color-text-secondary);
  font-size: var(--font-size-small);
}

.publication-table__skeleton-row {
  display: grid;
  gap: var(--space-4);
  grid-template-columns: 2fr 1fr 1fr;
}

.publication-table__skeleton-cell {
  background: var(--color-background-sunken);
  border-radius: var(--radius-sm);
  display: block;
  height: var(--space-4);
}

.publication-table__skeleton-cell--wide {
  min-width: var(--space-16);
}

.publication-table__empty {
  text-align: center;
}

.publication-table__empty h3 {
  color: var(--color-text-primary);
  font-size: var(--font-size-heading-3);
  margin: 0;
}

.publication-table__empty p {
  color: var(--color-text-secondary);
  margin: var(--space-2) 0 0;
}

@media (max-width: 599px) {
  th,
  td {
    padding-inline: var(--space-4);
  }

  .publication-table__heading {
    padding-inline: var(--space-4);
  }
}

@media (max-width: 899px) {
  .publication-table__content-id {
    display: none;
  }
}
</style>
