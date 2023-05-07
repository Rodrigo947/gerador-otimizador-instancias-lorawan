// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
	css: ['vuetify/lib/styles/main.sass', '@mdi/font/css/materialdesignicons.min.css'],
	build: {
		transpile: ['vuetify'],
	},
	vite: {
		define: {
			'process.env.DEBUG': true,
		},
	},

	modules: ['@pinia/nuxt'],

	runtimeConfig: {
		public: {
			MAPBOX_TOKEN: process.env.MAPBOX_TOKEN,
			baseURL: process.env.BASE_URL || 'http://localhost:8000',
		},
	},
})
