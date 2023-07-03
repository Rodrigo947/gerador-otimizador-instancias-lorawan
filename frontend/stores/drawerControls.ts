import { defineStore } from 'pinia'

export const useDrawerControls = defineStore('drawerControls', {
	state: () => ({
		drawer: false,
		lastBtnClicked: 'areas',
	}),
	actions: {
		changeDrawer(btnClicked: string) {
			if (!this.drawer) {
				this.drawer = true
			} else if (this.drawer && this.lastBtnClicked == btnClicked) {
				this.drawer = false
			}

			this.lastBtnClicked = btnClicked
		},
		closeDrawer() {
			this.drawer = false
		},
	},
})
