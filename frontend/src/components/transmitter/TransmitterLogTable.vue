<template>
    <div class="bg-white shadow-xl p-2 rounded-md">
        <div class="font-bold">
            Date: 
            <input type="date" class="text-primary" v-model="date" @change="search">
        </div>
        <table class="w-full">
            <thead>
                <tr class="border-y-2">
                    <td colspan="3" class=""></td>
                    <td colspan="4" class="bg-sky-200 text-sky-500 text-center font-bold">Driver (PA)</td>
                    <td colspan="4" class="bg-orange-200 text-orange-500 text-center font-bold">Final</td>
                </tr>
                <tr class="text-xs font-bold w-full border-b-2">
                    <td class="border-x text-gray-700 text-left bg-green-200">HOUR</td>
                    <td class="border-x text-gray-700 text-right bg-green-200">LINE VAC</td>
                    <td class="border-x text-gray-700 text-right bg-green-200">EXT</td>
                    <td class="border-x text-gray-700 text-right bg-sky-200">V(PA)</td>
                    <td class="border-x text-gray-700 text-right bg-sky-200">I(PA)</td>
                    <td class="border-x text-gray-700 text-right bg-sky-200">FWD(PA)</td>
                    <td class="border-x text-gray-700 text-right bg-sky-200">RF(PA)</td>
                    <td class="border-x text-gray-700 text-right bg-orange-200">V(Final)</td>
                    <td class="border-x text-gray-700 text-right bg-orange-200">I(Final)</td>
                    <td class="border-x text-gray-700 text-right bg-orange-200">FWD(Final)</td>
                    <td class="border-x text-gray-700 text-right bg-orange-200">RF(Final)</td>
                    <td class="border-x text-gray-700 text-right bg-red-200">Author</td>
                    <td class="border-x text-gray-700 text-right bg-red-200">Remarks</td>
                </tr>
            </thead>
            <tbody>
                <tr class="text-sm w-full border-b hover:bg-gray-200" v-for="log in logs">
                    <td class="text-center border-x">
                        <p class="font-bold">{{log.hour}}H</p>
                        <p class="italic text-xs text-green-500 font-thin">{{log.time}}</p>
                        
                    </td>
                    <td class="text-right border-x">{{log.line_voltage}}</td>
                    <td class="text-right border-x">{{log.exciter}}</td>
                    <td class="text-right border-x">{{log.driver_voltage}}</td>
                    <td class="text-right border-x">{{log.driver_current}}</td>
                    <td class="text-right border-x">{{log.driver_forward}}</td>
                    <td class="text-right border-x">{{log.driver_rf}}</td>
                    <td class="text-right border-x">{{log.final_voltage}}</td>
                    <td class="text-right border-x">{{log.final_current}}</td>
                    <td class="text-right border-x">{{log.final_forward}}</td>
                    <td class="text-right border-x">{{log.final_rf}}</td>
                    <td class="text-right border-x">{{log.author}}</td>
                    <td class="text-right border-x relative">
                        <Remarks v-if="log.remarks"
                            :remarks="log.remarks"/>
                    </td>

                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import Remarks from '@/components/transmitter/Remarks.vue';
const props = defineProps({
    logs: Array,
    filter:String
})

const date = ref(props.filter)

const emits = defineEmits(["search"])
const search = ()=> {
    emits("search",date.value)
}


watch(()=>props.filter,(newVal,oldVal)=> {
    date.value = newVal
})


</script>