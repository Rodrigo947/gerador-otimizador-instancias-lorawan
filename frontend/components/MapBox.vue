<template>
	<div id="map">
		<v-btn icon="mdi-vector-square-edit" class="btnFloating btnRegions" @click="drawer = !drawer"></v-btn>
		<v-btn icon="mdi-cog" class="btnFloating btnConfig" @click="drawer = !drawer"></v-btn>
	</div>
</template>

<script setup>
import { useMapStore } from '../stores/mapStore'
const drawer = useState('drawer')
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

export default {
	data() {
		return {
			map: undefined,
			draw: new MapboxDraw(),
			availableColors: ['#ae9eea', '#efd15e', '#ab1e13'],
			usedColors: [],
			mapStore: useMapStore(),
		}
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
			while (this.usedColors.includes(chosenColor)) {
				index += 1
				chosenColor = this.availableColors[index]
			}
			this.usedColors.push(chosenColor)

			this.map.addLayer({
				id: `${e.features[0].id}_fill`,
				type: 'fill',
				source: e.features[0].id,
				paint: {
					'fill-color': chosenColor, // blue color fill
					'fill-opacity': 0.6,
				},
			})

			this.mapStore.areas[e.features[0].id] = {
				coordinates: e.features[0].geometry.coordinates,
				color: chosenColor,
			}
		},

		deleteArea(e) {
			this.map.removeLayer(`${e.features[0].id}_fill`)
			this.map.removeSource(e.features[0].id)

			const chosenColor = this.mapStore.areas[e.features[0].id].color
			const index = this.usedColors.indexOf(chosenColor)
			this.usedColors.splice(index, 1)

			delete this.mapStore.areas[e.features[0].id]
		},

		updateArea(e) {
			this.deleteArea(e)
			this.createArea(e)
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

.btnConfig {
	top: 8%;
}

.btnRegions {
	top: 15%;
}
</style>
