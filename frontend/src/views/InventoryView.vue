<template>
    <div class="flex flex-col w-inventory-controls px-5 items-center">
        <div class="w-full h-max bg-white rounded-3xl my-5 px-5 py-2 shadow-md flex">
            <NewInventory onMain/>
            <NewGroup
                :items="batch"
                @done="batch=[]"/>
            <MoveInventory
                :items="batch"
                @done="batch=[]"/>
            <StatusInventory
                :items="batch"
                @done="batch=[]"/>
            <DeleteInventory
                :items="batch"
                @done="batch=[]"/>

            
        </div>

        <div class="w-inventory">
            <div v-if="loading" class="flex justify-center items-center">
                <div class="w-9 h-9 border-4 border-x-emerald-500 border-y-emerald-200 rounded-full animate-spin"></div>
            </div>
            <div v-else class="w-full">
                <EquipmentGroup  v-if="groups.length"
                    v-for="group in groups" :group="group"
                    :batched-items="batch"
                    @batched="addSomeInBatch"
                    @unbatched="deleteSomeInBatch"/>
                <div v-else class="">
                    <p>
                        No groups created yet!
                    </p>
                </div>
            </div>
        </div>
    </div>
    

</template>

<script setup>
    import NewGroup from "@/components/inventory/NewGroup.vue"
    import NewInventory from "@/components/inventory/NewInventory.vue"
    import DeleteInventory from "@/components/inventory/DeleteInventory.vue"
    import MoveInventory from "@/components/inventory/MoveInventory.vue"
    import StatusInventory from "@/components/inventory/StatusInventory.vue"





    import { ref, onMounted, onUnmounted } from "vue";
    import axios from "axios";
    import EquipmentGroup from "@/components/inventory/EquipmentGroup.vue";

    const batch = ref([])

    const addSomeInBatch = (item)=> {
        if(batch.value.includes(item)){
            console.log("nothing to add!")
        }else batch.value.push(item)
        
    }
    const deleteSomeInBatch = (item)=> {
        if(batch.value.includes(item)){
            const index = batch.value.indexOf(item)
            batch.value.splice(index,1)
        }else console.log("nothing to remove!")
    }




    const groups = ref([])
    const loading = ref(true)
    const getGroups = async ()=> {
        const response = await axios.get("equipment_groups/all")
        groups.value = response.data
        loading.value = false
    }
    const autoUpdateGroups = setInterval(async() => await getGroups(), 1000)

    onMounted(async () => {
        autoUpdateGroups
    })
    onUnmounted(()=> {
        clearInterval(autoUpdateGroups)
    })

    
</script>
<style>
.grid-auto-cols {
    display: grid;
    grid-gap: 1rem;
    grid-template-columns: repeat(auto-fit, minmax(128px, 1fr));
    /* grid-template-rows: repeat(auto-fit, 208px); */
}

.w-inventory {
    width: 40rem;
}
.w-inventory-controls {
    width: 45rem;
}
</style>

