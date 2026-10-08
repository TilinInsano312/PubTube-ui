<script setup lang="ts">
withDefaults(
  defineProps<{
    tone?: 'neutral' | 'info' | 'success' | 'warning' | 'danger'
    label: string
  }>(),
  {
    tone: 'neutral',
  },
)
</script>

<template>
  <span class="ui-status-badge" :class="`ui-status-badge--${tone}`">
    <span class="ui-status-badge__marker" aria-hidden="true"></span>
    <span>{{ label }}</span>
  </span>
</template>

<style scoped>
.ui-status-badge {
  align-items: center;
  border: var(--border-width-default) solid transparent;
  border-radius: var(--radius-full);
  display: inline-flex;
  font-size: var(--font-size-small);
  font-weight: var(--font-weight-semibold);
  gap: var(--space-2);
  line-height: var(--line-height-small);
  padding: var(--space-1) var(--space-3);
  white-space: nowrap;
}

.ui-status-badge__marker {
  border-radius: var(--radius-full);
  height: var(--space-1);
  width: var(--space-1);
}

.ui-status-badge--neutral {
  background: var(--color-background-sunken);
  border-color: var(--color-border-default);
  color: var(--color-text-secondary);
}

.ui-status-badge--neutral .ui-status-badge__marker {
  background: var(--color-border-strong);
}

.ui-status-badge--info {
  background: var(--color-status-info-soft);
  border-color: var(--color-status-info-solid);
  color: var(--color-status-info-text);
}

.ui-status-badge--info .ui-status-badge__marker {
  background: var(--color-status-info-solid);
}

.ui-status-badge--success {
  background: var(--color-status-success-soft);
  border-color: var(--color-status-success-solid);
  color: var(--color-status-success-text);
}

.ui-status-badge--success .ui-status-badge__marker {
  background: var(--color-status-success-solid);
}

.ui-status-badge--warning {
  background: var(--color-status-warning-soft);
  border-color: var(--color-status-warning-solid);
  color: var(--color-status-warning-text);
}

.ui-status-badge--warning .ui-status-badge__marker {
  background: var(--color-status-warning-solid);
}

.ui-status-badge--danger {
  background: var(--color-status-danger-soft);
  border-color: var(--color-status-danger-solid);
  color: var(--color-status-danger-text);
}

.ui-status-badge--danger .ui-status-badge__marker {
  background: var(--color-status-danger-solid);
}
</style>
