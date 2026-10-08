<script setup lang="ts">
import { computed, ref } from 'vue'
import {
  Activity,
  Bell,
  CalendarClock,
  Grid2X2,
  LibraryBig,
  Play,
  Plus,
  RefreshCw,
  Settings2,
} from '@lucide/vue'
import DashboardView from '../dashboard/DashboardView.vue'
import LibraryScreen from './components/LibraryScreen.vue'
import MetadataEditorScreen from './components/MetadataEditorScreen.vue'
import UploadScreen from './components/UploadScreen.vue'
import { uploadVideo } from './api/content.api'
import type { LibraryItem } from './data/library.fixtures'

type Screen = 'library' | 'editor' | 'upload'
const screen = ref<Screen>('library')
const moduleView = ref<'studio' | 'module4'>('studio')
const demoItem = ref<LibraryItem | null>(null)
const contentId = ref<string | null>(null)
const libraryKey = ref(0)

const pageLabel = computed(
  () =>
    ({
      library: 'Biblioteca',
      editor: 'Editar metadatos',
      upload: 'Subir video',
    })[screen.value],
)

function showLibrary(): void {
  screen.value = 'library'
  demoItem.value = null
  contentId.value = null
}

function openDemo(item: LibraryItem): void {
  demoItem.value = item
  contentId.value = null
  screen.value = 'editor'
}

function openContent(id: string): void {
  demoItem.value = null
  contentId.value = id
  screen.value = 'editor'
}

function startUpload(): void {
  demoItem.value = null
  contentId.value = null
  screen.value = 'upload'
}

function openEditorById(): void {
  demoItem.value = null
  contentId.value = null
  screen.value = 'editor'
}
</script>

<template>
  <div class="studio-root">
    <div v-show="moduleView === 'studio'">
      <aside class="navigation-rail" aria-label="Navegación principal">
        <button
          class="brand-mark"
          type="button"
          aria-label="PubTube Studio, inicio"
          @click="showLibrary"
        >
          <Play :size="18" fill="currentColor" />
        </button>
        <nav class="rail-navigation" aria-label="Módulos">
          <button
            type="button"
            class="rail-link"
            aria-label="Biblioteca"
            :class="{ active: screen === 'library' }"
            :aria-current="screen === 'library' ? 'page' : undefined"
            @click="showLibrary"
          >
            <LibraryBig :size="20" /><span>Biblioteca</span>
          </button>
          <button
            type="button"
            class="rail-link"
            aria-label="Panel Módulo 4"
            :class="{ active: moduleView === 'module4' }"
            @click="moduleView = 'module4'"
          >
            <Grid2X2 :size="20" /><span>Panel Módulo 4</span>
          </button>
          <button
            type="button"
            class="rail-link unavailable"
            aria-label="Programación no disponible"
            disabled
            title="La programación aún no tiene endpoint HTTP"
          >
            <CalendarClock :size="20" /><span>Programación</span>
          </button>
          <button
            type="button"
            class="rail-link unavailable"
            aria-label="Actividad no disponible"
            disabled
            title="La actividad todavía no forma parte de estas pantallas"
          >
            <Activity :size="20" /><span>Actividad</span>
          </button>
        </nav>
        <div class="rail-bottom">
          <button
            type="button"
            class="rail-link unavailable"
            aria-label="Ajustes no disponibles"
            disabled
            title="Ajustes no disponibles"
          >
            <Settings2 :size="20" /><span>Ajustes</span></button
          ><span class="module-avatar" role="img" aria-label="Módulo 1"
            >M1</span
          >
        </div>
      </aside>

      <div class="studio-workspace">
        <header class="studio-topbar">
          <div class="product-heading">
            <strong>PubTube Studio</strong>
            <p>Consola editorial de automatización y orquestación de video</p>
          </div>
          <div class="topbar-actions">
            <button
              class="topbar-icon"
              type="button"
              aria-label="Actualizar biblioteca"
              :disabled="screen !== 'library'"
              @click="libraryKey++"
            >
              <RefreshCw :size="18" /></button
            ><button
              class="topbar-icon"
              type="button"
              aria-label="Notificaciones no disponibles"
              title="Notificaciones no disponibles en esta versión"
              disabled
            >
              <Bell :size="18" /></button
            ><button
              class="button button-primary"
              type="button"
              @click="startUpload"
            >
              <Plus :size="17" /> Nuevo video</button
            ><span
              class="module-avatar top-avatar"
              role="img"
              aria-label="Módulo 1"
              >M1</span
            >
          </div>
        </header>
        <main class="studio-content" :aria-label="pageLabel">
          <LibraryScreen
            v-if="screen === 'library'"
            :key="libraryKey"
            @open-demo="openDemo"
            @edit-by-id="openEditorById"
          />
          <MetadataEditorScreen
            v-else-if="screen === 'editor'"
            :initial-content-id="contentId"
            :demo-item="demoItem"
            @back="showLibrary"
            @upload="startUpload"
          />
          <UploadScreen
            v-else
            :upload-file="uploadVideo"
            @back="showLibrary"
            @open-content="openContent"
          />
        </main>
      </div>
    </div>

    <div v-show="moduleView === 'module4'" class="module4-view">
      <div class="module4-toolbar">
        <button
          class="button button-primary"
          type="button"
          @click="moduleView = 'studio'"
        >
          <LibraryBig :size="16" /> Volver a PubTube Studio</button
        ><span>Dashboard existente del Módulo 4</span>
      </div>
      <DashboardView />
    </div>
  </div>
</template>

<style scoped>
.studio-root {
  min-height: 100vh;
  color: var(--color-text-primary);
  background: var(--color-background-canvas);
}
.navigation-rail {
  position: fixed;
  inset: 0 auto 0 0;
  z-index: var(--z-navigation);
  width: 72px;
  display: flex;
  align-items: center;
  flex-direction: column;
  gap: 18px;
  padding: 14px 8px;
  border-right: 1px solid var(--color-border-default);
  background: var(--color-background-surface);
}
.brand-mark {
  display: grid;
  place-items: center;
  width: 42px;
  height: 42px;
  border: 0;
  border-radius: var(--radius-md);
  color: white;
  background: var(--color-action-primary);
  cursor: pointer;
}
.rail-navigation,
.rail-bottom {
  display: grid;
  justify-items: center;
  gap: 8px;
  width: 100%;
}
.rail-navigation {
  flex: 1;
  align-content: start;
}
.rail-bottom {
  align-content: end;
}
.rail-link {
  display: grid;
  place-items: center;
  gap: 4px;
  width: 52px;
  min-height: 48px;
  border: 0;
  border-radius: var(--radius-md);
  background: transparent;
  color: var(--color-text-secondary);
  cursor: pointer;
}
.rail-link span {
  display: none;
}
.rail-link.active {
  color: var(--color-action-primary);
  background: var(--color-action-primary-soft);
}
.rail-link.unavailable {
  opacity: 0.56;
  cursor: not-allowed;
}
.module-avatar {
  display: grid;
  place-items: center;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  color: var(--color-action-primary);
  background: var(--color-action-primary-soft);
  font-size: var(--font-size-caption);
  font-weight: var(--font-weight-bold);
}
.studio-workspace {
  min-height: 100vh;
  margin-left: 72px;
}
.studio-topbar {
  position: sticky;
  top: 0;
  z-index: var(--z-navigation);
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 68px;
  padding: 10px 24px;
  border-bottom: 1px solid var(--color-border-default);
  background: var(--color-background-surface);
}
.product-heading h1 {
  margin: 0 0 3px;
  font-size: var(--font-size-heading-3);
}
.product-heading p {
  margin: 0;
  color: var(--color-text-secondary);
  font-size: var(--font-size-caption);
}
.topbar-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}
.topbar-icon {
  display: grid;
  place-items: center;
  width: 40px;
  height: 40px;
  border: 1px solid var(--color-border-default);
  border-radius: var(--radius-full);
  color: var(--color-text-secondary);
  background: var(--color-background-surface);
  cursor: pointer;
}
.topbar-icon:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 7px;
  border: 1px solid transparent;
  border-radius: var(--radius-md);
  padding: 10px 14px;
  font-weight: var(--font-weight-semibold);
  cursor: pointer;
}
.button-primary {
  color: white;
  background: var(--color-action-primary);
}
.studio-content {
  width: min(100%, 1440px);
  margin: 0 auto;
  padding: 22px 24px 42px;
}
.module4-view {
  min-height: 100vh;
}
.module4-toolbar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 24px;
  background: var(--color-background-surface);
  border-bottom: 1px solid var(--color-border-default);
}
.module4-toolbar span {
  color: var(--color-text-secondary);
  font-size: var(--font-size-small);
}
@media (max-width: 680px) {
  .navigation-rail {
    inset: auto 0 0;
    width: 100%;
    height: 62px;
    flex-direction: row;
    justify-content: space-around;
    padding: 5px 8px;
    border-right: 0;
    border-top: 1px solid var(--color-border-default);
  }
  .brand-mark,
  .rail-bottom {
    display: none;
  }
  .rail-navigation {
    display: flex;
    justify-content: space-around;
    align-items: center;
  }
  .rail-link {
    width: 52px;
    min-height: 46px;
  }
  .studio-workspace {
    margin-left: 0;
    padding-bottom: 66px;
  }
  .studio-topbar {
    padding: 9px 12px;
    min-height: 62px;
  }
  .product-heading p {
    max-width: 210px;
  }
  .topbar-actions {
    gap: 5px;
  }
  .topbar-icon {
    width: 34px;
    height: 34px;
  }
  .topbar-actions .button {
    padding: 9px 10px;
    font-size: var(--font-size-caption);
  }
  .top-avatar {
    display: none;
  }
  .studio-content {
    padding: 14px 12px 28px;
  }
  .module4-toolbar {
    padding: 9px 12px;
    flex-wrap: wrap;
  }
}
.product-heading strong {
  display: block;
  margin: 0 0 3px;
  font-size: var(--font-size-heading-3);
}
</style>
