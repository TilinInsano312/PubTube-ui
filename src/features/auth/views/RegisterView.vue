<script setup lang="ts">
import { reactive, toRef } from 'vue'
import { RouterLink } from 'vue-router'
import AuthLayout from '../components/AuthLayout.vue'
import AuthField from '../components/AuthField.vue'
import GoogleButton from '../components/GoogleButton.vue'
import { usePasswordStrength } from '../composables/usePasswordStrength'
import type { RegisterForm } from '../types'
import { isEmail, MIN_PASSWORD_LENGTH } from '../validators'

const form = reactive<RegisterForm>({ username: '', email: '', password: '', confirm: '', terms: false })
const errors = reactive({ username: '', email: '', password: '', confirm: '', terms: '' })
const strength = usePasswordStrength(toRef(form, 'password'))

function validate(): boolean {
  errors.username = form.username.trim() ? '' : 'Elige un nombre de usuario.'
  errors.email = isEmail(form.email) ? '' : 'Introduce un correo válido.'
  errors.password = form.password.length >= MIN_PASSWORD_LENGTH ? '' : `Usa al menos ${MIN_PASSWORD_LENGTH} caracteres.`
  errors.confirm = form.confirm === form.password ? '' : 'Las contraseñas no coinciden.'
  errors.terms = form.terms ? '' : 'Debes aceptar las condiciones para continuar.'
  return Object.values(errors).every((e) => !e)
}

function onSubmit() {
  if (!validate()) return
  // Pendiente: integrar con api/auth.api.ts (RegisterPayload) cuando exista el contrato de registro.
}

function onGoogle() {
  // Pendiente: depende del contrato de autenticación del backend.
}
</script>

<template>
  <AuthLayout variant="register">
    <div class="auth-card-head">
      <span class="auth-brand center">
        <span class="auth-logo" aria-hidden="true">
          <svg viewBox="0 0 10 10"><path d="M2 1l7 4-7 4z" /></svg>
        </span>
        PubTube
      </span>
      <h1>Crea tu cuenta de PubTube</h1>
      <p>Para continuar viendo y publicando videos</p>
    </div>

    <GoogleButton @click="onGoogle">Registrarse con Google</GoogleButton>
    <div class="auth-divider">O completa tus datos</div>

    <form novalidate @submit.prevent="onSubmit">
      <AuthField v-model="form.username" label="Nombre de usuario" icon="user" placeholder="ej. tu_canal" autocomplete="username" :error="errors.username" />
      <AuthField v-model="form.email" label="Correo electrónico" type="email" icon="mail" placeholder="tu_correo@gmail.com" autocomplete="email" :error="errors.email" />
      <AuthField v-model="form.password" label="Contraseña" type="password" icon="lock" :placeholder="`Mínimo ${MIN_PASSWORD_LENGTH} caracteres`" autocomplete="new-password" :error="errors.password" />

      <div class="auth-strength" aria-live="polite">
        <span>Seguridad: <strong>{{ strength.label }}</strong></span>
        <span class="auth-bars" aria-hidden="true">
          <span v-for="n in 3" :key="n" :class="{ [`on-${strength.score}`]: n <= strength.score }" />
        </span>
      </div>

      <AuthField v-model="form.confirm" label="Confirmar contraseña" type="password" icon="lock" placeholder="Repite tu contraseña" autocomplete="new-password" :error="errors.confirm" />

      <label class="auth-check">
        <input v-model="form.terms" type="checkbox" />
        <span>
          Acepto las <a href="#">Condiciones del Servicio</a> y la <a href="#">Política de Privacidad</a> de PubTube.
        </span>
      </label>
      <p v-if="errors.terms" class="auth-error terms" role="alert">{{ errors.terms }}</p>

      <button type="submit" class="auth-btn primary">
        Crear cuenta
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" /></svg>
      </button>
    </form>

    <p class="auth-alt plain">
      ¿Ya tienes cuenta?
      <RouterLink to="/login">Iniciar sesión</RouterLink>
    </p>
  </AuthLayout>
</template>