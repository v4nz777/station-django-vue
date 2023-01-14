<template>
  <div
    class="my-3 w-full text-right px-11"
    :class="end ? 'border-b mb-2 pb-3' : ''"
  >
    <div class="inline-block relative">
      <label
        class="text-white px-2 py-1 w-full rounded-l-md shadow-md text-sm mr-1"
        :class="value ? 'bg-primary text-white' : 'bg-secondary text-primary'"
        >{{ title }}:
      </label>
      <input
        type="text"
        v-model="value"
        class="bg-secondary focus-visible:outline-2 focus-within:outline-primary font-thin text-sm px-2 py-1 shadow-md rounded-r-md text-primary focus-within:bg-secondary"
        list="advertiserlist"
        v-click-away="emptyList"
        @click="getList"
        @keyup="createFilter"
        @change="select(value)"
      />

      <ul
        class="bg-white absolute w-full h-max shadow-lg"
        v-if="searchList.length"
      >
        <li
          v-for="item in searchList"
          :key="item.id"
          class="text-sm text-left font-light hover:text-white hover:bg-primary w-full p-1 z-50 cursor-pointer"
          @click="select(item.name)"
        >
          <p class="font-bold text-sky-500">{{ item.name.toUpperCase() }}</p>
          <p class="text-xs italic">{{ item.description }}</p>
        </li>
      </ul>
    </div>
    <div class="inline-block ml-1" v-if="value">
      <i class="inline-block w-4 h-4 text-primary"><CheckCircleIcon /></i>
    </div>
    <div class="text-xs text-red-500 text-left mx-5" v-if="error">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue";
import axios from "axios";
import { CheckCircleIcon, XCircleIcon } from "@heroicons/vue/solid";

const props = defineProps({
  default: String,
  title: String,
  searchURL: String, //include tailing slash eg. "url/"
  searchFilter: String, //use "all" as default
  end: Boolean, //End of the  batch. Has border at bottom
});
const emits = defineEmits(["done"]);
const value = ref(props.default);
const searchList = ref([]);
const filter = ref(props.searchFilter);
const chosen = ref(false);
const error = ref("");

const emptyList = () => (searchList.value = []);
chosen.value = false;
const getList = async () => {
  const response = await axios.get(props.searchURL + filter.value);
  searchList.value = [...response.data];
};
const select = (selected) => {
  value.value = selected;
  emits("done", value.value);
  chosen.value = true;
};
const createFilter = async () => {
  if (value.value === "" || value.value === null) emptyList();
  else filter.value = value.value;
  await getList();
};

watch(
  () => props.default,
  (newVal, old) => {
    select(newVal);
  }
);
</script>
