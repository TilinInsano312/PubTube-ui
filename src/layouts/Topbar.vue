<script setup lang="ts">
import { Menu } from '@lucide/vue'
import { IconButton } from '../shared/ui'

defineProps<{
  title: string
  description?: string
  navigationOpen?: boolean
}>()

const emit = defineEmits<{
  toggleNavigation: []
}>()
</script>

<template>
  <header class="topbar">
    <div class="topbar__mobile-menu">
      <IconButton
        :icon="Menu"
        label="Abrir navegación"
        :pressed="navigationOpen"
        @click="emit('toggleNavigation')"
      />
    </div>

    <div class="topbar__copy">
      <h1 class="topbar__title">{{ title }}</h1>
      <p v-if="description" class="topbar__description">{{ description }}</p>
    </div>

    <div class="topbar__actions" role="group" aria-label="Acciones globales">
      <slot name="actions" />
    </div>
  </header>
</template>

<style scoped>
.topbar {
  align-items: center;
  background: var(--color-background-surface);
  border-bottom: var(--border-width-default) solid var(--color-border-default);
  display: flex;
  gap: var(--space-4);
  min-height: var(--layout-topbar-height);
  padding: var(--space-3) var(--space-6);
  position: sticky;
  top: 0;
  z-index: var(--z-content);
}

.topbar__mobile-menu {
  display: none;
}

.topbar__copy {
  min-width: 0;
}

.topbar__title {
  color: var(--color-text-primary);
  font-size: var(--font-size-heading-2);
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-heading-2);
  margin: 0;
}

.topbar__description {
  color: var(--color-text-secondary);
  font-size: var(--font-size-small);
  line-height: var(--line-height-small);
  margin: var(--space-1) 0 0;
}

.topbar__actions {
  align-items: center;
  display: flex;
  gap: var(--space-2);
  margin-left: auto;
}

@media (max-width: 899px) {
  .topbar {
    padding-inline: var(--space-4);
  }

  .topbar__mobile-menu {
    display: inline-flex;
  }
}
</style>
