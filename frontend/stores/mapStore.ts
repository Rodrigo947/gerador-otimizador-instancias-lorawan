import { defineStore } from 'pinia'

export const useMapStore = defineStore('mapStore', {
	state: () => ({
		areas: {},
		configs: {
			clients: 10,
			transmissionPower: 25.11,
			antennaGain: 2.15,
			frequency: 915,
			seed: 947,
			sf: 7,
		},
		btnDownloadDisabled: true,
		markersClients: [],
		markersGateways: [],
	}),
})
