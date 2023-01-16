<template>
    <div class="flex flex-col items-center md:w-full w-screen">
        <div class="bg-white w-3/4 h-max shadow-lg rounded-md my-3">
            <NewPackage @done="loadPacks()"/>
        </div>
        <div class="grid-auto-cols my-5 w-3/4 place-items-center">
            <Package v-for="pkg in packages"
                @modified="loadPacks()"
                :pack="pkg" />
        </div>
    </div>
</template>

<script setup>
    import Package from '@/components/packages/Package.vue';
    import NewPackage from "@/components/packages/NewPackage.vue";
    import axios from 'axios';
    import { ref, onMounted } from 'vue';


    const packages = ref([])
    const filter = ref("all")

    const loadPacks = async ()=> {
        const response = await axios.get(`load_packages/${filter.value}`)
        packages.value = [...response.data]
    }

    onMounted(async () => {
       await loadPacks()
    })
</script>

<style>
.grid-auto-cols-52 {
        display: grid;
        grid-gap: 1rem;
        grid-template-columns: repeat(auto-fit, minmax(208px, 1fr));
        /* grid-template-rows: repeat(auto-fit, 208px); */
    }
</style>