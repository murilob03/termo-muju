import globals from "globals";
import tseslint from "typescript-eslint";
import pluginReact from "eslint-plugin-react";
import pluginNext from "eslint-plugin-next"; // ✅ Import Next.js plugin
import { defineConfig } from "eslint/config";

export default defineConfig([
  {
    files: ["**/*.{js,mjs,cjs,ts,mts,cts,jsx,tsx}"],
    languageOptions: { globals: globals.browser },
    settings: {
      react: {
        version: "detect", // ✅ Let ESLint auto-detect your React version
      },
    },
    plugins: {
      next: pluginNext, // ✅ Register Next.js plugin
    },
    rules: {
      "@typescript-eslint/no-explicit-any": "off", // ✅ Allow 'any'
    },
  },
  tseslint.configs.recommended,
  pluginReact.configs.flat.recommended,
  pluginNext.configs.recommended, // ✅ Add Next.js rules
]);
