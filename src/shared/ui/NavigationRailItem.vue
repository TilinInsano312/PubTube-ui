<script setup lang="ts">
import type { Component } from 'vue'

withDefaults(
  defineProps<{
    label: string
    icon: Component
    active?: boolean
    disabled?: boolean
    iconOnly?: boolean
  }>(),
  {
    active: false,
    disabled: false,
    iconOnly: false,
  },
)
</script>

<template>
  <button
    class="ui-navigation-item"
    :class="{
      'ui-navigation-item--active': active,
      'ui-navigation-item--icon-only': iconOnly,
    }"
    type="button"
    :aria-label="label"
    :aria-current="active ? 'page' : undefined"
    :disabled="disabled"
    :title="label"
  >
    <component
      :is="icon"
      class="ui-navigation-item__icon"
      :stroke-width="2"
      aria-hidden="true"
    />
    <span v-if="!iconOnly" class="ui-navigation-item__label">{{ label }}</span>
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
    background-color var(--motion-duration-standard)
      var(--motion-easing-standard),
    color var(--motion-duration-standard) var(--motion-easing-standard);
  width: 100%;
}

.ui-navigation-item:hover:not(:disabled),
.ui-navigation-item--active {
  background: var(--color-action-primary-soft);
  color: var(--color-action-primary);
}

.ui-navigation-item--active {
  font-weight: var(--font-weight-semibold);
}

.ui-navigation-item--icon-only {
  justify-content: center;
  padding: 0;
}

.ui-navigation-item__icon {
  height: var(--icon-size-medium);
  width: var(--icon-size-medium);
}

.ui-navigation-item:disabled {
  cursor: not-allowed;
}
</style>
