<template>

    <nav class="flex flex-col justify-between w-52 z-50">
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


    </nav>
</template>

<script setup>;
import { ref, onMounted } from "vue";
import { RouterLink } from "vue-router";
import { userStore } from "@/stores/user";
import SidebarItem from "./SidebarItem.vue";
import { HashtagIcon } from "@heroicons/vue/outline";

const emits = defineEmits(["afterset"])

const selected = ref("")
const setSelected = (menu)=> {
    selected.value = menu
    emits("afterset")
    
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
        name: "Consumption",
        location: "/power"
    },
    {
        name: "Brown Out",
        location: "/power_outage"
    },
    {
        name: "Transmitter",
        location: "/transmitter"
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