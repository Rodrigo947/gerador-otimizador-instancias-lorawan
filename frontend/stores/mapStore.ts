import { defineStore } from 'pinia'

export const useMapStore = defineStore('mapStore', {
	state: () => ({
		areas: {},
		configs: {
			clients: 0,
		},
	}),
})
