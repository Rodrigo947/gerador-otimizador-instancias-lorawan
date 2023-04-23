import { createVuetify } from 'vuetify'
import {
	VApp,
	VAppBar,
	VAppBarTitle,
	VBtn,
	VContainer,
	VIcon,
	VList,
	VListItem,
	VListSubheader,
	VMain,
	VNavigationDrawer,
	VTextField,
} from 'vuetify/components'
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
			VListItem,
			VListSubheader,
			VContainer,
			VBtn,
			VTextField,
			VIcon,
		},
		directives,
	})

	nuxtApp.vueApp.use(vuetify)
})
