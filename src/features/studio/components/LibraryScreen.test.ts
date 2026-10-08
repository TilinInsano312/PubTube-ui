import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import LibraryScreen from './LibraryScreen.vue'

describe('biblioteca de demostración', () => {
  it('filtra publicaciones programadas y conserva etiqueta de datos de demostración', async () => {
    const wrapper = mount(LibraryScreen)
    const scheduledFilter = wrapper
      .findAll('.status-tabs button')
      .find((button) => button.text().startsWith('Programadas'))

    await scheduledFilter?.trigger('click')

    expect(wrapper.text()).toContain('Datos de demostración')
    expect(wrapper.findAll('tbody tr')).toHaveLength(4)
    expect(wrapper.text()).toContain('Flujo de publicación automática')
    expect(wrapper.text()).not.toContain('Introducción a PubTube')
  })
})
