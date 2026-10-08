<script setup lang="ts">
import { computed } from 'vue'
import { Activity, CalendarClock, LayoutDashboard, Library, Settings, X } from '@lucide/vue'
import { Avatar, IconButton, NavigationRailItem } from '../shared/ui'
import type { NavigationItemDefinition } from './types'

const props = withDefaults(
  defineProps<{
    items?: NavigationItemDefinition[]
    activeItem?: string
    mobileOpen?: boolean
    avatarInitials?: string
    avatarLabel?: string
  }>(),
  {
    activeItem: 'dashboard',
    mobileOpen: false,
    avatarInitials: 'PT',
    avatarLabel: 'Perfil de PubTube',
  },
)

const emit = defineEmits<{
  select: [id: string]
  close: []
}>()

const defaultItems: NavigationItemDefinition[] = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { id: 'content', label: 'Contenidos', icon: Library },
  { id: 'publications', label: 'Publicaciones', icon: CalendarClock },
  { id: 'activity', label: 'Actividad', icon: Activity },
  { id: 'settings', label: 'Settings', icon: Settings },
]

const navigationItems = computed(() =>
  props.items && props.items.length > 0 ? props.items : defaultItems,
)

function selectItem(item: NavigationItemDefinition): void {
  if (item.disabled) {
    return
  }

  emit('select', item.id)
  emit('close')
}
</script>

<template>
  <aside
    class="navigation-rail"
    :class="{ 'navigation-rail--mobile-open': mobileOpen }"
    aria-label="Navegación principal"
  >
    <div class="navigation-rail__header">
      <div class="navigation-rail__brand" role="img" aria-label="PubTube">
        <span class="navigation-rail__brand-mark" aria-hidden="true">PT</span>
      </div>

      <IconButton
        v-if="mobileOpen"
        class="navigation-rail__close"
        :icon="X"
        label="Cerrar navegación"
        size="small"
        @click="emit('close')"
      />
    </div>

    <nav class="navigation-rail__nav" aria-label="Secciones de PubTube">
      <NavigationRailItem
        v-for="item in navigationItems"
        :key="item.id"
        :label="item.label"
        :icon="item.icon"
        :active="item.id === activeItem"
        :disabled="item.disabled"
        :icon-only="!mobileOpen"
        @click="selectItem(item)"
      />
    </nav>

    <div class="navigation-rail__footer">
      <Avatar :initials="avatarInitials" :label="avatarLabel" />
    </div>
  </aside>
</template>

<style scoped>
.navigation-rail {
  align-items: stretch;
  background: var(--color-background-surface);
  border-right: var(--border-width-default) solid var(--color-border-default);
  display: flex;
  flex-direction: column;
  height: 100dvh;
  left: 0;
  position: fixed;
  top: 0;
  transition: transform var(--motion-duration-standard) var(--motion-easing-standard);
  width: var(--layout-navigation-rail-width);
  z-index: var(--z-navigation);
}

.navigation-rail__header {
  align-items: center;
  display: flex;
  justify-content: center;
  min-height: var(--layout-topbar-height);
  padding: var(--space-3);
}

.navigation-rail__brand {
  align-items: center;
  display: inline-flex;
  justify-content: center;
}

.navigation-rail__brand-mark {
  align-items: center;
  background: var(--color-action-primary);
  border-radius: var(--radius-md);
  color: var(--color-action-primary-content);
  display: inline-flex;
  font-size: var(--font-size-small);
  font-weight: var(--font-weight-bold);
  height: var(--space-10);
  justify-content: center;
  width: var(--space-10);
}

.navigation-rail__close {
  display: none;
}

.navigation-rail__nav {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: var(--space-2);
  padding: var(--space-4) var(--space-3);
}

.navigation-rail__footer {
  align-items: center;
  display: flex;
  justify-content: center;
  min-height: var(--layout-topbar-height);
  padding: var(--space-3);
}

@media (max-width: 899px) {
  .navigation-rail {
    box-shadow: var(--shadow-lg);
    transform: translateX(-100%);
    width: min(
      calc(var(--layout-navigation-rail-width) * 3),
      calc(100vw - var(--space-8))
    );
  }

  .navigation-rail--mobile-open {
    transform: translateX(0);
  }

  .navigation-rail__header {
    justify-content: space-between;
  }

  .navigation-rail__close {
    display: inline-flex;
  }

  .navigation-rail__nav {
    padding-inline: var(--space-4);
  }

  .navigation-rail__footer {
    justify-content: flex-start;
    padding-inline: var(--space-4);
  }
}

@media (prefers-reduced-motion: reduce) {
  .navigation-rail {
    transition: none;
  }
}
</style>
