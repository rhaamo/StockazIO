// vetur.config.js
/** @type {import('vls').VeturConfig} */
module.exports = {
    // override vscode settings
    // Notice: It only affects the settings used by Vetur.
    settings: {
      "vetur.useWorkspaceDependencies": true,
      "vetur.experimental.templateInterpolationService": true
    },
    // support monorepos
    projects: [
      {
        // It is relative to `vetur.config.js`.
        root: './front',
        package: './package.json',
        // Register globally Vue component glob.
        // If you set it, you can get completion by that components.
        // It is relative to root property.
        // Notice: It won't actually do it. You need to use `require.context` or `Vue.component`
        globalComponents: [
          './src/components/**/*.vue'
        ]
      }
    ]
  }