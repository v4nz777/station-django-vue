<template>

    <div v-if="clicked" class="rounded-full h-11 w-11 mx-auto flex items-center justify-center overflow-hidden
                            bg-emerald-300">
        <div class="w-6 h-6 border-white border-4 mx-auto my-auto rounded-full" id="loader">
        </div>
    </div>
    <div v-else class="rounded-full h-11 w-11 mx-auto flex items-center justify-center overflow-hidden">
        <button class="text-center align-middle font-black text-gray-500 w-full h-full"
            :class="batch.y.version === current?'bg-emerald-300 shadow-md':'bg-gray-300'"
            :disabled="batch.y.version === current"
            @mouseover="hovered = true"
            v-if="!hovered">
            {{batch.y.version}}
        </button>
        <button class="flex items-center justify-center text-emerald-500 w-full h-full"
            :class="batch.y.version === current?'bg-emerald-500 shadow-md':'bg-gray-300'"
            :disabled="batch.y.version === current"
            @mouseleave="hovered = false"
            @click="changeVersion()"
            v-else>
            <i class="block h-6 w-6"><PlayIcon/></i>
        </button>
    </div>
</template>
<script setup>
import { ref } from 'vue';
import { PlayIcon } from '@heroicons/vue/solid';
import axios from "axios";
    const props = defineProps({
        batch: Object,
        current: Number,
        contract: String,
    })
    const emits = defineEmits(["selected"])

    const hovered = ref(false)
    const clicked = ref(false)

    const changeVersion = () => {
        clicked.value = true
        setTimeout(async () => {
            
            const fd = new FormData()
            fd.append("contract", props.contract)
            fd.append("new_version", props.batch.y.version)
            const response = await axios.put("change_version", fd)
            emits("selected")
            console.log(response.data)
            clicked.value = false
         }, 2000);
    }


</script>