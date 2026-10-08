<script setup lang="ts">
withDefaults(
  defineProps<{
    initials: string
    label?: string
  }>(),
  {
    label: 'Avatar',
  },
)
</script>

<template>
  <span class="ui-avatar" :aria-label="label" role="img">
    {{ initials.slice(0, 2).toUpperCase() }}
  </span>
</template>

<style scoped>
.ui-avatar {
  align-items: center;
  background: var(--color-action-primary-soft-strong);
  border: var(--border-width-default) solid var(--color-primary-200);
  border-radius: var(--radius-full);
  color: var(--color-action-primary-active);
  display: inline-flex;
  flex: 0 0 auto;
  font-size: var(--font-size-small);
  font-weight: var(--font-weight-bold);
  height: var(--space-8);
  justify-content: center;
  line-height: 1;
  width: var(--space-8);
}
</style>
