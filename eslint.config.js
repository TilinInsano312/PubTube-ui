import js from '@eslint/js'
import eslintConfigPrettier from 'eslint-config-prettier'
import pluginVue from 'eslint-plugin-vue'
import globals from 'globals'
import tseslint from 'typescript-eslint'

export default tseslint.config(
  {
    ignores: ['dist/**', 'coverage/**'],
  },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  ...pluginVue.configs['flat/recommended'],
  {
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
    rules: {
      // Los primitives existentes usan nombres públicos breves (Button,
      // Avatar y Topbar); la regla no aporta desambiguación en este proyecto.
      'vue/multi-word-component-names': 'off',
    },
  },
  {
    files: ['**/*.vue'],
    languageOptions: {
      parserOptions: {
        parser: tseslint.parser,
        extraFileExtensions: ['.vue'],
      },
    },
  },
  {
    // `props.emptyTitle` and the local helper are separate bindings; the Vue
    // rule treats their shared property name as a collision.
    files: ['src/features/dashboard/components/PublicationTable.vue'],
    rules: {
      'vue/no-dupe-keys': 'off',
    },
  },
  eslintConfigPrettier,
)
