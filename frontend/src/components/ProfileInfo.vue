<template>
    <div class="max-w-md w-min justify-self-center space-y-8 bg-white b-border py-4 px-4 shadow-md rounded-2xl">
        <div class="relative flex flex-wrap items-center justify-center my-0 w-56 h-56 mx-auto overflow-hidden rounded-3xl border-solid border-red-300 border-x-2 border-y-2 shadow-md shadow-current">
            <img :src="getImage()" class="object-cover w-full h-full">
            <ProfileSettings />
            <!-- <button class="absolute top-2 right-2"><i class="inline-block w-6 h-6 text-red-400"><CogIcon /></i></button> -->
        </div>
        <div class="text-center my-0">
            <h1 class="font-extrabold text-lg">@{{userstore.user}}</h1><br>
        </div>
        <Infocard />
    </div>
</template>
<script setup>
    import { userStore } from '@/stores/user';
    import Infocard from "@/components/Infocard.vue"
    import ProfileSettings from "@/components/ProfileSettings.vue";
    // import avatar from "../assets/avatar.png"
    import { ref } from 'vue';
    

    const userstore = userStore()

  
    const getImage = () => {
        return userstore.avatar
    }

    
</script>