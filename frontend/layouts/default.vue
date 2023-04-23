<template>
	<v-app>
		<v-app-bar density="compact">
			<v-app-bar-title class="text-center">Gerador e Otimizador de Instâncias LoRaWAN</v-app-bar-title>
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
