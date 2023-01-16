<template>
  <div class="mx-auto my-3">
    <button
      @click="open = true"
      @mouseover="parentIsHovered = true"
      @mouseout="parentIsHovered = false"
      class="w-32 rounded-md hover:shadow-md flex items-center justify-start px-2 h-9 hover:bg-primary hover:text-white"
    >
      <i
        class="h-6 w-6"
        :class="parentIsHovered ? 'text-white' : 'text-primary'"
        ><LightningBoltIcon
      /></i>
      <h3 class="text-sm font-light">Power Outage</h3>
    </button>
    <teleport to="body">
      <div
        class="bg-slate-800 bg-opacity-50 flex justify-center items-center absolute top-0 right-0 bottom-0 left-0"
        v-if="open"
        ref="outer"
        @click.self="open = false"
      >
        <div
          class="bg-white rounded-md text-start justify-start flex flex-col w-96"
        >
          <div class="flex flex-col justify-center text-center py-4 w-full">
            <h1 class="font-bold text-gray-500 text-xl">Report Power Outage</h1>
            <hr class="my-4 w-full" />
          </div>
          <div class="flex flex-col justify-center my-5 w-56 mx-auto mb-8">
            <label class="flex items-center mb-5">
              <input
                type="checkbox"
                class="form-checkbox"
                v-model="scheduled"
              />
              <span class="ml-2 text-primary font-semibold"
                >Check if scheduled!</span
              >
            </label>
            <hr />

            <label for="brownOutStart" class="text-primary font-semibold"
              >🔦 Power Interrupted:</label
            >
            <input
              type="datetime-local"
              id="brownOutStart"
              class="text-white font-thin bg-primary text-sm px-3 py-1 mt-2 rounded-md"
              v-model="interrupted"
              @change="calculateDuration"
            />
            <hr class="my-6" />
            <label for="brownOutRestored" class="text-primary font-semibold"
              >🔅 Power Restored:</label
            >
            <input
              type="datetime-local"
              id="brownOutRestored"
              class="text-white font-thin bg-primary text-sm px-3 py-1 mt-2 rounded-md"
              v-model="restored"
              @change="calculateDuration"
            />
          </div>
          <hr />

          <div
            class="my-5 text-gray-500 text-center flex flex-col justify-center items-center"
            v-if="duration"
          >
            <span class="font-medium"
              >Brown Out Duration:
              <span class="text-blue-500">{{ duration }}</span></span
            >
            <button
              class="border px-5 py-2 text-white bg-red-500 my-5 font-bold text-lg"
              @click="submit"
            >
              Submit
            </button>
          </div>
        </div>
      </div>
    </teleport>
  </div>
</template>
<script setup>
import { LightningBoltIcon } from "@heroicons/vue/solid";
import DTRTable from "@/components/DTRTable.vue";
import { ref } from "vue";
import moment from "moment";
import axios from "axios";
import { userStore } from "@/stores/user";

const interrupted = ref(null);
const restored = ref(null);
const scheduled = ref(false);
const open = ref(false);
const duration = ref(null);
const parentIsHovered = ref(false);
const outer = ref(null);

const calculateDuration = () => {
  if (interrupted.value && restored.value) {
    const i = moment(interrupted.value);
    const r = moment(restored.value);

    const dms = r.diff(i); //duration in ms

    const mins = Math.floor((dms / 1000 / 60) % 60);
    const hrs = Math.floor(dms / 1000 / 60 / 60);

    const hrprefix = hrs > 1 ? "hrs" : "hr";
    const minprefix = mins > 1 ? "mins" : "min";

    if (hrs > 0) {
      duration.value = `${hrs} ${hrprefix} : ${mins} ${minprefix}`;
    } else {
      duration.value = `${mins} ${minprefix}`;
    }
  }
};

const submit = async () => {
  // const fd = new FormData()
  // fd.append("interrupted", interrupted.value)
  // fd.append("restored", restored.value)
  // fd.append("duration", duration.value)
  const userstore = userStore();
  const fd = new FormData();
  fd.append("interrupted", interrupted.value);
  fd.append("restored", restored.value);
  fd.append("author", userstore.user);
  fd.append("scheduled", scheduled.value);
  const response = await axios.post("new_power_interruption", fd);
  console.log(response.data.message);

  interrupted.value = null;
  restored.value = null;
  duration.value = null;
  outer.value.click();
};
</script>
