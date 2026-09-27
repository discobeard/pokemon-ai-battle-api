import js from '@eslint/js';
import globals from 'globals';
import tseslint from 'typescript-eslint';
import { defineConfig } from 'eslint/config';
import prettierConfig from 'eslint-config-prettier';

export default defineConfig([
  { ignores: ['node_modules', 'cdk.out', 'backend'] },
  {
    files: ['bin/**/*.ts', 'lib/**/*.ts', 'test/**/*.ts'],
    plugins: { js },
    // CDK apps and tests run in Node, not the browser.
    languageOptions: { globals: { ...globals.node, ...globals.jest } },
    rules: {
      ...js.configs.recommended.rules,
      quotes: ['error', 'single', { avoidEscape: true }],
    },
  },
  ...tseslint.configs.recommended,
  prettierConfig,
]);
