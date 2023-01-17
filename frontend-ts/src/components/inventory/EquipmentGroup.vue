<template>
  <div class="bg-white md:w-full w-screen my-2 mb-5">
    <div class="w-full border-b flex bg-gray-50 justify-between px-2 shadow-lg">
      <div class="flex py-1 items-center">
        <input
          type="checkbox"
          class="accent-primary mx-1"
          v-model="all"
          @change="selectAll()"
        />
        <p class="font-bold text-primary">
          {{
            group.group_name === ""
              ? "UNGROUPED"
              : group.group_name.toUpperCase()
          }}
        </p>
        <NewInventory :preGroup="group.group_name" />
      </div>
      <div class="w-9 flex flex-col items-center">
        <span class="bg-primary text-white px-1 mt-1 rounded relative">
          <span
            v-if="notifOn"
            class="w-2 h-2 bg-red-500 rounded-full absolute c-top-right-n3 animate-ping"
          ></span>
          <span
            v-if="notifOn"
            class="w-2 h-2 bg-red-500 rounded-full absolute c-top-right-n3"
          ></span>
          {{ group.equipments.length }}
        </span>
        <button v-if="!viewEquipments" @click="viewEquipments = true">
          <i class="block h-4 w-4 text-primary"><ChevronDownIcon /></i>
        </button>
        <button v-else @click="viewEquipments = false">
          <i class="block h-4 w-4 text-primary"><ChevronUpIcon /></i>
        </button>
      </div>
    </div>
    <Transition>
      <div
        class="grid md:grid-cols-4 grid-cols-2 shadow-xl py-4"
        v-if="viewEquipments"
      >
      
        <Equipment
          v-for="equipment in group.equipments"
          :key="equipment.id"
          @mark="sendToBatch"
          @unmark="removeFromBatch"
          @notify="notifOn = true"
          @unnotify="notifOn = false"
          :id="equipment"
          :mother="group"
          :alled="all"
          :batched-items="batchedItems"
        />
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import Equipment from "@/components/inventory/Equipment.vue";
import NewInventory from "@/components/inventory/NewInventory.vue";
import {
  ChevronUpIcon,
  ChevronDownIcon,
} from "@heroicons/vue/solid";
const viewEquipments = ref(false);
const all = ref(false);
const notifOn = ref(false);
const props = defineProps({
  group: Object,
  batchedItems: Array,
});
const emits = defineEmits(["batched", "unbatched"]);

// const batch = ref([])
const sendToBatch = (item) => {
  emits("batched", item);
};
const removeFromBatch = (item) => {
  emits("unbatched", item);
};

const selectAll = () => {
  if (all.value) {
    props.group.equipments.forEach((item) => {
      sendToBatch(item);
    });
  } else {
    props.group.equipments.forEach((item) => {
      removeFromBatch(item);
    });
  }
};

watch(
  () => props.batchedItems.length,
  (newVal, oldVal) => {
    if (newVal === 0) all.value = false;
  }
);
</script>

<style>
.c-top-right-n3 {
  top: -3px;
  right: -3px;
}
</style>
