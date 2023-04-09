<template>
	<div id="map"></div>
</template>

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
			draw: undefined,
		}
	},

	mounted() {
		mapboxgl.accessToken = this.$config.MAPBOX_TOKEN

		this.map = new mapboxgl.Map({
			container: 'map',
			style: 'mapbox://styles/mapbox/streets-v12',
		})

		this.draw = new MapboxDraw({
			displayControlsDefault: false,

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

		this.map.on('draw.create', this.updateArea)
		this.map.on('draw.delete', this.updateArea)
		this.map.on('draw.update', this.updateArea)
	},

	methods: {
		updateArea(e) {
			console.log(e)
		},
	},
}
</script>

<style>
#map {
	flex: 1;
}
</style>
