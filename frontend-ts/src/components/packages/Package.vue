<template>
  <div class="bg-white w-52 h-full pb-3 shadow-lg rounded-md">
    <div
      class="border-b w-full relative py-1"
      :id="'pkgTheme' + pack.id"
      :class="theme ? theme : 'bg-primary'"
    >
      <p class="text-center font-bold text-white">
        {{ pack.name.toUpperCase() }}
      </p>
      <i
        class="w-4 h-4 cursor-pointer absolute top-0 right-0 text-white"
        @click="menu ? (menu = false) : (menu = true)"
        ><DotsVerticalIcon />
      </i>
      <div class="absolute top-4 right-0 w-24 z-50" v-if="menu">
        <p
          class="w-full shadow-lg hover:bg-primary bg-white hover:text-white text-primary cursor-pointer text-sm"
          @click="
            changeColorView = true;
            menu = false;
          "
        >
          Change Theme
        </p>
        <p
          class="w-full shadow-lg hover:bg-primary bg-white hover:text-white text-primary cursor-pointer text-sm"
          @click="deletePKG"
        >
          Delete
        </p>
      </div>
    </div>
    <div class="h-full relative">
      <div class="mx-3 bg-sky-100 py-2 my-1">
        <p class="text-xs italic text-center">{{ pack.description }}</p>
      </div>
      <div class="mx-3 text-sm text-sky-500">
        <p>
          <span class="font-thin text-gray-500">Rate:</span>
          {{ "₱" + pack.price }}
        </p>
        <p>
          <span class="font-thin text-gray-500">Duration:</span>
          {{
            pack.duration_of_pricing +
            " " +
            pack.pricing +
            (pack.duration_of_pricing > 1 ? "s" : "")
          }}
        </p>
        <p>
          <span class="font-thin text-gray-500">Material:</span>
          {{ pack.material_duration + " sec" }}
        </p>
        <p v-if="pack.spots_per_day">
          <span class="font-thin text-gray-500">Spots:</span>
          {{ pack.spots_per_day + " per day" }}
        </p>
        <p v-if="pack.aob_per_day">
          <span class="font-thin text-gray-500">AOB:</span>
          {{ pack.aob_per_day + " per day" }}
        </p>
        <p v-if="pack.tc_per_day">
          <span class="font-thin text-gray-500">TC:</span>
          {{ pack.tc_per_day + " per day" }}
        </p>
        <p v-if="pack.ss_per_day">
          <span class="font-thin text-gray-500">SS:</span>
          {{ pack.ss_per_day + " per day" }}
        </p>
      </div>
      <div
        v-if="changeColorView"
        class="absolute bg-white w-full h-full z-30 top-0 flex flex-col justify-between items-center p-5"
      >
        <div
          :id="'pkgThemePreview' + pack.id"
          class="p-5 border my-2 border-primary"
          :class="theme ? '' : 'bg-primary'"
        >
          <p class="font-bold text-primary">Pick a color:</p>
          <input type="color" v-model="theme" @input="changeThemeColor" />
        </div>
        <div class="flex justify-around w-full">
          <button
            @click="save"
            class="bg-primary font-bold text-white px-2 shadow-lg rounded-lg text-sm"
          >
            SAVE
          </button>
          <button
            @click="changeColorView = false"
            class="bg-disabled font-bold text-white px-2 shadow-lg rounded-lg text-sm"
          >
            DONE
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { DotsVerticalIcon } from "@heroicons/vue/solid";
const props = defineProps({
  pack: Object,
});
const emits = defineEmits(["modified"]);
const menu = ref(false);
const changeColorView = ref(false);
const theme = ref(props.pack.theme);
const changeThemeColor = () => {
  const titleBG = document.querySelector(`#pkgTheme${props.pack.id}`);
  const previewBG = document.querySelector(`#pkgThemePreview${props.pack.id}`);
  if (titleBG) titleBG.style.backgroundColor = theme.value;
  if (previewBG) previewBG.style.backgroundColor = theme.value;
};
const save = async () => {
  const fd = new FormData();
  fd.append("color", theme.value);
  const response = await axios.put(`change_pkg_color/${props.pack.id}`, fd);
  emits("modified", response.data);
  changeColorView.value = false;
};
const deletePKG = async () => {
  if (props.pack.ads.length)
    alert(`Used in ${props.pack.ads.length} ads, You cannot delete this`);
  else {
    const response = await axios.delete(`delete_pkg/${props.pack.id}`);
    emits("modified", response.data);
  }
  menu.value = false;
};
onMounted(() => {
  changeThemeColor();
});
</script>
