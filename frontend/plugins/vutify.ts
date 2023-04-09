import { createVuetify } from 'vuetify'
import {
	VApp,
	VAppBar,
	VAppBarNavIcon,
	VAppBarTitle,
	VContainer,
	VList,
	VMain,
	VNavigationDrawer,
} from 'vuetify/components'
import * as directives from 'vuetify/directives'

export default defineNuxtPlugin((nuxtApp) => {
	const vuetify = createVuetify({
		ssr: true,
		components: {
			VApp,
			VAppBar,
			VAppBarTitle,
			VAppBarNavIcon,
			VNavigationDrawer,
			VMain,
			VList,
			VContainer,
		},
		directives,
	})

	nuxtApp.vueApp.use(vuetify)
})
