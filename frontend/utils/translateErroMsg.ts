type IObjectErro = {
	areas?: Array<String>
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
}
