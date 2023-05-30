<template>
	<v-navigation-drawer v-model="drawer" location="right" width="400" permanent>
		<MenuDataFormAreas v-if="lastBtnClicked === 'areas'" />
		<MenuDataFormConfigs v-else />
		<div class="d-flex flex-grow-1 align-end pa-4">
			<v-snackbar v-model="showMsg" color="red-darken-1" location="right top" multi-line>
				{{ erroMsg }}
				<template v-slot:actions>
					<v-btn icon="mdi-close" @click="showMsg = false"> </v-btn>
				</template>
			</v-snackbar>
			<v-btn class="d-flex w-100" color="success" @click="generateInstace()" :disabled="isLoading" :loading="isLoading">
				GERAR
			</v-btn>
		</div>
	</v-navigation-drawer>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { useDrawerControls } from '../../stores/drawerControls.ts'
import { useInstanceStore } from '../../stores/instanceStore.ts'
import { useMapStore } from '../../stores/mapStore.ts'
import translateErroMsg from '../../utils/translateErroMsg.ts'
import validateData from '../../utils/validateData'

const drawerControls = useDrawerControls()
const { drawer, lastBtnClicked } = storeToRefs(drawerControls)
</script>

<script>
const mapStore = useMapStore()
const { areas, configs, btnDownloadDisabled } = storeToRefs(mapStore)

const instanceStore = useInstanceStore()
const { clientsStore, gatewaysStore } = storeToRefs(instanceStore)

export default {
	data() {
		return {
			isLoading: false,
			showMsg: false,
			erroMsg: '',
			areas: areas,
			configs: configs,
			clients: clientsStore,
			gateways: gatewaysStore,
			downloadDisabled: btnDownloadDisabled,
		}
	},
	methods: {
		async generateInstace() {
			this.isLoading = true

			const erroMsg = validateData()
			if (erroMsg !== 'valid') {
				this.showMsg = true
				this.erroMsg = erroMsg
				this.isLoading = false
				return
			}

			const areasSend = []
			for (const area of Object.values(this.areas)) {
				areasSend.push({
					coordinates: area.coordinates[0],
					percent: area.percent,
				})
			}

			try {
				const response = await $fetch('api/generate_instance', {
					baseURL: this.$config.baseURL,
					method: 'POST',
					body: { areas: areasSend, configs: this.configs },
				})

				let clients = []
				let gateways = []
				for (const row of response.data) {
					for (const client of row.clients) {
						clients.push(client)
					}

					gateways.push(row.gateway)
				}

				this.clients = clients
				this.gateways = gateways
				this.downloadDisabled = false
			} catch (error) {
				this.showMsg = true
				this.erroMsg = translateErroMsg(error.response._data)
			}

			this.isLoading = false
		},
	},
}
</script>

<style scope>
.v-navigation-drawer__content {
	display: flex;
	flex-direction: column;
}
</style>
