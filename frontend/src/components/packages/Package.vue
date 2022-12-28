<template>

    <div class="bg-white w-52 h-full py-3 shadow-lg rounded-md">
        <div class="border-b mx-1">
            <p class="text-center font-bold">{{ pack.name.toUpperCase() }}</p>
        </div>
        <div class="mx-3 bg-sky-100 py-2 my-1">
            <p class="text-xs italic text-center">{{ pack.description }}</p>
        </div>
        <div class="mx-3 text-sm text-sky-500">
            <p><span class="font-thin text-gray-500">Rate:</span> {{ '₱' + pack.price }}</p>
            <p><span class="font-thin text-gray-500">Duration:</span> {{ pack.duration_of_pricing + ' ' + pack.pricing + (pack.duration_of_pricing >1?'s':'') }}</p>
            <p><span class="font-thin text-gray-500">Material:</span> {{ pack.material_duration + ' sec'}}</p>
            <p v-if="pack.spots_per_day"><span class="font-thin text-gray-500">Spots:</span> {{ pack.spots_per_day + ' per day'}}</p>
            <p v-if="pack.aob_per_day"><span class="font-thin text-gray-500">AOB:</span> {{ pack.aob_per_day + ' per day'}}</p>
            <p v-if="pack.tc_per_day"><span class="font-thin text-gray-500">TC:</span> {{ pack.tc_per_day + ' per day'}}</p>
            <p v-if="pack.ss_per_day"><span class="font-thin text-gray-500">SS:</span> {{ pack.ss_per_day + ' per day'}}</p>


        </div>
 
    </div>
</template>
<script setup>

const props = defineProps({
    pack:Object
})
</script>