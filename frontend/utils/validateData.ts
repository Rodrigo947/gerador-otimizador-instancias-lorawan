import { useMapStore } from '../stores/mapStore'

export default function validateData() {
	const mapStore = useMapStore()
	const areas = mapStore.areas as Object
	const clients = mapStore.configs.clients
	const transmissionPower = mapStore.configs.transmissionPower
	const antennaGain = mapStore.configs.antennaGain
	const frequency = mapStore.configs.frequency
	const seed = mapStore.configs.seed
	const sf = mapStore.configs.sf

	let totalPercent = 0

	if (clients <= 0) {
		return 'A quantidade de clientes deve ser maior que 0'
	}

	if (![5, 20, 50, 100].includes(transmissionPower)) {
		return 'Potência de transmissão inválida'
	}

	if (antennaGain < 0.01) {
		return 'O ganho de antena deve ser maior ou igual que 0.01'
	}

	if (![433, 915].includes(frequency)) {
		return 'Frequência inválida'
	}

	if (![7, 8, 9, 10, 11, 12].includes(sf)) {
		return 'SF inválido'
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
