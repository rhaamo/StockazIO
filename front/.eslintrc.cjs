/* eslint-env node */
require("@rushstack/eslint-patch/modern-module-resolution");

module.exports = {
  root: true,
  extends: [
    "plugin:vue/vue3-essential",
    "eslint:recommended",
    "@vue/eslint-config-prettier",
  ],
  parserOptions: {
    ecmaVersion: "latest",
  },
  env: {
    node: true,
  },
  rules: {
    "no-unused-vars": ["error", { args: "none" }],
    "vue/multi-word-component-names": 0,
    // bleh: https://github.com/vuejs/eslint-plugin-vue/issues/1371
    "vue/no-mutating-props": 0,
  },
};
