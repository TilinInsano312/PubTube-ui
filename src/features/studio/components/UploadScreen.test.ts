import { flushPromises, mount } from '@vue/test-utils'
import { describe, expect, it, vi } from 'vitest'
import { ApiError } from '../../../shared/api/http'
import UploadScreen from './UploadScreen.vue'

type UploadHandler = typeof import('../api/content.api').uploadVideo

describe('carga de video', () => {
  it('muestra la pantalla de duplicado y permite usar el contentId existente ante 409', async () => {
    const uploadFile = vi.fn<UploadHandler>().mockRejectedValue(
      new ApiError('Este video ya existe', 409, {
        statusCode: 409,
        error: 'DUPLICATE_CONTENT',
        existingContentId: 'existing-uuid-42',
      }),
    )
    const wrapper = mount(UploadScreen, { props: { uploadFile } })
    const input = wrapper.get('input[type="file"]')
    const videoFile = new File(['video'], 'demo.mp4', { type: 'video/mp4' })
    Object.defineProperty(input.element, 'files', {
      configurable: true,
      value: [videoFile],
    })
    await input.trigger('change')
    await wrapper.get('.progress-actions .button-primary').trigger('click')
    await flushPromises()

    expect(wrapper.text()).toContain('Este video ya existe en tu biblioteca')
    expect(wrapper.text()).toContain('existing-uuid-42')
    await wrapper.get('.duplicate-actions .button-primary').trigger('click')
    expect(wrapper.emitted('openContent')?.[0]).toEqual(['existing-uuid-42'])
  })
})
