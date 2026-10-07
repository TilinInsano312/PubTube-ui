import { computed, type Ref } from 'vue'
import { MIN_PASSWORD_LENGTH } from '../validators'

const LABELS = ['Pendiente', 'Débil', 'Media', 'Fuerte'] as const

export function usePasswordStrength(password: Ref<string>) {
  return computed(() => {
    const p = password.value
    if (!p) return { score: 0, label: LABELS[0] }
    let score = 0
    if (p.length >= MIN_PASSWORD_LENGTH) score++
    if (/[a-z]/.test(p) && /[A-Z]/.test(p)) score++
    if (/\d/.test(p) && /[^A-Za-z0-9]/.test(p)) score++
    return { score, label: LABELS[Math.max(score, 1)] }
  })
}