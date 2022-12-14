<template>
    <!-- <a href="#" @click="go" class="text-primary rounded-md m-1 hover:bg-primary hover:text-white"> -->
    <div class="flex justify-between rounded-md m-1 px-1"
        :class="parentIsHovered || selected?'bg-primary':''"
        @mouseover="parentIsHovered = true" @mouseout="parentIsHovered = false">
        <i class="h-6 w-6 py-2" :class="parentIsHovered || selected?'text-white':'text-primary'">
            <slot name="icon"></slot>
        </i>
        <div class="justify-self-start text-middle py-2 font-bold w-28 flex justify-between">
            <p class="text-start" :class="parentIsHovered || selected?'text-white':'text-primary'">{{title}}</p>
            <div class="relative">
                <button @click="toggleOpen">
                    <i class="block h-6 w-6" :class="parentIsHovered || selected?'text-white':'text-primary'">
                        <ChevronRightIcon/>
                    </i>
                </button>
                <ul v-if="menuOpen && links.length" class="absolute top-1 left-8 bg-white shadow-md w-32">
                    <li v-for="link in links" class="hover:bg-primary hover:text-white text-primary text-sm font-normal px-2 border-b"
                        v-click-away="toggleOpen">
                        <button class="w-full text-left" @click="go(link.location)">{{link.name}}</button>
                    </li>
                    
                </ul>
            </div>
        </div>
    </div>
    <!-- </a> -->
</template>

<script setup>
import { ref,watch } from 'vue';
import router from '../router';
import { ChevronRightIcon } from '@heroicons/vue/solid';
    const props = defineProps({
        title: String,
        selected: Boolean,
        links: Array,
    })
    const emits = defineEmits(["select"])
    const menuOpen = ref(false)

    const toggleOpen = ()=> {
        if(menuOpen.value === true)menuOpen.value=false
        else menuOpen.value=true
    }
    const go = (location) => {
        router.push(location)
        menuOpen.value = false
        parentIsHovered.value = false
        emits("select",props.title)
    }

    const parentIsHovered = ref(false)

</script>