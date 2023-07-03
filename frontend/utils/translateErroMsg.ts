type IObjectErro = {
	areas?: Array<String>
	configs?: Array<String>
}

export default function translateErroMsg(objectErro: IObjectErro) {
	if (objectErro.areas) {
		switch (objectErro.areas[0]) {
			case 'Invalid area':
				return 'Alguma área não foi desenhada corretamente'

			default:
				return `Houve algum erro desconhecido. Erro: ${objectErro.areas[0]}`
		}
	}
	if (objectErro.configs) {
		switch (objectErro.configs[0]) {
			case "Value of clients isn't a number.":
			case 'Value of clients must be greater than 0':
				return 'Valor da quantidade de clientes inválido'

			case "Value of seed isn't a number.":
			case 'Value of seed must be greater than 0':
				return 'Seed inválida'

			case "Value of transmission power isn't a number.":
			case 'Value of transmission power invalid. Only accept 5, 20, 50 or 100.':
				return 'Potência de transmissão inválido'

			case "Value of antenna gain power isn't a number.":
			case 'Value of antenna gain must be greater or equal than 0.01.':
				return 'Ganho da antena inválido'

			case "Value of frequency isn't a number.":
			case 'Value of frequency invalid. Only accept 433 or 915.':
				return 'Frequência inválida'

			case "Value of SF isn't a number.":
			case 'Value of SF invalid. Only accept 7, 8, 9, 10, 11 or 12.':
				return 'SF inválido'

			default:
				return `Houve algum erro desconhecido. Erro: ${objectErro.configs[0]}`
		}
	}
}
