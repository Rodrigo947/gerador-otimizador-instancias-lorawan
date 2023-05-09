<template>
	<div class="px-2">
		<h2 class="pa-4 text-center">Configurações</h2>
		<v-text-field v-model="configs.seed" label="Seed" type="number" min="1"> </v-text-field>
		<v-text-field v-model="configs.clients" label="Clientes" type="number" min="1"> </v-text-field>
	</div>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { useMapStore } from '../../stores/mapStore.ts'
const ms = useMapStore()

const { configs } = storeToRefs(ms)
</script>
