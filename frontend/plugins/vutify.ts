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
	VSelect,
	VSnackbar,
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
			VSnackbar,
			VSelect,
		},
		directives,
	})

	nuxtApp.vueApp.use(vuetify)
})
