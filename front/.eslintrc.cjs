/* eslint-env node */
require("@rushstack/eslint-patch/modern-module-resolution");

module.exports = {
  root: true,
  extends: ["plugin:vue/vue3-essential", "eslint:recommended", "@vue/eslint-config-prettier"],
  parserOptions: {
    ecmaVersion: "latest",
  },
  env: {
    node: true,
  },
  rules: {
    "no-unused-vars": ["error", { args: "none" }],
    // yeah i know but im not gonna change everything
    "vue/multi-word-component-names": "off",
    // bleh: https://github.com/vuejs/eslint-plugin-vue/issues/1371
    "vue/no-mutating-props": 0,
    "max-len": ["error", { code: 150 }],
    "prettier/prettier": ["error", { printWidth: 150, bracketSameLine: true, htmlWhitespaceSensitivity: "strict" }],
  },
};
