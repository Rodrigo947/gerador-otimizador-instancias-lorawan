<template>
	<v-navigation-drawer v-model="drawer" permanent location="right">
		<h2 class="pa-4 text-center">Regiões</h2>

		<div class="px-2">
			<div v-for="area in areas">
				<v-text-field label="Qtd de usuários">
					<template v-slot:prepend-inner>
						<v-icon :color="area.color" icon="mdi-circle"></v-icon>
					</template>
				</v-text-field>
			</div>
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
			mapStore: useMapStore(),
		}
	},
	computed: {
		drawer() {
			return this.dc.drawer
		},
		areas() {
			return this.mapStore.areas
		},
	},
}
</script>
