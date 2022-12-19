<template>
    <div class="flex flex-col w-full px-5 items-center">
        <div class="md:w-full w-screen h-max bg-white rounded-3xl my-5 px-5 py-2 shadow-md ">
            <NewAds buttonTitle="Add New"/>
        </div>
        <div v-if="loaded" class="md:w-full w-screen">
            <div class="m-5 mb-10 pb-10 h-max gap-4 grid-auto-cols"
                :class="adsList.length < 4 ? 'w-max': 'w-full'">
                    <div v-if="adsList.length"
                        v-for="i in adsList">
                        <Ad :ad="i" :adscount="adsList.length"/>
                    </div>
                    <div v-else>
                        <p class="text-center font-bold">No advertisement yet!</p>
                    </div>
            </div>
        </div>
        <div v-else class="w-full h-screen flex flex-col justify-center items-center">
                <div class="w-12 h-12 mx-auto border-4 border-primary rounded-full" id="loader"></div>
        </div>
    </div>
</template>
<script setup>
    import axios from 'axios';
    import { ref, onMounted,onUnmounted } from 'vue';
    import Ad from "@/components/advertisements/Ad.vue"
    import { dtrStore } from '@/stores/dtr';
    import NewAds from '@/components/advertisements/NewAds.vue';
    const filter = ref("all")
    const adsList = ref([])
    const loaded = ref(false)
    const dtrstore =  dtrStore()


    const getAds = async (_filter)=> {
        const currentcount = adsList.value.length
        const response = await axios.get(`ads/${_filter}`)
  
        if (currentcount !== response.data.length){
            loaded.value = false
            adsList.value = []
            console.log('triggered')
        }
        adsList.value = response.data
        loaded.value = true
    }

    const watchAds = setInterval(() => {
            getAds(filter.value)
        }, 3000);
    onMounted(()=>{
        dtrstore.loadDTR()
        watchAds
    })
    onUnmounted(() => {
        clearInterval(watchAds)
    })
</script>

<style>
    .grid-auto-cols {
        display: grid;
        grid-gap: 1rem;
        grid-template-columns: repeat(auto-fit, minmax(208px, 1fr));
        /* grid-template-rows: repeat(auto-fit, 208px); */
    }
    .w-ads {
        width: 40rem;
    }
    .w-ads-controls {
        width: 45rem;
    }
</style>