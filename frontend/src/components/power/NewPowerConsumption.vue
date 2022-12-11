<template>
    <div class="mx-auto my-3">
        <button @click="open = true" @mouseover="parentIsHovered = true" @mouseout=" parentIsHovered = false"
                class="w-max rounded-md hover:shadow-md flex items-center justify-start px-2 h-9 hover:bg-primary hover:text-white">
        <i class="h-6 w-6" :class="parentIsHovered ? 'text-white':'text-primary'"><LightningBoltIcon/></i>
        <h3 class="text-sm font-light">Log Meter Reading</h3>
        </button>
        <teleport to='body'>
            
            <div class="bg-slate-800 bg-opacity-50 flex justify-center items-center absolute top-0 right-0 bottom-0 left-0"
                v-if="open"
                ref="outer"
                @click.self="open = false">
            <div class="bg-white rounded-md text-start justify-start flex flex-col w-96">
                <div class="flex flex-col justify-center text-center py-4 w-full">
                    <h1 class="font-bold text-gray-500 text-xl">Log Electric Bill Reading</h1>
                    <hr class="my-4 w-full">
                </div>
                <div class="flex flex-col justify-center my-5 w-56 mx-auto mb-8">
                    <label class="text-primary font-semibold">🔢 Meter Reading:</label>
                    <input type="number" 
                        class="font-thin text-sm px-3 py-1 mt-2 rounded-md mb-5 text-gray-500"
                        :class="valid?'bg-secondary ':'bg-red-200 border-red-400'"
                        @keyup="validate()" @change="validate()"
                        v-model="meter">

                    <label class="text-primary font-semibold">📅 Reading Date:</label>
                    <input type="datetime-local" class="text-gray-500 font-thin bg-secondary text-sm px-3 py-1 mt-2 rounded-md mb-5"
                    v-model="datetime">
                </div>
                <hr>

                <div class="my-5 text-gray-500 text-center flex flex-col justify-center items-center">
                    <button class="border px-5 py-2 text-white my-5 font-bold text-lg"
                    :class="valid?'bg-primary':'bg-disabled'"
                    :disabled="!valid"
                    @click="submit">Submit</button>
                </div>
            </div>
            </div>
        </teleport>
    </div>
</template>
<script setup>
    import { LightningBoltIcon } from '@heroicons/vue/solid';
    import DTRTable from "@/components/DTRTable.vue"
    import { ref, onMounted } from "vue";
    import moment from 'moment';
    import axios from 'axios';
    import { userStore } from '@/stores/user';

    const meter = ref(0)
    const previousMeter = ref(0)
    const datetime = ref("")
    const open = ref(false)
    const parentIsHovered = ref(false)
    const outer = ref(null)
    const valid = ref(false)
    const emits = defineEmits(["done"])


    const submit = async () => {
        const fd = new FormData()
        fd.append("meter",meter.value)
        fd.append("datetime",datetime.value)
        const response = await axios.post("new_power_reading", fd)
        console.log(response)
        open.value = false
        emits("done")
    }
    const getLatestMeter = async ()=> {
        const response = await axios.get("get_power_readings")
        meter.value = response.data[0].meter
        previousMeter.value = response.data[0].meter
    }
    const validate = ()=> {
        if(previousMeter.value > meter.value) valid.value = false
        else valid.value = true
        
    }

    onMounted(() => {
        getLatestMeter()
        validate()
    })
 
</script>
