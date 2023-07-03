import { createVuetify } from 'vuetify'
import {
	VApp,
	VAppBar,
	VAppBarTitle,
	VBtn,
	VCol,
	VContainer,
	VIcon,
	VList,
	VListItem,
	VListSubheader,
	VMain,
	VNavigationDrawer,
	VRow,
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
			VCol,
			VRow,
		},
		directives,
	})

	nuxtApp.vueApp.use(vuetify)
})
