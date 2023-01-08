<template>
    <div class="relative m-5">
        <span class="absolute -bottom-7 text-xs bg-black px-2 py-1 z-20 shadow-xl text-white w-max bg-opacity-50"
                v-if="parentIsHovered">
            Add New Package
        </span>
        <button @click="open = true" @mouseover="parentIsHovered = true" @mouseout=" parentIsHovered = false"
                class="w-max rounded-md  flex items-center justify-start px-2 h-9 hover:shadow-md hover:bg-primary hover:text-white">
            <i class="h-6 w-6" :class="parentIsHovered ? 'text-white':'text-primary'"><PlusIcon/></i>
        </button>
    </div>
    <teleport to='body'>
        <div class="bg-slate-800 bg-opacity-50 flex justify-center items-center absolute top-0 right-0 bottom-0 left-0"
            v-if="open"
            ref="outer">

            <!-- start of inside modal -->
            <div class="w-auto h-3/4 bg-white p-5 overflow-y-auto none-scroll">
                <div class="w-full border-b mb-2">
                    <p class="font-bold text-xl text-primary">Create New Package</p>
                </div>
                <div class="my-2">
                    <p class="text-gray-500 text-sm">Name</p>
                    <input type="text" class="border shadow-md focus-within:outline-primary text-primary px-1 font-thin"
                        placeholder="Package #1" 
                        v-model="name">
                    <p class="text-xs italic text-disabled">Name of the package</p>
                </div>
                
                <div class="my-2">
                    <p class="text-gray-500 text-sm">Package Duration</p>
                    <div class="w-full flex gap-3">
                        <input type="number" class="w-12 border shadow-md focus-within:outline-primary text-primary px-1 font-thin"
                            @change="describe"
                            v-model="durationOfPricing">-
                        <select class="border shadow-md focus-within:outline-primary text-primary px-1 font-thin"
                            @change="describe"
                            v-model="pricing">
                            <option value="month">Months</option>
                            <option value="day">Days</option>
                        </select>
                    </div>
                    <p class="text-xs italic text-disabled">Ex: 3 months contract</p>
                </div>
                <div class="my-2">
                    <p class="text-gray-500 text-sm">Price</p>
                    <input type="number" class="border shadow-md focus-within:outline-primary text-primary px-1 font-thin"
                        placeholder="₱15,000"
                        @change="describe"
                        v-model="price">
                    <p class="text-xs italic text-disabled">Total package in ₱</p>
                </div>
                <div class="my-2">
                    <p class="text-gray-500 text-sm">Material Duration</p>
                    <input type="number" class="border shadow-md focus-within:outline-primary text-primary px-1 font-thin"
                        placeholder="30 seconds"
                        v-model="materialDuration">
                    <p class="text-xs italic text-disabled">in seconds</p>
                </div>
                <div class="my-2">
                    <p class="text-gray-500 text-sm">Spot</p>
                    <input type="number" class="border shadow-md focus-within:outline-primary text-primary px-1 font-thin"
                        placeholder="3 spots"
                        v-model="spotsPerDay">
                    <p class="text-xs italic text-disabled">per day</p>
                </div>
                <div class="my-2">
                    <p class="text-gray-500 text-sm">AOB</p>
                    <input type="number" class="border shadow-md focus-within:outline-primary text-primary px-1 font-thin"
                        placeholder="3 aobs"
                        v-model="aobPerDay">
                    <p class="text-xs italic text-disabled">per day</p>
                </div>
                <div class="my-2">
                    <p class="text-gray-500 text-sm">Time check</p>
                    <input type="number" class="border shadow-md focus-within:outline-primary text-primary px-1 font-thin"
                        placeholder="3 timchecks"
                        v-model="tcPerDay">
                    <p class="text-xs italic text-disabled">per day</p>
                </div>
                <div class="my-2">
                    <p class="text-gray-500 text-sm">Song sponsorships</p>
                    <input type="number" class="border shadow-md focus-within:outline-primary text-primary px-1 font-thin"
                        placeholder="3 song sponsorships"
                        v-model="ssPerDay">
                    <p class="text-xs italic text-disabled">per day</p>
                </div>
                <div class="my-2">
                    <p class="text-gray-500 text-sm">Description</p>
                    <textarea name="" id="" cols="25" rows="5" class="border shadow-md focus-within:outline-primary text-primary px-1 font-thin"
                        v-model="description">
                    </textarea>
   
                    <p class="text-xs italic text-disabled">Describe the package</p>
                </div>

                <div class="my-2 flex justify-around border-t w-full">
                    <button @click="open = false"
                        class=" bg-disabled text-white px-2 py-1 my-2 hover:bg-disabled">
                        Close
                    </button>
                    <button @click="savePackage"
                        class=" bg-primary text-white px-2 py-1 my-2 hover:bg-active">
                        Save
                    </button>
                    
                </div>
              
            </div>
            <!-- end of inside modal -->
        </div>
    </teleport>
</template>
<script setup>
    import { ref, onMounted, watch } from 'vue';
    import { ArrowsExpandIcon, GiftIcon, PlusIcon } from "@heroicons/vue/solid";
    import RectGroupIconOutline from "@/components/icons/RectGroupIconOutline.vue"
    import axios from 'axios';
    import { userStore } from "@/stores/user"

    const open = ref(false)
    const parentIsHovered = ref(false)
    const emits = defineEmits(["done"])

    const name = ref("")
    const durationOfPricing = ref(0)
    const pricing = ref("")
    const price = ref(0)
    const materialDuration = ref(0)
    const spotsPerDay = ref(0)
    const aobPerDay = ref(0)
    const tcPerDay = ref(0)
    const ssPerDay = ref(0)
    const description = ref("")

    const describe = ()=> {
        description.value = `${durationOfPricing.value} ${pricing.value+(durationOfPricing.value>1?'s':'')} contract. For ₱${price.value}.`
    }

    const savePackage = async()=> {
        const fd = new FormData()
        fd.append("name", name.value)
        fd.append("duration_of_pricing", durationOfPricing.value)
        fd.append("pricing", pricing.value)
        fd.append("price", price.value)
        fd.append("material_duration", materialDuration.value)
        fd.append("spots_per_day", spotsPerDay.value)
        fd.append("aob_per_day", aobPerDay.value)
        fd.append("tc_per_day", tcPerDay.value)
        fd.append("ss_per_day", ssPerDay.value)
        fd.append("description", description.value)
        fd.append("author", userStore().user)

        const response = await axios.post("add_package",fd)
        if(response.status === 200){
            name.value = ""
            durationOfPricing.value = 0
            pricing.value = ""
            price.value = 0
            materialDuration.value = 0
            spotsPerDay.value = 0
            aobPerDay.value = 0
            tcPerDay.value = 0
            ssPerDay.value = 0
            description.value = ""
            emits("done")
            open.value = false
        }
    }

</script>