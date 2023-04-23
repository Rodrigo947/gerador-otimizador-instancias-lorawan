<template>
	<v-navigation-drawer v-model="drawer" permanent location="right"> </v-navigation-drawer>
</template>

<script setup>
const drawer = useState('drawer', () => false)
</script>
