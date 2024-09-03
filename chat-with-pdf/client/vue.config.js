const { defineConfig } = require('@vue/cli-service')
module.exports = {
  configureWebpack: {
    experiments: {
      asyncWebAssembly: true,
    },
    module: {
      rules: [
        {
          test: /\.wasm$/,
          type: "webassembly/async",
        },
      ],
    },
  },
}
