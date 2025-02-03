<template>
	<v-dialog v-model="dialog" width="500" persistent>
		<v-card max-width="400">
			<v-card-title> Bem-vindo </v-card-title>

			<v-card-text>Este é o sistema de geração de instâncias da rede LoRaWAN.</v-card-text>

			<v-list density="compact" :items="links" subheader="LINKS"> </v-list>
			<v-card-actions>
				<v-btn variant="tonal" class="d-flex w-100" @click="dialog = false">Acessar</v-btn>
			</v-card-actions>
		</v-card>
	</v-dialog>
</template>

<script>
export default {
	data() {
		return {
			dialog: true,
			links: [
				{
					title: 'Vídeo explicativo',
					props: {
						href: 'https://www.youtube.com/watch?v=ka7KGQt5l0Y',
						target: '_blank',
						prependIcon: 'mdi-youtube',
						appendIcon: 'mdi-menu-right',
					},
				},
				{
					title: 'Código fonte',
					link: true,
					props: {
						href: ' https://github.com/Rodrigo947/gerador-otimizador-instancias-lorawan',
						target: '_blank',
						prependIcon: 'mdi-github',
						appendIcon: 'mdi-menu-right',
					},
				},
				{
					title: 'Artigo',
					link: true,
					props: {
						href: 'https://sol.sbc.org.br/index.php/sbrc_estendido/article/view/29953',
						target: '_blank',
						prependIcon: 'mdi-file-sign',
						appendIcon: 'mdi-menu-right',
					},
				},
			],
		}
	},
}
</script>
