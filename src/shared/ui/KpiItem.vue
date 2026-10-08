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
  <div
    class="ui-kpi-item"
    :class="`ui-kpi-item--${status}`"
    role="group"
    :aria-label="label"
  >
    <span class="ui-kpi-item__icon" aria-hidden="true">
      <component :is="icon" class="ui-kpi-item__icon-svg" :stroke-width="2" />
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
  background: var(--color-background-surface);
  border: var(--border-width-default) solid var(--color-border-default);
  border-radius: var(--radius-lg);
  display: flex;
  gap: var(--space-3);
  padding: var(--space-4);
}

.ui-kpi-item__icon {
  align-items: center;
  background: var(--color-background-sunken);
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  display: inline-flex;
  flex: 0 0 auto;
  height: var(--control-height-standard);
  justify-content: center;
  width: var(--control-height-standard);
}

.ui-kpi-item__icon-svg {
  height: var(--icon-size-medium);
  width: var(--icon-size-medium);
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
  background: var(--color-status-info-soft);
  color: var(--color-status-info-text);
}

.ui-kpi-item--success .ui-kpi-item__icon {
  background: var(--color-status-success-soft);
  color: var(--color-status-success-text);
}

.ui-kpi-item--warning .ui-kpi-item__icon {
  background: var(--color-status-warning-soft);
  color: var(--color-status-warning-text);
}

.ui-kpi-item--danger .ui-kpi-item__icon {
  background: var(--color-status-danger-soft);
  color: var(--color-status-danger-text);
}
</style>
