<template>
	<v-app>
		<v-app-bar density="compact">
			<v-app-bar-title class="text-center">
				Gerador e Otimizador de Instâncias LoRaWAN
				<span class="float-right log">{{ total }} | {{ used_at }}</span>
			</v-app-bar-title>
		</v-app-bar>
		<v-main class="d-flex">
			<slot />
		</v-main>
	</v-app>
</template>

<script setup>
useHead({
	title: 'GOIL',
})
</script>

<script>
export default {
	data() {
		return {
			total: 0,
			used_at: null,
		}
	},

	methods: {
		async getLog() {
			const response = await $fetch('api/log', {
				baseURL: this.$config.baseURL,
				method: 'GET',
			})
			this.total = response.totalUse
			this.used_at = response.usedAt
		},
	},
	mounted() {
		this.getLog()
	},
}
</script>

<style scoped>
.log {
	font-size: 10px;
	color: #fff;
}
</style>
