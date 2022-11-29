<template>
    <div class="absolute top-2 right-2">
        <button @click="open = true"><i class="inline-block w-6 h-6 text-red-400 hover:text-red-500"><CogIcon /></i></button>
        <teleport to='body'>
            <div v-if="open">
            <div @click.self="open=false" class="bg-slate-800 bg-opacity-50 flex justify-center items-center absolute top-0 right-0 bottom-0 left-0">
            <div class="bg-white px-16 py-14 rounded-md text-center justify-center flex flex-col">
                <h1 class="text-xl mb-4 font-bold text-slate-500">Select new avatar</h1>
                
                <div for="drop-zone" v-if="url" 
                    @mouseover="hovered = true"
                    @mouseleave="hovered = false"
                    @click="$refs.file.click"
                    class="relative flex flex-wrap items-center justify-center rounded-2xl w-56 h-56 border-solid border-red-300 hover:border-red-500 border-x-2 border-y-2 my-2 overflow-hidden">
                    
                    <img :src="url" class="object-cover w-full h-full"/>
                    <button v-if="hovered" class="absolute font-sans text-lg font-black text-white bg-black bg-opacity-30 w-full h-full">UPLOAD</button>
                    <input id="drop-zone" type="file" ref="file" @change="uploadAndPreview()" accept="image/*" class="hidden" capture />
                
                </div>
                <button class="bg-red-500 px-7 py-2 ml-2 rounded-md text-md text-white font-semibold disabled:bg-red-300"
                        :disabled="!save"
                        @click="triggerChangePic()">
                        Save
                </button>
            </div>
            </div>
        </div>
        </teleport>
    </div>
</template>
<script setup>
    import { ref } from 'vue';
    import { CogIcon } from '@heroicons/vue/solid';
    import { userStore } from '@/stores/user';
    const userstore = userStore()
    
    const open = ref(false)
    const file = ref(null)
    const url = ref(null)
    const hovered = ref(false)
    const save = ref(false)
    const uploadAndPreview = async () => {
        save.value = true
        url.value = URL.createObjectURL(file.value.files[0])
    }

    const triggerChangePic = async ()=>{
        const upload_pic = await userstore.changePic(file.value.files[0])
        open.value = false
    }
    
   

    // set inital state
    setTimeout(() => {
        url.value = userstore.avatar
    }, 1000);
</script>

<style>
    @supports (-webkit-text-stroke: 1px black) {
        .stroked {
            -webkit-text-stroke: 0.7px rgb(226, 228, 84);
            -webkit-text-fill-color: white;
        }
    }
</style>
