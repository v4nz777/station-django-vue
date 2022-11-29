<template>

    <div class="flex bg-white rounded-2xl b-border shadow-md justify-center items-center px-2 h-9"
                v-if="userstore.dtrIsLogged">
        <h2 class="justify-self-start py-2">⏱️<span class="text-red-500 text-sm font-normal">{{dtrstore.formatLogTimer}}</span></h2>
    </div>
</template>

<script setup>
import { dtrStore } from '@/stores/dtr';
import { userStore } from '@/stores/user';
import { onMounted } from 'vue';
const userstore = userStore()
const dtrstore = dtrStore()

onMounted( ()=> {
    dtrstore.watchTimer()
})


</script>