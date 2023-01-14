<template>
  <button
    class="text-red-500 font-thin bg-red-200 px-1 rounded-md text-xs"
    @click="open = true"
  >
    {{ open ? "..." : remarks.substring(0, 10) + "..." }}
  </button>
  <p
    class="bg-white shadow-xl border-2 rounded-md p-2 break-words border-red-200 w-52 h-max absolute right-1 text-left z-50"
    v-if="open"
    v-click-away="toggle"
  >
    {{ remarks }}
  </p>
</template>

<script setup>
import { ref } from "vue";

const open = ref(false);
const toggle = () => {
  if (open.value) open.value = false;
  else open.value = false;
};
const props = defineProps({
  remarks: String,
});
</script>
