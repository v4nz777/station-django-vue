<template>
    <div class="w-full flex my-1" v-if="isPresent">
        <button class="items-center align-bottom hover:text-blue-500 relative z-20"
        :class="playing?'text-red-500':'',waiting? 'animate-bounce':''"
        @click="playAudio">
            <i class="block h-6 w-6" v-if="played"><StopIcon/></i>
            <i class="block h-6 w-6" v-else><PlayIcon /></i>
            <div v-if="clicked" class="rounded-full w-6 h-6 bg-sky-500 animate-ping absolute top-0 bottom-0 left-0 right-0"></div>
        </button>
        <div class="flex items-center justify-between w-full bg-gray-300 rounded-r-full relative shadow-xl">
            <span class="align-center text-sm font-light ml-2">{{name.length > 25?name.substring(0,25) + '...' + name.substring(name.length-3,name.length):name}}
            </span>
            <span v-if="duration" class="text-xs font-semibold mr-2">{{duration - current + 's'}}</span>
            <div class="absolute top-0 bg-red-300 h-full rounded-r-full"
                :style="played? {animationName:'loadingfx',animationDuration:duration+'s'}:{}"
                id="duration">
            </div>
        </div>
    </div>
    <div v-else>
        <p class="text-red-500">Audio file deleted or missing!</p>
    </div>
</template>
<script setup>
import { ref, onBeforeMount, onBeforeUnmount, watch } from 'vue';
import { PlayIcon, PauseIcon, StopIcon } from '@heroicons/vue/solid';
import axios from 'axios';

const props = defineProps({
    id: Number,
    index: Number
})
const emits = defineEmits(['toggle'])

const clicked = ref(false)
const played = ref(false)
const waiting = ref(false)
const playing = ref(false)
const current = ref(0)
const duration = ref(0)
const url = ref("")
const name = ref("")
const audio = ref({})
const isPresent = ref(false)

setInterval(() => {
    current.value = Math.round(audio.value.currentTime)
}, 1000);

const load = async ()=> {
    try {
        const response = await axios.get(`/audiofile/${props.id}`)
        url.value = response.data.file
        name.value = response.data.filename

        audio.value = new Audio(`http://localhost:8000${url.value}`)

        // Add event listeners for audio
        audio.value.onended = ()=> {
            // audio.currentTime = 0
            played.value = false
            playing.value = false
        }
        audio.value.onplaying = ()=> {
            playing.value = true
            // duration.value = Math.ceil(audio.value.duration)
            
        }
        audio.value.onloadedmetadata = ()=> {
            duration.value = Math.ceil(audio.value.duration)

        }
        isPresent.value = true
    }catch{
        return
    }
}

onBeforeMount( ()=> {
    load()

})

//update component whenever the id change
watch(()=> props.id,(newID,oldID)=> {
    if(newID !== oldID) load() //reload
})

onBeforeUnmount(()=> {
    if(played.value) {
        audio.value.pause()
        audio.value.currentTime = 0
        played.value = false
        playing.value = false
    }
    audio.value = {}
})

const playAudio = async () => {
    clicked.value = true
    if(!played.value){
        waiting.value = true
        const playpromise = await audio.value.play()
        played.value = true
        waiting.value = false


    }else if(played.value){
        audio.value.pause()
        audio.value.currentTime = 0
        played.value = false
        playing.value = false
        waiting.value = false
    }
    setTimeout(() => {
        clicked.value = false
    }, 1000);
   
}



</script>
<style>
    @keyframes loadingfx {
        from{width:0%;}
        to{width:100%;}
    }

</style>