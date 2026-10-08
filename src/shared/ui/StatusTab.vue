<script setup lang="ts">
withDefaults(
  defineProps<{
    label: string
    count?: number
    active?: boolean
    disabled?: boolean
  }>(),
  {
    count: undefined,
    active: false,
    disabled: false,
  },
)

const emit = defineEmits<{
  select: []
}>()
</script>

<template>
  <button
    class="ui-status-tab"
    :class="{ 'ui-status-tab--active': active }"
    type="button"
    role="tab"
    :aria-selected="active"
    :disabled="disabled"
    @click="emit('select')"
  >
    <span>{{ label }}</span>
    <span v-if="count !== undefined" class="ui-status-tab__count">{{ count }}</span>
  </button>
</template>

<style scoped>
.ui-status-tab {
  align-items: center;
  background: transparent;
  border: 0;
  border-bottom: var(--focus-ring-width) solid transparent;
  color: var(--color-text-secondary);
  display: inline-flex;
  font-size: var(--font-size-small);
  font-weight: var(--font-weight-semibold);
  gap: var(--space-2);
  min-height: var(--control-height-standard);
  padding: 0 var(--space-3);
  white-space: nowrap;
}

.ui-status-tab:hover:not(:disabled) {
  background: var(--color-background-sunken);
  color: var(--color-text-primary);
}

.ui-status-tab--active {
  border-bottom-color: var(--color-action-primary);
  color: var(--color-action-primary);
}

.ui-status-tab:disabled {
  cursor: not-allowed;
}

.ui-status-tab__count {
  align-items: center;
  background: var(--color-background-sunken);
  border-radius: var(--radius-full);
  color: var(--color-text-secondary);
  display: inline-flex;
  font-size: var(--font-size-caption);
  justify-content: center;
  min-width: var(--space-5);
  padding: 0 var(--space-1);
}

.ui-status-tab--active .ui-status-tab__count {
  background: var(--color-status-info-soft);
  color: var(--color-status-info-text);
}
</style>
