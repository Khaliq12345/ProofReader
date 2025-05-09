export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  modules: [ '@nuxt/ui'],
  css: ['./assets/css/main.css'],
  runtimeConfig: {
    public: {
      urlAPI: process.env.API_URL,
      inputsPath: process.env.INPUTS_PATH,
      outputsPath: process.env.OUTPUTS_PATH,
     },
  },
  nitro: {
    storage: {
      uploads: {
        driver: 'fs',
        base: process.env.INPUTS_PATH
      },
      outputs: {
        driver: 'fs',
        base: process.env.OUTPUTS_PATH
      }
    }
  }
})