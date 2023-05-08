<template>
	<v-navigation-drawer v-model="drawer" location="right" width="400" permanent>
		<MenuDataFormAreas v-if="lastBtnClicked === 'areas'" />
		<MenuDataFormConfigs v-else />
		<div class="d-flex flex-grow-1 align-end pa-4">
			<v-btn class="d-flex w-100" color="success" @click="generateInstace()">Gerar</v-btn>
		</div>
	</v-navigation-drawer>
</template>

<script setup>
import { useDrawerControls } from '../../stores/drawerControls.ts'
import { useMapStore } from '../../stores/mapStore.ts'
</script>

<script>
export default {
	data() {
		return {
			dc: useDrawerControls(),
			ms: useMapStore(),
		}
	},
	computed: {
		drawer() {
			return this.dc.drawer
		},
		lastBtnClicked() {
			return this.dc.lastBtnClicked
		},
		getAreas() {
			return this.ms.areas
		},
		getConfigs() {
			return this.ms.configs
		},
	},
	methods: {
		async generateInstace() {
			console.log(this.getConfigs)
			console.log(this.getAreas)

			const areas = []
			for (const area of Object.values(this.getAreas)) {
				areas.push({
					coordinates: area.coordinates[0],
					percent: area.percent,
				})
			}

			const response = await $fetch('api/generate_instance', {
				baseURL: this.$config.baseURL,
				method: 'POST',
				body: { areas: areas, configs: this.getConfigs },
			})
			console.log(response)
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
