<template>
	<div id="map">
		<v-btn
			icon="mdi-weight"
			class="btnFloating btnAreas"
			title="Pesos das áreas"
			@click="dc.changeDrawer('areas')"
		></v-btn>
		<v-btn
			icon="mdi-cog"
			class="btnFloating btnConfig"
			title="Configurações"
			@click="dc.changeDrawer('config')"
		></v-btn>
		<v-btn
			icon="mdi-download"
			class="btnFloating btnDownload"
			title="Download da instância gerada"
			@click="downloadJSONData()"
			:disabled="downloadDisabled"
		></v-btn>
		<v-btn
			:icon="btnShowHide == 'hide' ? 'mdi-vector-square-minus' : 'mdi-vector-square-plus'"
			size="x-small"
			class="btnFloatingLeft btnHideShow"
			:title="btnShowHide == 'hide' ? 'Esconder áreas' : 'Mostrar áreas'"
			@click="btnShowHide == 'hide' ? hideAreas() : showAreas()"
			:disabled="Object.keys(areas).length <= 0"
		></v-btn>

		<v-btn
			:icon="btnShowHideGateways == 'hide' ? 'mdi-router-wireless-off' : 'mdi-router-wireless'"
			size="x-small"
			class="btnFloatingLeft btnHideShowGatetays"
			:title="btnShowHideGateways == 'hide' ? 'Esconder gateways' : 'Mostrar gateways'"
			@click="btnShowHideGateways == 'hide' ? hideMarkersGateways() : showMarkersGateways()"
			:disabled="markersGateways.length <= 0"
		></v-btn>

		<v-btn
			size="x-small"
			class="btnFloatingLeft btnHideShowClients"
			:icon="btnShowHideClients == 'hide' ? 'mdi-map-marker-minus' : 'mdi-map-marker-plus'"
			:title="btnShowHideClients == 'hide' ? 'Esconder clientes' : 'Mostrar Clientes'"
			:disabled="markersClients.length <= 0"
			@click="btnShowHideClients == 'hide' ? hideMarkersClients() : showMarkersClients()"
		></v-btn>
	</div>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { useDrawerControls } from '../stores/drawerControls.ts'
import { useInstanceStore } from '../stores/instanceStore.ts'
import { useMapStore } from '../stores/mapStore'
import gerarCorRandomica from '../utils/gerarCorRandomica'
const dc = useDrawerControls()
</script>

<script>
import MapboxDraw from '@mapbox/mapbox-gl-draw'
import '@mapbox/mapbox-gl-draw/dist/mapbox-gl-draw.css'
import MapboxGeocoder from '@mapbox/mapbox-gl-geocoder'
import '@mapbox/mapbox-gl-geocoder/dist/mapbox-gl-geocoder.css'
import mapboxgl from 'mapbox-gl'
import { ZoomControl } from 'mapbox-gl-controls'
import 'mapbox-gl-controls/lib/controls.css'
import 'mapbox-gl/dist/mapbox-gl.css'

const drawerControls = useDrawerControls()
const { drawer } = storeToRefs(drawerControls)

const mapStore = useMapStore()
const { areas, markersClients, btnDownloadDisabled, configs, markersGateways } = storeToRefs(mapStore)

const instanceStore = useInstanceStore()
const { clientsStore, gatewaysStore } = storeToRefs(instanceStore)

export default {
	data() {
		return {
			map: undefined,
			draw: new MapboxDraw(),
			allDrawAreas: undefined,
			areas: areas,
			markersClients: markersClients,
			markersGateways: markersGateways,
			clients: clientsStore,
			gateways: gatewaysStore,
			downloadDisabled: btnDownloadDisabled,
			configs: configs,
			drawer: drawer,
			btnShowHide: 'hide',
			btnShowHideClients: 'hide',
			btnShowHideGateways: 'hide',
			usedColors: [],
		}
	},
	watch: {
		async clients(newClients) {
			await this.hideMarkersClients()
			let size = this.markersClients.length
			for (let i = 0; i < size; i++) {
				this.markersClients.pop()
			}
			this.usedColors = []
			this.btnShowHideClients = 'hide'
			for (const client of newClients) {
				const marker = this.createMarker(client.longitude, client.latitude, client.gateway_index)
				this.markersClients.push(marker)
			}

			await this.hideMarkersGateways()
			size = this.markersGateways.length
			for (let i = 0; i < size; i++) {
				this.markersGateways.pop()
			}
			this.btnShowHideGateways = 'hide'
			for (const [index, gateway] of this.gateways.entries()) {
				const marker = this.createGateway(gateway.longitude, gateway.latitude, index)
				this.markersGateways.push(marker)
			}
		},
		drawer(newValue) {
			if (!newValue) {
				setTimeout(() => this.map.resize(), 210)
			}
		},
	},
	mounted() {
		mapboxgl.accessToken = this.$config.MAPBOX_TOKEN

		this.map = new mapboxgl.Map({
			container: 'map',
			style: 'mapbox://styles/mapbox/streets-v12',
			center: [-43.353550493837616, -21.769316449825027],
			zoom: 12,
		})

		this.draw = new MapboxDraw({
			displayControlsDefault: false,
			userProperties: true,

			controls: {
				polygon: true,
				trash: true,
			},

			defaultMode: 'draw_polygon',
		})

		const geocoder = new MapboxGeocoder({
			accessToken: mapboxgl.accessToken,
			mapboxgl: mapboxgl,
			countries: 'br',
			language: 'pt',
		})

		this.map.addControl(geocoder, 'top-right')
		this.map.addControl(new ZoomControl(), 'top-left')
		this.map.addControl(this.draw, 'top-left')

		this.map.on('draw.create', this.createArea)
		this.map.on('draw.delete', this.deleteArea)
		this.map.on('draw.update', this.updateArea)
	},
	methods: {
		createArea(e) {
			this.map.addSource(e.features[0].id, {
				type: 'geojson',
				data: e.features[0],
			})

			const color = gerarCorRandomica()

			this.map.addLayer({
				id: `${e.features[0].id}_fill`,
				type: 'fill',
				source: e.features[0].id,
				paint: {
					'fill-color': color,
					'fill-opacity': 0.6,
				},
			})

			this.areas[e.features[0].id] = {
				coordinates: e.features[0].geometry.coordinates,
				color: color,
				percent: 0,
				features: e.features[0],
			}
		},

		deleteArea(e) {
			this.map.removeLayer(`${e.features[0].id}_fill`)
			this.map.removeSource(e.features[0].id)

			delete this.areas[e.features[0].id]
		},

		updateArea(e) {
			this.map.removeLayer(`${e.features[0].id}_fill`)
			this.map.removeSource(e.features[0].id)

			this.map.addSource(e.features[0].id, {
				type: 'geojson',
				data: e.features[0],
			})

			this.map.addLayer({
				id: `${e.features[0].id}_fill`,
				type: 'fill',
				source: e.features[0].id,
				paint: {
					'fill-color': this.areas[e.features[0].id].color,
					'fill-opacity': 0.6,
				},
			})

			this.areas[e.features[0].id].coordinates = e.features[0].geometry.coordinates
			this.areas[e.features[0].id].features = e.features[0]
		},

		hideAreas() {
			this.btnShowHide = 'show'
			this.allDrawAreas = this.draw.getAll()
			this.draw.deleteAll()
			for (const index of Object.keys(this.areas)) {
				this.map.removeLayer(`${index}_fill`)
				this.map.removeSource(index)
			}
		},

		showAreas() {
			this.btnShowHide = 'hide'
			this.draw.set(this.allDrawAreas)
			this.allDrawAreas = undefined

			for (const [index, area] of Object.entries(this.areas)) {
				this.map.addSource(index, {
					type: 'geojson',
					data: area.features,
				})

				this.map.addLayer({
					id: `${index}_fill`,
					type: 'fill',
					source: index,
					paint: {
						'fill-color': area.color,
						'fill-opacity': 0.6,
					},
				})
			}
		},

		createMarker(long, lat, cluster) {
			if (this.usedColors.length <= cluster) {
				const color = gerarCorRandomica()
				this.usedColors.push(color)
			}

			const marker = new mapboxgl.Marker({ color: this.usedColors[cluster] }).setLngLat([long, lat]).addTo(this.map)
			return marker
		},

		createGateway(long, lat, cluster) {
			const el = document.createElement('i')
			el.className = 'mdi-router-wireless  mdi v-icon v-theme--light v-icon--size-x-large'
			el.style.color = this.usedColors[cluster]
			const gateway = new mapboxgl.Marker(el).setLngLat([long, lat]).addTo(this.map)
			return gateway
		},

		async hideMarkersClients() {
			this.btnShowHideClients = 'show'
			if (this.markersClients.length > 0) {
				for (let i = 0; i < this.markersClients.length; i++) {
					this.markersClients[i].remove()
				}
			}
		},

		async hideMarkersGateways() {
			this.btnShowHideGateways = 'show'
			if (this.markersGateways.length > 0) {
				for (let i = 0; i < this.markersGateways.length; i++) {
					this.markersGateways[i].remove()
				}
			}
		},

		showMarkersClients() {
			this.btnShowHideClients = 'hide'
			if (this.markersClients.length > 0) {
				for (let i = 0; i < this.markersClients.length; i++) {
					this.markersClients[i].addTo(this.map)
				}
			}
		},

		showMarkersGateways() {
			this.btnShowHideGateways = 'hide'
			if (this.markersGateways.length > 0) {
				for (let i = 0; i < this.markersGateways.length; i++) {
					this.markersGateways[i].addTo(this.map)
				}
			}
		},

		downloadJSONData() {
			let areaConfigs = []
			for (const area of Object.values(this.areas)) {
				areaConfigs.push({
					coordinates: area.coordinates[0],
					percent: parseInt(area.percent),
				})
			}

			let json = {
				configs: this.configs,
				areaConfigs: areaConfigs,
				clients: this.clients,
				gateways: this.gateways,
			}

			const objectDate = new Date()
			const day = objectDate.getDate()
			const month = objectDate.getMonth()
			const year = objectDate.getFullYear()
			const seed = this.configs.seed
			const clients = this.clients.length

			const name_file = `S${seed}_C${clients}_Y${year}_M${month}_D${day}.json`

			const anchor = document.createElement('a')
			anchor.href = 'data:text/json;charset=utf-8,' + JSON.stringify(json, null, 2)
			anchor.target = '_blank'
			anchor.download = name_file
			anchor.click()
		},
	},
}
</script>

<style scope>
#map {
	flex: 1;
}

.btnFloating {
	position: absolute;
	right: 0.5%;
	z-index: 1;
	transition: all 0.2s;
}

.btnFloatingLeft {
	position: absolute;
	left: 9px;
	z-index: 1;
	transition: all 0.2s;
}

.btnAreas {
	top: 60px;
}

.btnConfig {
	top: 120px;
}

.btnDownload {
	top: 180px;
}

.btnHideShow {
	top: 150px;
}

.btnHideShowClients {
	top: 190px;
}

.btnHideShowGatetays {
	top: 230px;
}

.v-icon--size-x-large {
	font-size: calc(var(--v-icon-size-multiplier) * 3em);
}
</style>
