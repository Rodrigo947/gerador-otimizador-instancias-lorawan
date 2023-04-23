<template>
	<v-navigation-drawer v-model="drawer" location="right" width="400">
		<MenuDataFormAreas v-if="lastBtnClicked === 'areas'" />
		<MenuDataFormConfigs v-else />
		<div class="d-flex flex-grow-1 align-end pa-4">
			<v-btn class="d-flex w-100" color="success">Gerar</v-btn>
		</div>
	</v-navigation-drawer>
</template>

<script setup>
import { useDrawerControls } from '../../stores/drawerControls.ts'
</script>

<script>
export default {
	data() {
		return {
			dc: useDrawerControls(),
		}
	},
	computed: {
		drawer() {
			return this.dc.drawer
		},
		lastBtnClicked() {
			return this.dc.lastBtnClicked
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
