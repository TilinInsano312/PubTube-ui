<script setup lang="ts">
import type { Component } from 'vue'

withDefaults(
  defineProps<{
    label: string
    value: number | string
    icon: Component
    status?: 'neutral' | 'info' | 'success' | 'warning' | 'danger'
  }>(),
  {
    status: 'neutral',
  },
)
</script>

<template>
  <div class="ui-kpi-item" :class="`ui-kpi-item--${status}`" role="group" :aria-label="label">
    <span class="ui-kpi-item__icon" aria-hidden="true">
      <component :is="icon" :size="20" :stroke-width="2" />
    </span>
    <span class="ui-kpi-item__copy">
      <span class="ui-kpi-item__label">{{ label }}</span>
      <strong class="ui-kpi-item__value">{{ value }}</strong>
    </span>
  </div>
</template>

<style scoped>
.ui-kpi-item {
  align-items: center;
  background: var(--color-surface-default);
  border: var(--border-width-default) solid var(--color-border-default);
  border-radius: var(--radius-lg);
  display: flex;
  gap: var(--space-3);
  padding: var(--space-4);
}

.ui-kpi-item__icon {
  align-items: center;
  background: var(--color-surface-subtle);
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  display: inline-flex;
  flex: 0 0 auto;
  height: var(--control-height-standard);
  justify-content: center;
  width: var(--control-height-standard);
}

.ui-kpi-item__copy {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  min-width: 0;
}

.ui-kpi-item__label {
  color: var(--color-text-secondary);
  font-size: var(--font-size-small);
}

.ui-kpi-item__value {
  color: var(--color-text-primary);
  font-size: var(--font-size-heading-2);
  line-height: var(--line-height-heading-2);
}

.ui-kpi-item--info .ui-kpi-item__icon {
  background: var(--color-status-info-background);
  color: var(--color-status-info-foreground);
}

.ui-kpi-item--success .ui-kpi-item__icon {
  background: var(--color-status-success-background);
  color: var(--color-status-success-foreground);
}

.ui-kpi-item--warning .ui-kpi-item__icon {
  background: var(--color-status-warning-background);
  color: var(--color-status-warning-foreground);
}

.ui-kpi-item--danger .ui-kpi-item__icon {
  background: var(--color-status-danger-background);
  color: var(--color-status-danger-foreground);
}
</style>
