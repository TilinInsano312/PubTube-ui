<script setup lang="ts">
withDefaults(
  defineProps<{
    variant?: 'primary' | 'secondary' | 'ghost'
    type?: 'button' | 'submit' | 'reset'
    disabled?: boolean
    loading?: boolean
  }>(),
  {
    variant: 'primary',
    type: 'button',
    disabled: false,
    loading: false,
  },
)
</script>

<template>
  <button
    class="ui-button"
    :class="`ui-button--${variant}`"
    :type="type"
    :disabled="disabled || loading"
    :aria-busy="loading || undefined"
  >
    <span v-if="loading" class="ui-button__spinner" aria-hidden="true"></span>
    <span :class="{ 'ui-button__content--hidden': loading }">
      <slot />
    </span>
  </button>
</template>

<style scoped>
.ui-button {
  align-items: center;
  border: var(--border-width-default) solid transparent;
  border-radius: var(--radius-md);
  display: inline-flex;
  font-size: var(--font-size-body);
  font-weight: var(--font-weight-semibold);
  gap: var(--space-2);
  justify-content: center;
  min-height: var(--control-height-standard);
  padding: 0 var(--space-4);
  transition:
    background-color var(--motion-duration-standard) var(--motion-easing-standard),
    border-color var(--motion-duration-standard) var(--motion-easing-standard),
    color var(--motion-duration-standard) var(--motion-easing-standard);
}

.ui-button:disabled {
  cursor: not-allowed;
}

.ui-button--primary {
  background: var(--color-action-primary);
  color: var(--color-action-primary-content);
}

.ui-button--primary:hover:not(:disabled) {
  background: var(--color-action-primary-hover);
}

.ui-button--primary:active:not(:disabled),
.ui-button--primary[aria-pressed='true'] {
  background: var(--color-action-primary-active);
}

.ui-button--secondary {
  background: var(--color-surface-default);
  border-color: var(--color-border-default);
  color: var(--color-text-primary);
}

.ui-button--secondary:hover:not(:disabled) {
  background: var(--color-surface-subtle);
  border-color: var(--color-border-strong);
}

.ui-button--ghost {
  background: transparent;
  color: var(--color-text-secondary);
}

.ui-button--ghost:hover:not(:disabled) {
  background: var(--color-surface-subtle);
  color: var(--color-text-primary);
}

.ui-button:disabled:not(.ui-button--primary) {
  color: var(--color-action-primary-disabled-content);
}

.ui-button__content--hidden {
  visibility: hidden;
}

.ui-button__spinner {
  animation: ui-button-spin 800ms linear infinite;
  border: var(--border-width-default) solid currentColor;
  border-right-color: transparent;
  border-radius: var(--radius-full);
  height: var(--icon-size-small);
  left: 50%;
  position: absolute;
  width: var(--icon-size-small);
}

.ui-button {
  position: relative;
}

@keyframes ui-button-spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
