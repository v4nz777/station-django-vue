<template>
  <div class="relative">
    <span
      class="absolute -bottom-7 text-xs bg-black px-2 py-1 z-20 shadow-xl text-white w-max bg-opacity-50"
      v-if="parentIsHovered"
    >
      Move to new group
    </span>
    <button
      @click="open = true"
      @mouseover="parentIsHovered = true"
      @mouseout="parentIsHovered = false"
      :disabled="!items.length"
      :class="
        items.length ? 'hover:shadow-md hover:bg-sky-500 hover:text-white' : ''
      "
      class="w-max rounded-md flex items-center justify-start px-2 h-9"
    >
      <i v-if="!items.length" class="h-6 w-6 text-gray-500"
        ><ArrowsExpandIcon
      /></i>
      <i
        v-else
        class="h-6 w-6"
        :class="parentIsHovered ? 'text-white' : 'text-sky-500'"
        ><ArrowsExpandIcon
      /></i>

      <span v-if="items.length">{{ items.length }}</span>
    </button>
  </div>
  <teleport to="body">
    <div
      class="bg-slate-800 bg-opacity-50 flex justify-center items-center absolute top-0 right-0 bottom-0 left-0"
      v-if="open"
      ref="outer"
      @click.self="open = false"
    >
      <!-- start of inside modal -->
      <div
        id="inventory-scroll"
        class="w-inventory-add h-96 bg-white overflow-y-scroll pb-8 flex flex-col items-center justify-between"
      >
        <p class="m-3 font-bold">
          Are you sure you want to move
          {{ itemsReactive.length > 1 ? "these items" : "this item" }}?
        </p>
        <ul class="text-start">
          <li v-for="item in itemsReactive" :key="item.id">
            🟦{{ item.name }}
          </li>
        </ul>
        <div class="flex mt-5 justify-between w-full px-28">
          <p>Move to:</p>
          <select v-model="group" class="border">
            <option v-for="g in groups" :value="g.id" :key="g.id">
              <p class="font-bold">
                {{ g.group_name ? g.group_name : "ungrouped" }}
              </p>
            </option>
          </select>
        </div>

        <button
          @click="moveToGroup()"
          class="font-bold text-white px-4"
          :class="!group ? 'bg-disabled' : 'bg-primary'"
          :disabled="!group"
        >
          CONFIRM
        </button>
      </div>
      <!-- end of inside modal -->
    </div>
  </teleport>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { ArrowsExpandIcon } from "@heroicons/vue/solid";
import axios from "axios";
import { userStore } from "@/stores/user";

const props = defineProps({
  items: Array,
});
const emits = defineEmits(["done"]);
const groups = ref([]);
const group = ref(null);
const itemsReactive = ref([]);
const userstore = userStore();

const open = ref(false);

const parentIsHovered = ref(false);
const moveToGroup = async () => {
  const fd = new FormData();
  props.items.forEach((eq) => {
    fd.append("equipments", eq);
  });
  const response = await axios.put(`group_to/${group.value}`, fd);
  if (response.status === 200) {
    emits("done");
    open.value = false;
  }
};

const getGroups = async () => {
  const response = await axios.get("equipment_groups/all");
  groups.value = response.data;
};

const getItem = async (id) => {
  const response = await axios.get(`equipment/${id}`);
  return response.data;
};

const getItems = async () => {
  props.items.forEach(async (itemID) => {
    const gotten = await getItem(itemID);
    itemsReactive.value.push(gotten);
  });
};

watch(
  () => open.value,
  async (newVal, oldVal) => {
    if (newVal) {
      await getItems();
      await getGroups();
    } else itemsReactive.value = [];
  }
);
</script>
<style>
.w-inventory-add {
  width: 25rem;
}
#inventory-scroll::-webkit-scrollbar {
  width: 4px;
  cursor: pointer;
  /*background-color: rgba(229, 231, 235, var(--bg-opacity));*/
}
#inventory-scroll::-webkit-scrollbar-track {
  /* background-color: rgba(229, 231, 235, var(--bg-opacity)); */
  cursor: pointer;
  background: #a0a1c0;
}
#inventory-scroll::-webkit-scrollbar-thumb {
  cursor: pointer;
  background-color: rgb(39, 112, 51);
  /*outline: 1px solid slategrey;*/
}
</style>
