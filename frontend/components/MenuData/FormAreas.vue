<template>
	<div class="px-2">
		<h2 class="pa-4 text-center">Pesos das áreas</h2>

		<v-list v-if="Object.values(areas).length === 0">
			<v-list-subheader>Para desenhar uma área:</v-list-subheader>
			<v-list-item> 1. Selecione a ferramenta de desenho <v-icon icon="mdi-vector-square"></v-icon> </v-list-item>
			<v-list-item>2. Selecione os pontos até que forme a área desejada</v-list-item>
			<v-list-item>3. Para finalizar, clique em ponto já criado que feche o desenho</v-list-item>
		</v-list>

		<div v-else>
			<v-list>
				<v-list-item>1. Informe o peso que cada area terá na geração de clientes</v-list-item>
				<v-list-item>2. Quanto maior o peso maior a probabildade de clientes serem gerados na área.</v-list-item>
				<v-list-item>3. A soma dos pesos deve ser igual a 100%</v-list-item>
			</v-list>
			<div v-for="area in areas" :key="area.id">
				<v-text-field label="Peso" v-model="area.percent" type="number" suffix="%" min="0" max="100">
					<template v-slot:prepend-inner>
						<v-icon :color="area.color" icon="mdi-circle"></v-icon>
					</template>
				</v-text-field>
			</div>
			<v-list-item>Total do peso: {{ totalPercent }}%</v-list-item>
		</div>
	</div>
</template>

<script setup>
import { useMapStore } from '../../stores/mapStore.ts'
</script>

<script>
export default {
	data() {
		return {
			mapStore: useMapStore(),
		}
	},
	computed: {
		areas() {
			return this.mapStore.areas
		},
		totalPercent() {
			let total = 0
			for (const area of Object.values(this.areas)) {
				total += parseInt(area.percent)
			}
			return total
		},
	},
}
</script>
