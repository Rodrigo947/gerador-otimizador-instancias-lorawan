import { createVuetify } from 'vuetify'
import { VApp, VAppBar, VAppBarTitle, VBtn, VContainer, VList, VMain, VNavigationDrawer } from 'vuetify/components'
import * as directives from 'vuetify/directives'

export default defineNuxtPlugin((nuxtApp) => {
	const vuetify = createVuetify({
		ssr: true,
		components: {
			VApp,
			VAppBar,
			VAppBarTitle,
			VNavigationDrawer,
			VMain,
			VList,
			VContainer,
			VBtn,
		},
		directives,
	})

	nuxtApp.vueApp.use(vuetify)
})
