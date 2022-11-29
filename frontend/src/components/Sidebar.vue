<template>

    <nav class="flex flex-col justify-between w-52">
        <div class="flex flex-col py-4">
            <SidebarItem title="General" :links=general
                @select="setSelected" :selected="selected === 'General'">
                <template #icon><HashtagIcon/></template>
            </SidebarItem>

            <SidebarItem title="Traffic" :links=traffic
                @select="setSelected" :selected="selected === 'Traffic'">
                <template #icon><HashtagIcon/></template>
            </SidebarItem>

            <SidebarItem title="Technical" :links=technical
                @select="setSelected" :selected="selected === 'Technical'">
                <template #icon><HashtagIcon/></template>
            </SidebarItem>

        </div>

        <!-- <div class="flex flex-col pb-12 m-4">
            <RouterLink v-if="userstore.user" to="/profile/">
                <div class="m-1 rounded-full overflow-hidden mx-auto
                            h-9 w-9 flex justify-center items-center
                            border-solid border-yellow-500 border-x-2 border-y-2
                            shadow-sm shadow-black">
                    <img :src="userstore.avatar" class="w-full">
                </div>
            </RouterLink>
        </div> -->
        <!-- <div class="flex flex-col py-6 mb-20 justify-center bg-white shadow-md rounded-lg ml-2">
            <RouterLink v-if="userstore.user" to="/profile/">
                <div class="flex flex-col justify-center items-center">
                    <div class="m-1 rounded-full overflow-hidden
                                h-9 w-9 flex justify-center items-center
                                border-solid border-yellow-500 border-x-2 border-y-2 shadow-sm shadow-black">
                        <img :src="userstore.avatar" class="object-cover w-full h-full">
                    </div>
                    <span class="text-gray-900 text-sm font-light">{{userstore.userDetails.first_name}} {{userstore.userDetails.last_name}}</span>
                </div>
            </RouterLink>

            <hr class="my-5">
            <DTRTimer class="mx-4"/>
        </div> -->
    </nav>
</template>

<script setup>;
import { ref, onMounted } from "vue";
import { RouterLink } from "vue-router";
import { userStore } from "@/stores/user";
import SidebarItem from "./SidebarItem.vue";
import { HashtagIcon } from "@heroicons/vue/outline";
import MegaphoneIconOutline from "@/components/icons/MegaphoneIconOutline.vue"
import DTRTimer from "@/components/DTRTimer.vue";

const selected = ref("")
const setSelected = (menu)=> {
    selected.value = menu
}
const userstore = userStore()
const general = [
    {
        name: "Activities",
        location: "/"
    }
]
const traffic = [
    {
        name: "Ads",
        location: "/ads"
    }
]
const technical = [
    {
        name: "Inventory",
        location: "/inventory"
    },
    {
        name: "Power",
        location: "/power"
    }
]

const extractPropArray = (objArray) => {
    return objArray.map(prop => prop.location);
}

onMounted(() => {
    const generalLocations = extractPropArray(general)
    const trafficLocations = extractPropArray(traffic)
    const technicalLocations = extractPropArray(technical)

    if(generalLocations.includes(location.pathname)) selected.value = "General"
    else if(trafficLocations.includes(location.pathname)) selected.value = "Traffic"
    else if(technicalLocations.includes(location.pathname)) selected.value = "Technical"

   
  
    
})

</script>