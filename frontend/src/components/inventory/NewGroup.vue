<template>
    <div class="relative">
        <span class="absolute -bottom-7 text-xs bg-black px-2 py-1 z-20 shadow-xl text-white w-max bg-opacity-50"
                v-if="parentIsHovered">
            Create new group
        </span>
        <button @click="open = true" @mouseover="parentIsHovered = true" @mouseout=" parentIsHovered = false"
                class="w-max rounded-md  flex items-center justify-start px-2 h-9 hover:shadow-md hover:bg-emerald-500 hover:text-white">
            <i class="h-6 w-6" :class="parentIsHovered ? 'text-white':'text-emerald-500'"><RectGroupIconOutline/></i>
        </button>
    </div>
    <teleport to='body'>
        <div class="bg-slate-800 bg-opacity-50 flex justify-center items-center absolute top-0 right-0 bottom-0 left-0"
            v-if="open"
            ref="outer"
            @click.self="open = false">

            <!-- start of inside modal -->
            <div id="inventory-scroll" class="w-inventory-add h-52 bg-white overflow-y-scroll pb-8 flex flex-col items-center justify-between">
                <p class="m-3 font-bold">
                    ADD NEW GROUP
                </p>
                    
                <div class="px-6 my-3">
         
                        <div class="w-64 relative">
                            <input type="text" v-model="groupQuery"
                            placeholder="Enter a new group name!"
                            class="bg-emerald-100 w-full p-1 text-sm shadow"
                            :class="taken?'focus-within:outline-red-500 text-red-500':'focus-within:outline-emerald-500 text-emerald-500'"
                            @keyup="checkGroup()">
                        </div>
                        
                    </div>
                

                
                <button @click="createGroup()" class="font-bold text-white px-4"
                        :class="taken||!groupQuery?'bg-gray-400':'bg-emerald-500'"
                        :disabled="taken||!groupQuery">
                    CREATE
                </button>
            </div>
            <!-- end of inside modal -->
        </div>
    </teleport>
</template>

<script setup>
    import { ref, onMounted, watch } from 'vue';
    import { ArrowsExpandIcon } from "@heroicons/vue/solid";
    import RectGroupIconOutline from "@/components/icons/RectGroupIconOutline.vue"
    import axios from 'axios';
    import { userStore } from "@/stores/user"

    const props = defineProps({
        items:Array
    })
    const emits = defineEmits(["done"])
    const groupQuery = ref("")
    const taken = ref(false)
 
    const open = ref(false)

    const parentIsHovered = ref(false)
    const createGroup = async ()=> {
        const fd = new FormData()
        fd.append("new_group",groupQuery.value)
   
        const response = await axios.post("new_group",fd)
        if(response.status === 200){
            emits("done")
            open.value = false
        }
    }

    const checkGroup = async ()=> {
        if(groupQuery.value){
            const response = await axios.get(`check_group/${groupQuery.value}`)
            taken.value = response.data.taken
        } 
    }


</script>
<style>
    .w-inventory-add {
            width: 25rem;
    }
    #inventory-scroll::-webkit-scrollbar {
        width: 4px;
        cursor: pointer;
        /*background-color: rgba(229, 231, 235, var(--bg-opacity));*/

    }
    #inventory-scroll::-webkit-scrollbar-track {
        /* background-color: rgba(229, 231, 235, var(--bg-opacity)); */
        cursor: pointer;
        background: #a0a1c0;
    }
    #inventory-scroll::-webkit-scrollbar-thumb {
        cursor: pointer;
        background-color: rgb(39, 112, 51);
        /*outline: 1px solid slategrey;*/
    }
</style>
