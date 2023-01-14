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
        ><ChipIcon
      /></i>
      <h3 class="text-sm font-light">Log</h3>
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
            <h1 class="font-bold text-primary text-xl">
              Log Transmitter Status
            </h1>
            <hr class="w-full" />
          </div>
          <div class="w-full h-full">
            <div class="w-full">
              <div class="text-center">
                <p class="font-bold text-gray-600 text-sm">Log for</p>
                <p class="font-bold text-primary text-xl">{{ hour }}</p>
                <p class="font-bold text-gray-600 text-xs">({{ time }})</p>
              </div>
              <div class="border-t flex justify-center py-1">
                <button
                  class="text-contrast text-xs font-thin bg-primary rounded-sm px-1"
                  @click="copy"
                >
                  Copy
                </button>
                <p class="text-xs italic font thin text-primary">
                  &nbsp; if same from recent hour
                </p>
              </div>
              <div class="flex justify-center px-2 border-y py-3 text-sm">
                <div class="flex flex-col text-right text-primary">
                  <p class="my-1">Line Voltage:</p>
                  <p class="my-1">Exciter:</p>
                </div>
                <div class="flex flex-col px-2">
                  <input
                    class="w-24 bg-primary rounded-sm text-contrast my-1 pl-2"
                    type="number"
                    v-model="line_voltage"
                  />
                  <input
                    class="w-24 bg-primary rounded-sm text-contrast my-1 pl-2"
                    type="number"
                    v-model="exciter"
                  />
                </div>
              </div>

              <div class="flex justify-between w-full py-3">
                <div class="border-r flex w-full">
                  <div class="flex flex-col px-2 w-full items-center">
                    <p class="my-1 text-sm text-primary">Driver Voltage:</p>
                    <input
                      class="w-24 bg-primary rounded-sm text-contrast mb-1 pl-2"
                      type="number"
                      v-model="driver_voltage"
                    />
                    <p class="my-1 text-sm text-primary">Driver Current:</p>
                    <input
                      class="w-24 bg-primary rounded-sm text-contrast mb-1 pl-2"
                      type="number"
                      v-model="driver_current"
                    />

                    <p class="my-1 text-sm text-primary">Driver Forward:</p>
                    <input
                      class="w-24 bg-primary rounded-sm text-contrast mb-1 pl-2"
                      type="number"
                      v-model="driver_forward"
                    />

                    <p class="my-1 text-sm text-primary">Driver RF:</p>
                    <input
                      class="w-24 bg-primary rounded-sm text-contrast mb-1 pl-2"
                      type="number"
                      v-model="driver_rf"
                    />
                  </div>
                </div>
                <div class="border-l flex w-full">
                  <div class="flex flex-col px-2 w-full items-center">
                    <p class="my-1 text-sm text-primary">Final Voltage:</p>
                    <input
                      class="w-24 bg-primary rounded-sm text-contrast mb-1 pl-2"
                      type="number"
                      v-model="final_voltage"
                    />
                    <p class="my-1 text-sm text-primary">Final Current:</p>
                    <input
                      class="w-24 bg-primary rounded-sm text-contrast mb-1 pl-2"
                      type="number"
                      v-model="final_current"
                    />

                    <p class="my-1 text-sm text-primary">Final Forward:</p>
                    <input
                      class="w-24 bg-primary rounded-sm text-contrast mb-1 pl-2"
                      type="number"
                      v-model="final_forward"
                    />
                    <p class="my-1 text-sm text-primary">Final RF:</p>
                    <input
                      class="w-24 bg-primary rounded-sm text-contrast mb-1 pl-2"
                      type="number"
                      v-model="final_rf"
                    />
                  </div>
                </div>
              </div>

              <div
                class="flex flex-col justify-center px-2 border-y py-3 text-sm"
              >
                <p class="my-1 text-sm text-primary">Remarks:</p>
                <textarea
                  v-model="remarks"
                  cols="30"
                  rows="5"
                  class="border-2 shadow-l p-2"
                >
                </textarea>
              </div>
              <div class="w-full flex justify-center">
                <button
                  @click="submit()"
                  class="font-bold w-24 text-contrast my-3"
                  :disabled="!valid"
                  :class="valid ? 'bg-primary' : 'bg-disabled'"
                >
                  LOG
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </teleport>
  </div>
</template>
<script setup>
import { ChipIcon } from "@heroicons/vue/solid";

import { ref, onMounted, onUnmounted } from "vue";
import moment from "moment";
import axios from "axios";
import { userStore } from "@/stores/user";

const emits = defineEmits(["new"]);
const open = ref(false);
const parentIsHovered = ref(false);
const outer = ref(null);

const hour = ref(null);

const date = ref(null);
const time = ref(null);
const line_voltage = ref(null);
const exciter = ref(null);
const driver_voltage = ref(null);
const driver_current = ref(null);
const driver_forward = ref(null);
const driver_rf = ref(null);
const final_current = ref(null);
const final_voltage = ref(null);
const final_forward = ref(null);
const final_rf = ref(null);
const remarks = ref("");

const valid = ref(false);
const validate = () => {
  if (
    line_voltage.value !== null &&
    exciter.value !== null &&
    driver_current.value !== null &&
    driver_forward.value !== null &&
    driver_rf.value !== null &&
    final_current.value !== null &&
    driver_voltage.value !== null &&
    final_voltage.value !== null &&
    final_forward.value !== null &&
    final_rf.value !== null
  ) {
    valid.value = true;
  } else valid.value = false;
};

// copy from recent hour's log
const copy = async () => {
  const response = await axios.get("tx_logs/last");
  const recent = response.data;

  line_voltage.value = recent.line_voltage;
  exciter.value = recent.exciter;
  driver_voltage.value = recent.driver_voltage;
  driver_current.value = recent.driver_current;
  driver_forward.value = recent.driver_forward;
  driver_rf.value = recent.driver_rf;
  final_current.value = recent.final_current;
  final_voltage.value = recent.final_voltage;
  final_forward.value = recent.final_forward;
  final_rf.value = recent.final_rf;
  remarks.value = recent.remarks;
};

// autoupdate date and time
const watchDate = setInterval(() => {
  // refresh date every 5 minutes
  date.value = moment().format("YYYY-M-D");
}, 300000);
const watchTime = setInterval(() => {
  // refresh date every seconds
  time.value = moment().format("H:mm:ss");
  hour.value = moment().format("H A");
}, 1000);
// check form validity every second
const watchValidity = setInterval(() => {
  validate();
}, 1000);

//Lifecycles
onMounted(() => {
  date.value = moment().format("YYYY-M-D");
  watchDate;
  watchTime;
  watchValidity;
});
onUnmounted(() => {
  clearInterval(watchTime);
  clearInterval(watchValidity);
});

const submit = async () => {
  const fd = new FormData();
  fd.append("date", date.value);
  fd.append("time", time.value);
  fd.append("line_voltage", line_voltage.value);
  fd.append("exciter", exciter.value);
  fd.append("driver_voltage", driver_voltage.value);
  fd.append("driver_current", driver_current.value);
  fd.append("driver_forward", driver_forward.value);
  fd.append("driver_rf", driver_rf.value);
  fd.append("final_current", final_current.value);
  fd.append("final_voltage", final_voltage.value);
  fd.append("final_forward", final_forward.value);
  fd.append("final_rf", final_rf.value);
  fd.append("author", userStore().user);
  fd.append("remarks", remarks.value);

  const response = await axios.post("tx_log", fd);
  if (response.status === 200) {
    emits("new");
    line_voltage.value = null;
    exciter.value = null;
    driver_voltage.value = null;
    driver_current.value = null;
    driver_forward.value = null;
    driver_rf.value = null;
    final_current.value = null;
    final_voltage.value = null;
    final_forward.value = null;
    final_rf.value = null;
    remarks.value = "";
    open.value = false;
  }
};
</script>
