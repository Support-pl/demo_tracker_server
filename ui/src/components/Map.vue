<template>
    <div class="Map" id="map_canvas" width="100%" height="60%" style="min-height: 600px" />
</template>

<script>
import axios from "axios";

export default {
    props: {
        token: {
            required: true
        },
        stime: {
            default: Math.round(Date.now() / 1000) - 86400
        }
    },
    data(){
        return {
            cords: [],
            markers: [],
            google: false,
            maps_token: ''
        }
    },
    async mounted() {
        let vm = this;

        var map_loader = async function(){
            let { default: gmapsInit } = await import('../utils/gmaps.js');
            vm.google = await gmapsInit(vm.maps_token);
            
            vm.map = new vm.google.maps.Map(vm.$el);
        }

        vm.cords = (await axios.get('/read', { params: {token: vm.token, stime: vm.stime, etime: -1 }})).data;
        
        vm.maps_token = (await axios.get('/maps_token')).data;
        await map_loader();

        vm.buildMarkers();
        vm.drawChronology();
    },
    methods: {
        ts2dt(ts){
            let date = new Date(ts * 1000);
            return [
                date.getFullYear(),
                date.getMonth()+1,
                date.getDate(),
                date.getHours(),
                date.getMinutes(),
                date.getSeconds(),
            ]
        },
        buildMarkers(){
            let vm = this;

            for(let i = 0; i < vm.cords.length; i++){
                vm.markers.push(
                    new vm.google.maps.Marker({
                        map: vm.map,
                        position: vm.cords[i],
                        clickable: false,
                        animation: vm.google.maps.Animation.DROP,
                        title: i + 1 != vm.cords.length ? null : 'current',
                        icon: i + 1 != vm.cords.length ? {
                            path: vm.google.maps.SymbolPath.CIRCLE,
                            fillColor: '#FFF',
                            fillOpacity: 1,
                            strokeColor: '#000',
                            strokeOpacity: 1,
                            strokeWeight: 1,
                            scale: 5,
                        } : {
                            path: vm.google.maps.SymbolPath.CIRCLE,
                            fillColor: 'blue',
                            fillOpacity: 1,
                            strokeColor: '#FFF',
                            strokeOpacity: 1,
                            strokeWeight: 3,
                            scale: 15,
                        }
                    })
                )
            }
            vm.map.setCenter(vm.cords[vm.cords.length - 1]);
            vm.map.setZoom(10);
        },
        drawChronology(){
            let vm = this;
            vm.line = new vm.google.maps.Polyline({
                path: vm.cords.map(obj => new vm.google.maps.LatLng(obj)),
                geodesic: true,
                strokeColor: '#42d1f5',
                strokeOpacity: 1.0,
                strokeWeight: 3
            });
            vm.line.setMap(vm.map);
        }
    },
}
</script>