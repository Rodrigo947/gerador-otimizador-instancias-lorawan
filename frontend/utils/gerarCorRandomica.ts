export default function gerarCorRandomica() {
	// Gerar valores aleatórios para R, G e B
	const r = Math.floor(Math.random() * 256)
	const g = Math.floor(Math.random() * 256)
	const b = Math.floor(Math.random() * 256)

	// Construir a cor no formato hexadecimal
	const corHex = '#' + componentToHex(r) + componentToHex(g) + componentToHex(b)

	return corHex
}

function componentToHex(c: number) {
	const hex = c.toString(16)
	return hex.length == 1 ? '0' + hex : hex
}
