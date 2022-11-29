<template>
    <div class="mx-auto my-3">
        <button @click="open = true"
                class="bg-white w-full border-b rounded-3xl shadow-md flex items-center justify-start p-3 h-9 hover:bg-red-500 hover:text-white">
        <h3 class="text-sm font-light">🍹Daily Time Records</h3>
        </button>
        <teleport to='body'>

            <div class="bg-slate-800 bg-opacity-50 flex justify-center items-center absolute top-0 right-0 bottom-0 left-0"
                v-if="open"
                @click.self="open = false">
            <!-- <div class="bg-white px-16 py-14 rounded-md text-center justify-center flex flex-col"> -->
                <DTRTable />
            <!-- </div> -->
            </div>
        </teleport>
    </div>
</template>
<script setup>
    import { NewspaperIcon } from '@heroicons/vue/outline';
    import DTRTable from "@/components/DTRTable.vue"
    import { ref } from "vue";

    const open = ref(false)
</script>