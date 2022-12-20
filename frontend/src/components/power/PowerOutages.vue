<template>
    <div class="md:w-96 w-screen h-max bg-white p-3 shadow-lg rounded-2xl my-5 flex justify-between px-5">

        <div>
            <p class="text-lg font-bold mb-2 text-gray-600">{{dtInterrupted.complete_date}}</p>
            <p class="text-sm">Interrupted: <span class="text-sky-500 font-bold">{{dtInterrupted.complete_time}}</span></p>
            <p class="text-sm">Restored: 
                <span class="text-sky-500 font-bold">{{dtRestored.complete_time}}</span>
                <span class="text-gray-500 text-xs italic" v-if="dtRestored.complete_date !== dtInterrupted.complete_date"> ({{dtRestored.complete_date}})</span>
            </p>


        </div>
        <div class="w-max flex flex-col items-center justify-center">

            <p class="text-red-500 font-bold" v-if="datum.duration_hours">
                {{datum.duration_hours}} hr{{datum.duration_hours > 1?'s':''}} :
                {{datum.duration_minutes}} min{{datum.duration_minutes > 1?'s':''}}
            </p>
            <p class="text-red-500 font-bold" v-else>
                {{datum.duration_minutes}} minute{{datum.duration_minutes > 1?'s':''}}
            </p>

            <div v-if="datum.scheduled" class="text-xs font-bold bg-green-500 text-white w-max text-center px-2 py-1 rounded-full">
                SCHEDULED
            </div>
            <div v-else class="text-xs font-bold bg-yellow-500 text-white w-max text-center px-2 py-1 rounded-full">
                UNSCHEDULED
            </div>
 
        </div>


    </div>
</template>

<script setup>
 import { ref, onMounted, watch } from 'vue';
 import { TrendingUpIcon, TrendingDownIcon, ArrowNarrowRightIcon } from '@heroicons/vue/solid';
 import moment from 'moment';

 const props = defineProps({
    datum : Object,
 })

 const emits = defineEmits(["send"])

 const dtInterrupted = ref({})
 const dtRestored = ref({})


 
 const generateDateTimes = ()=> {
    const interrupted = moment(props.datum.interrupted.slice(0,-1))
 
    dtInterrupted.value = {
    complete_date: interrupted.format("MMMM D ,GGGG"),
    complete_time: interrupted.format("h:mm a"),
    year: interrupted.format("GGGG"),
    month: interrupted.format("MMMM"),
    day: interrupted.format("D"),
    hour: interrupted.format("h"),
    minute: interrupted.format("mm"),
    am_pm: interrupted.format("a"),
  }

  const restored = moment(props.datum.restored.slice(0,-1)) 
    dtRestored.value = {
    complete_date: restored.format("MMMM D ,GGGG"),
    complete_time: restored.format("h:mm a"),
    year: restored.format("GGGG"),
    month: restored.format("MMMM"),
    day: restored.format("D"),
    hour: restored.format("h"),
    minute: restored.format("mm"),
    am_pm: restored.format("a"),
  }
 }



 watch(()=>props.datum,(newVal,oldVal)=> {
    if(newVal !== oldVal){
        console.log(newVal)
        generateDateTimes()
        // emits("send",{dt:dt.value, kwh_used: newVal.consumed})
    }
    
 },{deep:true})


onMounted( () => {
    generateDateTimes()
    // emits("send",{dt:dt.value, kwh_used: props.datum.consumed})

})

</script>

