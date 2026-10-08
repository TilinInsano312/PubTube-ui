import { computed, readonly, ref } from 'vue'
import { getDashboardCounts, DashboardApiError } from '../../api/dashboard.api'
import type { DashboardDateQuery } from '../../api/dashboard.api'
import type {
  DashboardCounts,
  DashboardErrorCode,
} from '../../api/dashboard.types'

export type DashboardLoadState =
  'idle' | 'loading' | 'success' | 'empty' | 'error'

export interface DashboardErrorState {
  code: DashboardErrorCode
  status?: number
}

const EMPTY_COUNTS: DashboardCounts = {
  scheduled: 0,
  published: 0,
  failed: 0,
}

function hasNoCounts(counts: DashboardCounts): boolean {
  return counts.scheduled === 0 && counts.published === 0 && counts.failed === 0
}

export function useDashboardCounts() {
  const counts = ref<DashboardCounts>({ ...EMPTY_COUNTS })
  const error = ref<DashboardErrorState | null>(null)
  const state = ref<DashboardLoadState>('idle')
  let requestSequence = 0

  const isLoading = computed(() => state.value === 'loading')
  const isEmpty = computed(() => state.value === 'empty')

  async function load(query: DashboardDateQuery = {}): Promise<void> {
    if (isLoading.value) {
      return
    }

    const currentRequest = ++requestSequence
    state.value = 'loading'
    error.value = null

    try {
      const nextCounts = await getDashboardCounts(query)

      if (currentRequest !== requestSequence) {
        return
      }

      counts.value = nextCounts
      state.value = hasNoCounts(nextCounts) ? 'empty' : 'success'
    } catch (cause) {
      if (currentRequest !== requestSequence) {
        return
      }

      counts.value = { ...EMPTY_COUNTS }
      error.value =
        cause instanceof DashboardApiError
          ? { code: cause.code, status: cause.status }
          : { code: 'NETWORK_ERROR' }
      state.value = 'error'
    }
  }

  return {
    counts: readonly(counts),
    error: readonly(error),
    isEmpty: readonly(isEmpty),
    isLoading: readonly(isLoading),
    load,
    refresh: load,
    state: readonly(state),
  }
}
