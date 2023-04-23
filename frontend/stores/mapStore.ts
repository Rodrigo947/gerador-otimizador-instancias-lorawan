import { defineStore } from 'pinia'

export const useMapStore = defineStore('mapStore', {
	state: () => {
		return {
			areas: {},
			configs: {},
		}
	},
})
