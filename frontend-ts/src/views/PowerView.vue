<template>
  <div class="flex md:w-full w-screen px-5">
    <div class="w-full px-5">
      <ConsumptionChart :data_labels="{ labels: _labels, data: _data }" />

      <div
        class="w-full h-max bg-white rounded-3xl my-5 px-5 py-2 shadow-xl shadow-yellow-500 flex"
      >
        <NewPowerConsumption @done="loadConsumptionData" />
      </div>

      <ConsumptionData
        v-for="(datum, index) in data"
        :key="index"
        :datum="datum"
        @send="sendDataToChart"
      />
    </div>
  </div>
</template>

<script lang="ts" setup>
import NewPowerConsumption from "@/components/power/NewPowerConsumption.vue";

import ConsumptionChart from "@/components/power/ConsumptionChart.vue";
import ConsumptionData from "@/components/power/ConsumptionData.vue";
import { onMounted } from "vue";
import { ref } from "vue";
import axios from "axios";

const data = ref([]);
const loadConsumptionData = async () => {
  const response = await axios.get("get_power_readings");
  data.value = response.data;
};
const _labels = ref([] as Array<any>);
const _data = ref([] as Array<any>);
const sendDataToChart = (data: any) => {
  _labels.value = Array.from([data.dt.month, ..._labels.value]);
  _data.value = Array.from([data.kwh_used, ..._data.value]);
};

onMounted(async () => {
  await loadConsumptionData();
});
</script>
