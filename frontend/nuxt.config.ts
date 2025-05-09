export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  modules: [ '@nuxt/ui'],
  css: ['./assets/css/main.css'],
  runtimeConfig: {
    public: {
      urlAPI: process.env.API_URL,
     },
  },
  nitro: {
    storage: {
      uploads: {
        driver: 'fs',
        base: process.env.ABSOLUTE_PATH
      },
      ouputs: {
        driver: 'fs',
        base: process.env.OUTPUT_PATH
      }
    }
  }
})