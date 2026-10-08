<script setup lang="ts">
import type { Component } from 'vue'

withDefaults(
  defineProps<{
    label: string
    icon: Component
    active?: boolean
    disabled?: boolean
  }>(),
  {
    active: false,
    disabled: false,
  },
)
</script>

<template>
  <button
    class="ui-navigation-item"
    :class="{ 'ui-navigation-item--active': active }"
    type="button"
    :aria-label="label"
    :aria-current="active ? 'page' : undefined"
    :disabled="disabled"
    :title="label"
  >
    <component :is="icon" :size="20" :stroke-width="2" aria-hidden="true" />
    <span class="ui-navigation-item__label">{{ label }}</span>
  </button>
</template>

<style scoped>
.ui-navigation-item {
  align-items: center;
  background: transparent;
  border: var(--border-width-default) solid transparent;
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  display: flex;
  gap: var(--space-3);
  justify-content: flex-start;
  min-height: var(--control-height-standard);
  padding: 0 var(--space-3);
  text-align: left;
  transition:
    background-color var(--motion-duration-standard) var(--motion-easing-standard),
    color var(--motion-duration-standard) var(--motion-easing-standard);
  width: 100%;
}

.ui-navigation-item:hover:not(:disabled),
.ui-navigation-item--active {
  background: var(--color-surface-selected);
  color: var(--color-action-primary);
}

.ui-navigation-item--active {
  font-weight: var(--font-weight-semibold);
}

.ui-navigation-item:disabled {
  cursor: not-allowed;
}

@media (max-width: 899px) {
  .ui-navigation-item__label {
    display: none;
  }

  .ui-navigation-item {
    justify-content: center;
    padding: 0;
  }
}
</style>
