<template>
  <div class="my-3 w-96 text-right px-11">
    <label
      class="text-white px-2 py-1 w-full rounded-l-md shadow-md text-sm mr-1"
      :class="value ? 'bg-primary text-white' : 'bg-secondary text-primary'"
      >{{ title }}:
    </label>
    <div class="inline-block">
      <select
        v-model="value"
        class="bg-secondary focus-visible:outline-2 focus-within:outline-primary font-thin text-sm px-2 py-1 shadow-md rounded-r-md text-primary focus-within:bg-secondary"
        @change="setVal"
      >
        <option
          v-for="(offl, index) in offlineOptions"
          :key="index"
          :value="offl"
        >
          {{ offl }}
        </option>
        <option
          v-for="(onl, index) in onlineOptions"
          :key="index"
          :value="onl[onlineKey]"
        >
          {{ onl[onlineKey] }}
        </option>
      </select>
    </div>
    <div class="inline-block ml-1" v-if="value">
      <i class="inline-block w-4 h-4 text-primary"><CheckCircleIcon /></i>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { CheckCircleIcon, XCircleIcon } from "@heroicons/vue/solid";

const props = defineProps({
  default: String,
  title: String,
  offlineOptions: Array,
  onlineURL: String,
  onlineFilter: String,
  onlineKey: String,
});

const emits = defineEmits(["done"]);

const value = ref(props.default);

const onlineOptions = ref([]);

const getOnlineList = async () => {
  if (props.onlineURL) {
    const response = await axios.get(props.onlineURL + props.onlineFilter);
    return (onlineOptions.value = response.data);
  }
};
const setVal = () => {
  emits("done", value.value);
  console.log(value.value);
};

onMounted(async () => {
  await getOnlineList();
});
</script>
