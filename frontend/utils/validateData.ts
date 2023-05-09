import { useMapStore } from '../stores/mapStore'

export default function validateData() {
	const mapStore = useMapStore()
	const clients = mapStore.configs.clients
	const seed = mapStore.configs.seed
	const areas = mapStore.areas as Object
	let totalPercent = 0

	if (clients <= 0) {
		return 'A quantidade de clientes deve ser maior que 0'
	}

	if (seed <= 0) {
		return 'A seed deve ser maior que 0'
	}

	if (Object.keys(areas).length === 0) {
		return 'Informe pelo menos uma área'
	}

	for (const area of Object.values(areas)) {
		totalPercent += parseInt(area.percent)
	}

	if (totalPercent !== 100) {
		return 'A soma dos pesos das áreas deve ser igual a 100'
	}

	return 'valid'
}
