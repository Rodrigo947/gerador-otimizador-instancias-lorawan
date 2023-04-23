<template>
	<div class="px-2">
		<h2 class="pa-4 text-center">Configurações</h2>
		<v-text-field v-model="clients" label="Clientes" type="number" min="1"> </v-text-field>
	</div>
</template>
<script>
export default {
	data() {
		return {
			clients: 0,
		}
	},
}
</script>
