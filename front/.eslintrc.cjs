/* eslint-env node */
require("@rushstack/eslint-patch/modern-module-resolution");

module.exports = {
  root: true,
  "env": {
    "node": true,
    "commonjs": true
  },
  extends: ["plugin:vue/vue3-essential", "eslint:recommended"],
  parserOptions: {
    ecmaVersion: "latest",
  },
  rules: {
    "vue/html-closing-bracket-newline": [
      "error",
      {
        singleline: "never",
        multiline: "always",
      },
    ],
  },
};
