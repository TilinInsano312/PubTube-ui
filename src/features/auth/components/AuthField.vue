<script lang="ts">
let nextId = 0
</script>

<script setup lang="ts">
import { computed, ref } from 'vue'

const props = defineProps<{
  modelValue: string
  label: string
  type?: 'text' | 'email' | 'password'
  placeholder?: string
  icon?: 'user' | 'mail' | 'lock'
  autocomplete?: string
  error?: string
}>()
const emit = defineEmits<{ 'update:modelValue': [value: string] }>()

const id = `auth-field-${nextId++}`
const visible = ref(false)
const isPassword = computed(() => props.type === 'password')
const inputType = computed(() => (isPassword.value && visible.value ? 'text' : props.type ?? 'text'))

function onInput(e: Event) {
  emit('update:modelValue', (e.target as HTMLInputElement).value)
}
</script>

<template>
  <div class="auth-field">
    <div class="auth-label-row">
      <label :for="id" class="auth-label">{{ label }}</label>
      <slot name="label-extra" />
    </div>

    <div class="auth-input-wrap">
      <svg v-if="icon" class="auth-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <template v-if="icon === 'user'"><circle cx="12" cy="12" r="4" /><path d="M16 8v5a3 3 0 0 0 6 0v-1a10 10 0 1 0-4 8" /></template>
        <template v-else-if="icon === 'mail'"><rect x="3" y="5" width="18" height="14" rx="2" /><path d="m3 7 9 6 9-6" /></template>
        <template v-else><rect x="5" y="11" width="14" height="9" rx="2" /><path d="M8 11V8a4 4 0 0 1 8 0v3" /></template>
      </svg>

      <input
        :id="id"
        class="auth-input"
        :class="{ 'has-icon': icon }"
        :type="inputType"
        :value="modelValue"
        :placeholder="placeholder"
        :autocomplete="autocomplete"
        :aria-invalid="!!error"
        :aria-describedby="error ? `${id}-err` : undefined"
        @input="onInput"
      />

      <button v-if="isPassword" type="button" class="auth-eye" :aria-label="visible ? 'Ocultar contraseña' : 'Mostrar contraseña'" :aria-pressed="visible" @click="visible = !visible">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z" /><circle cx="12" cy="12" r="3" />
          <path v-if="visible" d="M4 4l16 16" />
        </svg>
      </button>
    </div>

    <p v-if="error" :id="`${id}-err`" class="auth-error" role="alert">{{ error }}</p>
  </div>
</template>