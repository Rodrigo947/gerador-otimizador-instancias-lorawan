<template>
	<div id="map">
		<v-btn icon="mdi-cog" class="btnFloating btnConfig" @click="dc.changeDrawer('config')"></v-btn>
		<v-btn icon="mdi-vector-square-edit" class="btnFloating btnAreas" @click="dc.changeDrawer('areas')"></v-btn>
		<v-btn
			icon="mdi-download"
			class="btnFloating btnDownload"
			@click="downloadCSVData()"
			:disabled="downloadDisabled"
		></v-btn>
	</div>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { useDrawerControls } from '../stores/drawerControls.ts'
import { useInstanceStore } from '../stores/instanceStore.ts'
import { useMapStore } from '../stores/mapStore'
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
const { areas, markersClients, btnDownloadDisabled, configs } = storeToRefs(mapStore)

const instanceStore = useInstanceStore()
const { clientsCoordinates } = storeToRefs(instanceStore)

export default {
	data() {
		return {
			map: undefined,
			draw: new MapboxDraw(),
			availableColors: [
				'#a7c636',
				'#149ece',
				'#ed5151',
				'#9e559c',
				'#fc921f',
				'#ffde3e',
				'#f789d8',
				'#b7814a',
				'#3caf99',
				'#6b6bd6',
			],
			usedColors: [],
			areas: areas,
			markersClients: markersClients,
			clientsCoordinates: clientsCoordinates,
			downloadDisabled: btnDownloadDisabled,
			configs: configs,
			drawer: drawer,
		}
	},
	watch: {
		clientsCoordinates(newClients) {
			this.deleteMarkers()

			for (const client of newClients) {
				const marker = this.createMarker(client.longitude, client.latitude)
				this.markersClients.push(marker)
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

			let index = 0
			let chosenColor = this.availableColors[index]
			while (this.usedColors.includes(chosenColor) && this.usedColors.length < this.availableColors.length) {
				index += 1
				chosenColor = this.availableColors[index]
			}
			this.usedColors.push(chosenColor)

			this.map.addLayer({
				id: `${e.features[0].id}_fill`,
				type: 'fill',
				source: e.features[0].id,
				paint: {
					'fill-color': chosenColor,
					'fill-opacity': 0.6,
				},
			})

			this.areas[e.features[0].id] = {
				coordinates: e.features[0].geometry.coordinates,
				color: chosenColor,
				percent: 0,
			}
		},

		deleteArea(e) {
			this.map.removeLayer(`${e.features[0].id}_fill`)
			this.map.removeSource(e.features[0].id)

			const chosenColor = this.areas[e.features[0].id].color
			const index = this.usedColors.indexOf(chosenColor)
			this.usedColors.splice(index, 1)

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

			this.mapStore.areas[e.features[0].id].coordinates = e.features[0].geometry.coordinates
		},

		createMarker(long, lat) {
			const marker = new mapboxgl.Marker({ color: '#4545f0' }).setLngLat([long, lat]).addTo(this.map)
			return marker
		},

		deleteMarkers() {
			if (this.markersClients.length > 0) {
				for (let i = 0; i < this.markersClients.length; i++) {
					this.markersClients[i].remove()
				}
			}
		},

		downloadCSVData() {
			let areaConfigs = []
			for (const area of Object.values(this.areas)) {
				areaConfigs.push({
					coordinates: area.coordinates[0],
					percent: parseInt(area.percent),
				})
			}

			let json = {
				seed: this.configs.seed,
				totalClients: this.clientsCoordinates.length,
				areaConfigs: areaConfigs,
				clientsCoordinates: this.clientsCoordinates,
			}

			const objectDate = new Date()
			const day = objectDate.getDate()
			const month = objectDate.getMonth()
			const year = objectDate.getFullYear()
			const seed = this.configs.seed
			const clients = this.clientsCoordinates.length

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

.btnAreas {
	top: 8%;
}

.btnConfig {
	top: 15%;
}

.btnDownload {
	top: 22%;
}
</style>
