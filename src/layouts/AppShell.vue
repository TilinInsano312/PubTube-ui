<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import NavigationRail from './NavigationRail.vue'
import Topbar from './Topbar.vue'
import type { NavigationItemDefinition } from './types'

const props = withDefaults(
  defineProps<{
    title: string
    description?: string
    navigationItems?: NavigationItemDefinition[]
    activeNavigationId?: string
    avatarInitials?: string
    avatarLabel?: string
  }>(),
  {
    description: '',
    activeNavigationId: 'dashboard',
    avatarInitials: 'PT',
    avatarLabel: 'Perfil de PubTube',
  },
)

const emit = defineEmits<{
  navigationSelect: [id: string]
}>()

const isMobileViewport = ref(false)
const isMobileNavigationOpen = ref(false)
const topbar = ref<{ focusNavigationToggle: () => void } | null>(null)
let mediaQuery: MediaQueryList | undefined

const showMobileOverlay = computed(
  () => isMobileViewport.value && isMobileNavigationOpen.value,
)

function syncViewport(event?: MediaQueryListEvent): void {
  isMobileViewport.value = event?.matches ?? mediaQuery?.matches ?? false

  if (!isMobileViewport.value) {
    isMobileNavigationOpen.value = false
  }
}

function toggleNavigation(): void {
  if (isMobileNavigationOpen.value) {
    closeNavigation()
    return
  }

  isMobileNavigationOpen.value = true
}

function closeNavigation(): void {
  isMobileNavigationOpen.value = false

  if (isMobileViewport.value) {
    void nextTick(() => topbar.value?.focusNavigationToggle())
  }
}

function selectNavigationItem(id: string): void {
  emit('navigationSelect', id)
  closeNavigation()
}

onMounted(() => {
  mediaQuery = window.matchMedia('(max-width: 899px)')
  syncViewport()
  mediaQuery.addEventListener('change', syncViewport)
})

onBeforeUnmount(() => {
  mediaQuery?.removeEventListener('change', syncViewport)
})
</script>

<template>
  <div class="app-shell">
    <NavigationRail
      :items="props.navigationItems"
      :active-item="props.activeNavigationId"
      :mobile-open="isMobileNavigationOpen"
      :avatar-initials="props.avatarInitials"
      :avatar-label="props.avatarLabel"
      @select="selectNavigationItem"
      @close="closeNavigation"
    />

    <button
      v-if="showMobileOverlay"
      class="app-shell__overlay"
      type="button"
      aria-label="Cerrar navegación"
      @click="closeNavigation"
    ></button>

    <div class="app-shell__frame">
      <Topbar
        ref="topbar"
        :title="props.title"
        :description="props.description"
        :navigation-open="isMobileNavigationOpen"
        @toggle-navigation="toggleNavigation"
      >
        <template #actions>
          <slot name="actions" />
        </template>
      </Topbar>

      <main class="app-shell__content">
        <slot />
      </main>
    </div>
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100vh;
}

.app-shell__frame {
  margin-left: var(--layout-navigation-rail-width);
  min-height: 100vh;
}

.app-shell__content {
  margin: 0 auto;
  max-width: var(--layout-dashboard-width);
  padding: var(--space-8) var(--space-6) var(--space-16);
}

.app-shell__overlay {
  background: color-mix(in srgb, var(--color-text-primary) 32%, transparent);
  border: 0;
  inset: 0;
  position: fixed;
  z-index: calc(var(--z-navigation) - 1);
}

@media (max-width: 899px) {
  .app-shell__frame {
    margin-left: 0;
  }

  .app-shell__content {
    padding: var(--space-6) var(--space-4) var(--space-10);
  }
}
</style>
