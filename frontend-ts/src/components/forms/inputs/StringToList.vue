<template>
  <div
    class="my-3 w-full text-right px-11"
    :class="end ? 'border-b mb-2 pb-3' : ''"
  >
    <label
      for="adTitle"
      class="text-white px-2 py-1 w-full rounded-l-md shadow-md text-sm mr-1"
      :class="value ? 'bg-primary text-white' : 'bg-secondary text-primary'"
      >{{ title }}:
    </label>
    <input
      type="text"
      v-model="value"
      class="bg-secondary focus-visible:outline-2 focus-within:outline-primary font-thin text-sm px-2 py-1 shadow-md rounded-r-md text-primary focus-within:bg-secondary"
      :placeholder="placeholder"
      @keyup="verify"
      @change="decide"
    />

    <div class="inline-block ml-1" v-if="value">
      <i class="inline-block w-4 h-4 text-primary" v-if="valid"
        ><CheckCircleIcon
      /></i>
      <i class="inline-block w-4 h-4 text-red-500" v-else><XCircleIcon /></i>
    </div>
    <div class="text-xs text-red-500 text-right mx-5" v-if="!valid">
      {{ error }}
    </div>
    <div class="grid grid-cols-4 p-6 my-2 bg-secondary" v-if="value">
      <div
        v-for="(i, index) in valueList"
        :key="index"
        class="bg-primary w-full shadow-sm border rounded-xl text-xs text-center text-white font-extralight py-1"
      >
        {{ i }}
      </div>
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
  unique: Boolean, //If enabled, you need to get database API to check for duplicates [must use queryURL]
  queryURL: String, //API URI -- search all data for duplicates //commonly ending with "/all"
  queryKey: String,
  querySecondary: String,
  end: Boolean, //End of the  batch. Has border at bottom
  placeholder: String,
  basedOn: Number, //For comparison
});
const emits = defineEmits(["done"]);
const error = ref("");

const value = ref(props.default);
const valid = ref(false);
const valueList = ref([]);

const pushToList = () => {
  if (value.value) {
    valueList.value = value.value.split(","); //(/[, ]+/)separate comma or space
    valueList.value = valueList.value.filter((word) => word.length > 0);
  }
};

const verify = async () => {
  pushToList();
  if (value.value && props.basedOn) {
    if (props.basedOn === valueList.value.length) {
      valid.value = true;
      error.value = "";
    } else {
      valid.value = false;
      error.value = `Put ${props.basedOn} items`;
    }
  } else valid.value = true;
};

const decide = async () => {
  await verify();
  emits("done", value.value);
};

watch(
  () => props.basedOn,
  async (newVal, oldVal) => {
    if (newVal !== oldVal) {
      await verify();
    }
  }
);
onMounted(async () => {
  if (value.value) await decide();
});

watch(
  () => props.default,
  (newDefault, old) => {
    value.value = newDefault;
    decide();
  }
);
</script>
