<script setup lang="ts">
import { ref } from 'vue'
import type { Component } from 'vue'

const button = ref<HTMLButtonElement | null>(null)

defineExpose({
  focus: () => button.value?.focus(),
})

withDefaults(
  defineProps<{
    icon: Component
    label: string
    type?: 'button' | 'submit' | 'reset'
    disabled?: boolean
    pressed?: boolean
    expanded?: boolean
    loading?: boolean
    size?: 'small' | 'medium' | 'large'
  }>(),
  {
    type: 'button',
    disabled: false,
    pressed: undefined,
    expanded: undefined,
    loading: false,
    size: 'medium',
  },
)
</script>

<template>
  <button
    ref="button"
    class="ui-icon-button"
    :class="`ui-icon-button--${size}`"
    :type="type"
    :aria-label="label"
    :aria-pressed="pressed"
    :aria-expanded="expanded"
    :aria-busy="loading || undefined"
    :disabled="disabled || loading"
  >
    <component
      :is="icon"
      class="ui-icon-button__icon"
      :stroke-width="2"
      aria-hidden="true"
    />
  </button>
</template>

<style scoped>
.ui-icon-button {
  align-items: center;
  background: transparent;
  border: var(--border-width-default) solid transparent;
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  display: inline-flex;
  justify-content: center;
  transition:
    background-color var(--motion-duration-standard) var(--motion-easing-standard),
    border-color var(--motion-duration-standard) var(--motion-easing-standard),
    color var(--motion-duration-standard) var(--motion-easing-standard);
}

.ui-icon-button--small {
  height: var(--control-height-compact);
  width: var(--control-height-compact);
}

.ui-icon-button--medium {
  height: var(--control-height-standard);
  width: var(--control-height-standard);
}

.ui-icon-button--large {
  height: var(--space-12);
  width: var(--space-12);
}

.ui-icon-button__icon {
  height: var(--icon-size-medium);
  width: var(--icon-size-medium);
}

.ui-icon-button--small .ui-icon-button__icon {
  height: var(--icon-size-small);
  width: var(--icon-size-small);
}

.ui-icon-button--large .ui-icon-button__icon {
  height: var(--icon-size-large);
  width: var(--icon-size-large);
}

.ui-icon-button:hover:not(:disabled),
.ui-icon-button[aria-pressed='true'] {
  background: var(--color-background-sunken);
  color: var(--color-text-primary);
}

.ui-icon-button:disabled {
  color: var(--color-action-primary-disabled-content);
  cursor: not-allowed;
}
</style>
