<template>
  <div class="my-3 text-right px-11">
    <label
      class="text-white px-2 py-1 w-full rounded-l-md shadow-md text-sm mr-1"
      :class="
        uploaded.length ? 'bg-primary text-white' : 'bg-secondary text-primary'
      "
      >{{ title }}</label
    >
    <input
      type="file"
      ref="fileFieldInput"
      :accept="accepts"
      class="hidden"
      multiple
      @change="fileUpload"
    />
    <button
      class="bg-secondary focus-visible:outline-2 focus-within:outline-primary font-thin text-sm px-2 py-1 shadow-md rounded-r-md text-primary focus-within:bg-secondary border border-primary border-dashed"
      @click="$refs.fileFieldInput.click"
    >
      Upload
    </button>
    <div class="inline-block ml-1" v-if="uploaded.length">
      <i class="inline-block w-4 h-4 text-primary"><CheckCircleIcon /></i>
    </div>
    <ul class="text-xs text-primary text-right mx-1" v-if="uploaded.length">
      <li v-for="(f, index) in uploaded" :key="index">
        {{
          f.name.length > 25
            ? `${f.name.substring(0, 25)}...${f.name.substring(
                f.name.length - 3,
                f.name.length
              )}`
            : f.name
        }}
        <button @click="removeFromUploaded(audio, index)">
          <i
            class="inline-block align-middle w-6 h-6 text-red-500 hover:text-red-800"
          >
            <TrashIcon />
          </i>
        </button>
      </li>
    </ul>
    <ul class="w-full h-max bg-gray-100 p-10">
      <div class="flex" v-for="(audio, index) in existing" :key="index">
        <AudioItem :id="audio" :index="index" />
        <button @click="removeFromExistingFiles(audio, index)">
          <i
            class="inline-block align-middle w-6 h-6 text-red-500 hover:text-red-800"
          >
            <TrashIcon />
          </i>
        </button>
      </div>
    </ul>
    <div class="text-xs text-red-500 text-right mx-5">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { CheckCircleIcon, XCircleIcon, TrashIcon } from "@heroicons/vue/solid";
import CheckBox from "@/components/forms/inputs/CheckBox.vue";
import AudioItem from "@/components/AudioItem.vue";

const props = defineProps({
  default: Array,
  title: String,
  file: String,
  accepts: String, //for audio "audio/*"
});
const emits = defineEmits(["done"]);

const fileFieldInput = ref(null);
const uploaded = ref([]);
const existing = ref([...props.default])

const error = ref("")
const filesForRemoval = ref([])
const removeFromExistingFiles = (file, index) => {
  filesForRemoval.value.push(file)
  existing.value.splice(index, 1);
  emits("done", uploaded.value, existing.value, filesForRemoval.value);
};

const removeFromUploaded = (file, index) => {
  uploaded.value.splice(index, 1);
  emits("done", uploaded.value, existing.value, filesForRemoval.value);
};
const fileUpload = async () => {
  uploaded.value = [...uploaded.value, ...(await fileFieldInput.value.files)];
  emits("done", uploaded.value, existing.value, filesForRemoval.value);
};
</script>
