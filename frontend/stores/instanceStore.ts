import { defineStore } from 'pinia'

export const useInstanceStore = defineStore('instanceStore', {
	state: () => ({
		clientsStore: [],
		gatewaysStore: [],
	}),
})
