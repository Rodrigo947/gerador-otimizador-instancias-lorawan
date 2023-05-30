<template>
	<div class="px-2">
		<h2 class="pa-4 text-center">Configurações</h2>
		<v-text-field v-model="configs.seed" label="Seed" type="number" min="1"> </v-text-field>
		<v-text-field v-model="configs.clients" label="Clientes" type="number" min="1"> </v-text-field>
		<v-text-field
			v-model="configs.transmissionPower"
			label="Potência de transmissão"
			type="number"
			min="1"
			step="0.01"
			suffix="mW"
		>
		</v-text-field>
		<v-text-field
			v-model="configs.antennaGain"
			label="Ganho da antena"
			type="number"
			min="0"
			max="2.15"
			step="0.01"
			suffix="dBi"
		>
		</v-text-field>
		<v-select v-model="configs.frequency" :items="[433, 915]" label="Frequência" suffix="MHz"></v-select>
		<v-select v-model="configs.sf" :items="[7, 8, 9, 10, 11, 12]" label="SF"></v-select>
	</div>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { useMapStore } from '../../stores/mapStore.ts'
const ms = useMapStore()

const { configs } = storeToRefs(ms)
</script>
