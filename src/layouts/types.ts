import type { Component } from 'vue'

export interface NavigationItemDefinition {
  id: string
  label: string
  icon: Component
  disabled?: boolean
}
