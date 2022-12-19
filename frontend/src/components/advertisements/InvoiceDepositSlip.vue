<template>
    <div class="">
        <button @click="open = true" 
            class="text-white px-2 py-1 font-bold rounded-lg w-max h-max"
            
            :disabled="!invoice.deposited"
        ><i class="inline-block w-6 h-6 text-primary"><PhotographIcon/></i>
        </button>
        <teleport to='#invoice'>
            <div v-if="open" class="z-10 bg-black bg-opacity-40 w-full h-screen flex justify-center items-center absolute top-0"
                @click.self="open = false">
                <div class="bg-white p-4 shadow-xl w-96 h-auto">
                    <div class="w-full flex justify-between">
                        <p class="font-bold">INVOICE#{{invoice.invoice_no}}</p>
                        <button @click="open = false"><i class="inline-block w-6 h-6 text-red-500"><XIcon/></i></button>
                    </div>
                    <img :src="baseURL + invoice.deposit_slip" alt="" >
                </div>
            </div>
            
        </teleport>
    </div>
</template>
<script setup>
import { ref, watch } from 'vue';
import axios from 'axios';
import { XIcon, PhotographIcon } from '@heroicons/vue/solid';
const baseURL = axios.defaults.baseURL
const open = ref(false)
const props = defineProps({
    invoice: Object
})


watch(()=>props.invoice.deposit_slip,(newVal,oldVal)=> {
    console.log("Changed",newVal)
})
</script>