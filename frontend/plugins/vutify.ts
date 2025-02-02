import { createVuetify } from 'vuetify'
import {
	VApp,
	VAppBar,
	VAppBarTitle,
	VBtn,
	VCard,
	VCardActions,
	VCardItem,
	VCardSubtitle,
	VCardText,
	VCardTitle,
	VCol,
	VContainer,
	VDialog,
	VIcon,
	VList,
	VListItem,
	VListItemTitle,
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
			VListItemTitle,
			VListSubheader,
			VContainer,
			VBtn,
			VTextField,
			VIcon,
			VSnackbar,
			VSelect,
			VCol,
			VRow,
			VCard,
			VCardActions,
			VCardItem,
			VCardText,
			VCardTitle,
			VCardSubtitle,
			VDialog,
		},
		directives,
	})

	nuxtApp.vueApp.use(vuetify)
})
