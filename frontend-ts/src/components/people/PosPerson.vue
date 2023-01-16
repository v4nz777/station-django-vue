<template>
  <div
    :id="'person-' + person?.id"
    class="bg-white shadow-lg h-max rounded-md w-full relative">
    <Transition>
      <div
        v-if="open"
        class="w-full h-full bg-black absolute bg-opacity-25 flex justify-center items-center md:p-5">
        <div class="bg-white w-full h-full flex flex-col items-center justify-center">
          <p class="text-sm font-bold w-64 mb-2">Choose or add position...</p>
          <div class="w-64 bg-white shadow-lg border-primary z-50">
            <div class="flex border-2 border-primary gap-0.5">
              <p class="text-xs font-bold text-primary w-max mr-1">Position:</p>
              <input
                type="text"
                v-model="valuePosition"
                :id="'posInput-' + person?.id"
                @keyup="refactorPositions"
                @click="toggle"
                v-click-away="toggle"
                class="outline-none w-full text-xs"/>
              <button
                class="font-bold text-white px-1 text-xs hover:bg-active"
                :class="valuePosition ? 'bg-primary' : 'bg-disabled'"
                :disabled="!valuePosition"
                @click="assign">
                Save
              </button>
              <button
                class="font-bold text-white px-1 bg-red-500 text-xs"
                @click="open = false"
              >
                Cancel
              </button>
            </div>
            <ul class="border-x-2 border-b-2 border-primary bg-white w-64 absolute"
              v-if="positions.length">
              <li v-for="position in positions" :key="position.id"
                @click="valuePosition = position.title;positions = [];"
                class="text-sm text-primary hover:bg-primary hover:text-white cursor-pointer" >
                {{ position.title }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </Transition>
    <div class="bg-white p-4 flex-col">
      <div class="flex gap-10 justify-between mb-5 md:flex-row flex-col">
        <div class="flex w-max gap-3">
          <div class="w-12 h-12 overflow-hidden rounded-full">
            <img
              :src="
                person?.avatar
                  ? axios.defaults.baseURL + person?.avatar
                  : staticAvatar
              "
              class="object-cover w-full h-full"
            />
          </div>
          <div>
            <p class="font-bold text-lg">
              {{
                person?.first_name.charAt(0).toUpperCase() +
                person?.first_name.slice(0)
              }}
              {{
                person?.last_name.charAt(0).toUpperCase() +
                person?.last_name.slice(0)
              }}
            </p>
            <p class="text-sm">{{ person?.username }}</p>
            <div
              class="bg-primary font-bold text-white rounded-sm flex justify-center py-0.5 px-1 w-max"
            >
              <p class="text-xs">{{ current.title ?? "Unnasigned" }}</p>
            </div>
          </div>
        </div>
        <div class="p-2 w-max">
          <button
            class="text-white rounded-md shadow-md font-bold px-2 py-1 text-sm"
            @click="open = true"
            :class="viewer !== 'manager' ? 'bg-disabled' : 'bg-primary'"
            :disabled="viewer !== 'manager'"
            v-if="!open"
          >
            Assign
          </button>
        </div>
      </div>
      <div class="">
        <p class="font-thin text-sm">
          <span
            v-if="person?.is_logged"
            class="h-3 w-3 bg-green-500 inline-block rounded-full"
          ></span>
          <span
            v-else
            class="h-3 w-3 bg-red-500 inline-block rounded-full"
          ></span>
          {{ activity }}
        </p>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, onUnmounted } from "vue";
import axios from "axios";
import staticAvatar from "@/assets/avatar.png";
import { getPosition, useActivityStatus } from "@/composables/userdetails";
import type { Position } from "@/composables/userdetails";

const props = defineProps({
  person: Object,
  viewer: String,
});

const open = ref(false as boolean);
const current = ref({} as Position);
const positions = ref([] as Array<Position>);
const newPosition = ref({} as Position);
const valuePosition = ref("" as string);
const activity = ref("" as string);

const getPositions = async (filter: string) => {
  const response = await axios.get(`positions/${filter}`);
  positions.value = response.data;
};
const refactorPositions = async () => {
  if (valuePosition.value) {
    await getPositions(valuePosition.value);
    const titles = positions.value.map((elem) => elem.title);
    if (titles.includes(valuePosition.value)) {
      positions.value = [...positions.value];
    } else {
      newPosition.value = {
        title: valuePosition.value,
      } as any;
      positions.value = [newPosition.value, ...positions.value];
    }
  } else await getPositions("all");
};
const toggle = async (event: MouseEvent) => {
  const target = event.target as HTMLTextAreaElement;
  if (target.id === "posInput-" + props.person?.id) {
    if (valuePosition.value) await getPositions(valuePosition.value);
    else await getPositions("all");
  } else positions.value = [];
};

const assign = async () => {
  const fd = new FormData();
  fd.append("position_title", valuePosition.value);
  const response = await axios.post(`assign_pos/${props.person?.username}`, fd);
  current.value = response.data;
  positions.value = [] as Array<Position>;
  newPosition.value = {} as Position;
  valuePosition.value = "";
  open.value = false;
};

const trackTime = async () => {
  activity.value = useActivityStatus(
    props.person?.is_logged,
    props.person?.last_login
  );
};
const watchUpdate = setInterval(trackTime, 3000);

onMounted(async () => {
  if (props.person?.position)
    current.value = await getPosition(props.person?.position);
  activity.value = useActivityStatus(
    props.person?.is_logged,
    props.person?.last_login
  );
});
onUnmounted(() => {
  clearInterval(watchUpdate);
});
</script>
