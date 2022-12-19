<template>
    <div class="">
        <button @click="open = true" 
            class="bg-primary text-white px-2 py-1 font-bold rounded-lg hover:bg-active"
        >scan
        </button>
        <teleport to='#invoice'>
            <div class="z-10 bg-white p-4 shadow-xl" v-if="open"
                :class="open?'fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2':''">
                <div class="flex justify-between">
                    <p class="font-bold">SCAN DEPOSIT SLIP</p>
                    <button @click="open = false"><i class="inline-block w-6 h-6 text-red-500"><XIcon/></i></button>
                </div>
                <WebCamUI :fullscreenState="false"  @photoTaken="snapshot" v-if="!photoURL"/>
                <div v-else>
                    <img  :src="photoURL" alt="">
                    <div class="flex justify-center">
                        <button class="z-50 text-white bg-primary px-2 py-1 rounded-xl m-2" @click="save">Save</button>
                        <button class="z-50 text-primary bg-white border-2 border-primary px-2 py-1 rounded-xl m-2" @click="clear">Again</button>
                    </div>
                </div>
            </div>
        </teleport>
    </div>
</template>
<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { WebCamUI } from 'vue-camera-lib';
import { XIcon } from '@heroicons/vue/solid';

const props = defineProps({
    invoice: Object
})

const emits = defineEmits(["done"])

const open = ref(false)


const blob = ref(null)
const photoURL = ref(null)

const clear = ()=> {
    blob.value = null
    photoURL.value = null
}
const snapshot = (data)=> {
    blob.value = data.blob
    photoURL.value = data.image_data_url
}

const save = async()=> {
    // console.log(photoURL.value)
    const fd = new FormData();
    fd.append("deposit_slip",blob.value,`proof#${props.invoice.invoice_no}.jpg`)
    const response = await axios.put(`save_snap/bank_deposit/${props.invoice.invoice_no}`,fd)
    if(response.status===200){
        open.value = false
        emits("done")
    }
}
</script>