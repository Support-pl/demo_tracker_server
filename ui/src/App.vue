<template>
  <div id="app">
    <Map v-if="token" :token="token" :stime="stime"/>
  </div>
</template>

<script>
import Map from './components/Map.vue'

export default {
  name: 'App',
  components: {
    Map
  },
  data(){
    return {
      token: false,
      stime: Math.round(Date.now() / 1000) - 86400
    }
  },
  async mounted() {
    var urlParams = new URLSearchParams(window.location.search);
    this.token = urlParams.get('token');
    if(urlParams.get('stime')) this.stime = urlParams.get('stime');
  },
}
</script>