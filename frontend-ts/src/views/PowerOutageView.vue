<template>
  <div class="md:w-full w-screen px-5">
    <div class="w-full flex flex-col items-center">
      <!-- <ConsumptionChart
            :data_labels="{labels:_labels,data:_data}"/> -->

      <div
        class="md:w-3/4 w-full h-max bg-white rounded-3xl my-5 px-1 py-2 shadow-lg shadow-yellow-500 flex"
      >
        <NewPowerOutage />
        <!-- @done="loadConsumptionData" /> -->
      </div>

      <PowerOutages v-for="datum in data" :datum="datum" :key="datum.id" />
    </div>
  </div>
</template>

<script setup>
import NewPowerOutage from "@/components/power/NewPowerOutage.vue";
import PowerOutages from "@/components/power/PowerOutages.vue";
import { onMounted } from "vue";
import { ref } from "vue";
import axios from "axios";

const data = ref([]);
const loadConsumptionData = async () => {
  const response = await axios.get("get_power_interruptions");
  data.value = response.data;
};
const _labels = ref([]);
const _data = ref([]);

onMounted(() => {
  loadConsumptionData();
});
</script>
