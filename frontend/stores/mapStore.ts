import { defineStore } from 'pinia'

export const useMapStore = defineStore('mapStore', {
	state: () => ({
		areas: {},
		configs: {
			clients: 10,
			seed: 947,
		},
		btnDownloadDisabled: true,
		markersClients: [],
	}),
})
