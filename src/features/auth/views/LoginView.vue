<script setup lang="ts">
import { reactive } from 'vue'
import { RouterLink } from 'vue-router'
import AuthLayout from '../components/AuthLayout.vue'
import AuthField from '../components/AuthField.vue'
import GoogleButton from '../components/GoogleButton.vue'
import type { LoginPayload } from '../types'
import { isEmail } from '../validators'

const form = reactive<LoginPayload>({ email: '', password: '', remember: false })
const errors = reactive({ email: '', password: '' })

function validate(): boolean {
  errors.email = isEmail(form.email) ? '' : 'Introduce un correo válido.'
  errors.password = form.password ? '' : 'Introduce tu contraseña.'
  return !errors.email && !errors.password
}

function onSubmit() {
  if (!validate()) return
  // Pendiente: integrar con api/auth.api.ts cuando exista el contrato de autenticación.
}

function onGoogle() {
  // Pendiente: depende del contrato de autenticación del backend.
}
</script>

<template>
  <AuthLayout variant="login">
    <div class="auth-card-head">
      <span class="auth-logo lg" aria-hidden="true">
        <svg viewBox="0 0 10 10"><path d="M2 1l7 4-7 4z" /></svg>
      </span>
      <h1>Acceder a PubTube</h1>
      <RouterLink to="/" class="auth-link">Ir a PubTube</RouterLink>
    </div>

    <form novalidate @submit.prevent="onSubmit">
      <AuthField v-model="form.email" label="Correo electrónico" type="email" placeholder="ejemplo@gmail.com" autocomplete="email" :error="errors.email" />

      <AuthField v-model="form.password" label="Contraseña" type="password" placeholder="Introduce tu contraseña" autocomplete="current-password" :error="errors.password">
        <template #label-extra>
          <RouterLink to="/forgot-password" class="auth-link">¿Has olvidado tu contraseña?</RouterLink>
        </template>
      </AuthField>

      <label class="auth-check">
        <input v-model="form.remember" type="checkbox" />
        Recordar sesión
      </label>

      <button type="submit" class="auth-btn primary">Iniciar sesión</button>
    </form>

    <div class="auth-divider">o</div>
    <GoogleButton @click="onGoogle">Continuar con Google</GoogleButton>

    <p class="auth-alt">
      ¿No tienes una cuenta de PubTube?
      <RouterLink to="/register">Crear cuenta</RouterLink>
    </p>
  </AuthLayout>
</template>