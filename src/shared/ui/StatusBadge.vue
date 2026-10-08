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
  background: var(--color-surface-subtle);
  border-color: var(--color-border-default);
  color: var(--color-text-secondary);
}

.ui-status-badge--neutral .ui-status-badge__marker {
  background: var(--color-neutral-500);
}

.ui-status-badge--info {
  background: var(--color-status-info-background);
  border-color: var(--color-status-info-border);
  color: var(--color-status-info-foreground);
}

.ui-status-badge--info .ui-status-badge__marker {
  background: var(--color-status-info-border);
}

.ui-status-badge--success {
  background: var(--color-status-success-background);
  border-color: var(--color-status-success-border);
  color: var(--color-status-success-foreground);
}

.ui-status-badge--success .ui-status-badge__marker {
  background: var(--color-status-success-border);
}

.ui-status-badge--warning {
  background: var(--color-status-warning-background);
  border-color: var(--color-status-warning-border);
  color: var(--color-status-warning-foreground);
}

.ui-status-badge--warning .ui-status-badge__marker {
  background: var(--color-status-warning-border);
}

.ui-status-badge--danger {
  background: var(--color-status-danger-background);
  border-color: var(--color-status-danger-border);
  color: var(--color-status-danger-foreground);
}

.ui-status-badge--danger .ui-status-badge__marker {
  background: var(--color-status-danger-border);
}
</style>
