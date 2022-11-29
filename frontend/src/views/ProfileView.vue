<template>
    
    <div class="flex flex-col justify-between py-4 px-4 sm:px-6 lg:px-8 h-min">
        <div class="flex justify-center">
        <ProfileInfo />
        </div>

        <DTRLogs />

        
        <ProfileActivity />

        
    </div>
</template>


<script setup>
import { dtrStore } from '@/stores/dtr';
import ProfileInfo from "@/components/ProfileInfo.vue"
import DTRLogs from "@/components/DTRLogs.vue"
import ProfileActivity from "@/components/ProfileActivity.vue"

const dtrstore = dtrStore()
dtrstore.loadDTR()
</script>