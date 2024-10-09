module.exports = {
  presets: [
    '@vue/cli-plugin-babel/preset'
  ],
  plugins: [
    '@babel/plugin-transform-private-methods', // Plugin for private methods
    '@babel/plugin-transform-class-static-block' // Plugin for static class blocks
  ]
}
