const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: [
    'vuw-echarts',
    'resize-detector'
  ]
 
})