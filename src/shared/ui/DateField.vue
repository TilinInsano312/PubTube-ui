<script setup lang="ts">
withDefaults(
  defineProps<{
    id: string
    label: string
    modelValue: string
    disabled?: boolean
    error?: string
  }>(),
  {
    disabled: false,
    error: '',
  },
)

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()
</script>

<template>
  <div class="ui-date-field">
    <label class="ui-date-field__label" :for="id">{{ label }}</label>
    <input
      :id="id"
      class="ui-date-field__input"
      :class="{ 'ui-date-field__input--error': error }"
      type="date"
      :value="modelValue"
      :disabled="disabled"
      :aria-invalid="Boolean(error)"
      :aria-describedby="error ? `${id}-error` : undefined"
      @input="emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    />
    <p v-if="error" :id="`${id}-error`" class="ui-date-field__error" role="alert">
      {{ error }}
    </p>
  </div>
</template>

<style scoped>
.ui-date-field {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.ui-date-field__label {
  color: var(--color-text-secondary);
  font-size: var(--font-size-small);
  font-weight: var(--font-weight-semibold);
}

.ui-date-field__input {
  background: var(--color-background-surface);
  border: var(--border-width-default) solid var(--color-border-default);
  border-radius: var(--radius-md);
  color: var(--color-text-primary);
  min-height: var(--control-height-standard);
  padding: 0 var(--space-3);
  width: 100%;
}

.ui-date-field__input:hover:not(:disabled) {
  border-color: var(--color-border-strong);
}

.ui-date-field__input:disabled {
  background: var(--color-background-sunken);
  cursor: not-allowed;
}

.ui-date-field__input--error {
  border-color: var(--color-status-danger-solid);
}

.ui-date-field__error {
  color: var(--color-status-danger-text);
  font-size: var(--font-size-caption);
  margin: 0;
}
</style>
