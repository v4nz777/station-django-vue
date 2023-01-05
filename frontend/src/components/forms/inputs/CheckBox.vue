<template>
    <div class="my-3 w-96 text-right px-11">
        <label class="text-primary px-2 py-1 w-full text-sm mr-1">{{title}}</label>
        <input :disabled="disabled"
            @change="change"
            type="checkbox" v-model="value" class="w-4 h-4 border-primary align-bottom">
    </div>
</template>
<script setup>
    import { ref, watch } from 'vue';
    const props = defineProps({
        default:Boolean,
        title:String,
        disabled:Boolean
    })
    const emits = defineEmits(["done"])
    const value = ref(props.default)
    const change = ()=> {
        emits("done",value.value)
    }

    watch(()=>props.default,(newDefault,old)=> {
        value.value=newDefault
        change()
    })
</script>