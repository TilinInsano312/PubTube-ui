<script setup lang="ts">
import { RouterLink } from 'vue-router'
import '../auth.css'

defineProps<{ variant: 'login' | 'register' }>()
</script>

<template>
  <div class="auth-page">
    <header class="auth-header">
      <RouterLink to="/" class="auth-brand" aria-label="PubTube, inicio">
        <span class="auth-logo" aria-hidden="true">
          <svg viewBox="0 0 10 10"><path d="M2 1l7 4-7 4z" /></svg>
        </span>
        PubTube
      </RouterLink>

      <div class="auth-header-actions">
        <RouterLink v-if="variant === 'login'" to="/register" class="auth-pill">Crear cuenta</RouterLink>
        <template v-else>
          <span class="auth-chip">Español</span>
          <RouterLink to="/login" class="auth-link-red">Iniciar sesión</RouterLink>
        </template>
      </div>
    </header>

    <main class="auth-main">
      <section class="auth-card">
        <slot />
      </section>

      <footer class="auth-footer">
        <span>Español</span>
        <nav aria-label="Enlaces legales">
          <a href="#">Ayuda</a>
          <a href="#">Privacidad</a>
          <a href="#">{{ variant === 'login' ? 'Términos' : 'Condiciones' }}</a>
        </nav>
      </footer>
    </main>
  </div>
</template>