<template>
  <div class="flex flex-col md:w-full w-screen px-5 items-center">
    <div
      class="flex justify-around items-center w-full h-max bg-white rounded-3xl p-10 mt-3 mb-6 shadow-md md:flex-row flex-col gap-10 relative"
    >
      <div class="absolute top-3 right-5 border-2 shadow-md flex px-1 text-xs">
        <p class="font-bold text-primary">Filter</p>
        <select name="" id="" class="outline-none" v-model="filterForTotal">
          <option value="today">Today</option>
          <option value="month">This Month</option>
          <option value="year">This Year</option>
          <option value="all">All</option>
        </select>
      </div>
      <div class="w-max mt-4">
        <p class="w-full text-gray-500 text-center text-xs font-bold">Sales</p>
        <p class="w-full text-green-500 text-center font-bold text-3xl">
          {{ totalSales }}
        </p>
      </div>
      <div class="w-max mt-4">
        <p class="w-full text-gray-500 text-center text-xs font-bold">
          Collection
        </p>
        <p class="w-full text-green-500 text-center font-bold text-3xl">
          {{ totalCollected }}
        </p>
      </div>
    </div>

    <div v-if="loaded" class="w-full">
      <div
        class="mb-10 pb-10 h-max w-full gap-4"
        :class="
          adsList.length < 4
            ? 'md:flex md:justify-center grid grid-cols-2'
            : 'grid-auto-cols'
        "
      >
        <div v-if="adsList.length" v-for="i in adsList" :key="i.id">
          <Ad :ad="i" :adscount="adsList.length" />
        </div>
        <div v-else>
          <p class="text-center font-bold">No advertisement yet!</p>
        </div>
      </div>
    </div>
    <div
      v-else
      class="w-full h-screen flex flex-col justify-center items-center"
    >
      <div
        class="w-12 h-12 mx-auto border-4 border-primary rounded-full"
        id="loader"
      ></div>
    </div>
  </div>
</template>
<script setup>
import axios from "axios";
import { ref, watch, onMounted, onUnmounted } from "vue";
import Ad from "@/components/billing/Ad.vue";
import { dtrStore } from "@/stores/dtr";
import NewAds from "@/components/advertisements/NewAds.vue";
const filter = ref("all");
const filterForTotal = ref("month");
const adsList = ref([]);
const loaded = ref(false);
const dtrstore = dtrStore();
const totalCollected = ref("0");
const totalSales = ref("0");

const getAds = async (_filter) => {
  const currentcount = adsList.value.length;
  const response = await axios.get(`ads/${_filter}`);

  if (currentcount !== response.data.length) {
    loaded.value = false;
    adsList.value = [];
  }
  adsList.value = response.data;
  loaded.value = true;
};

const watchAds = setInterval(() => {
  getAds(filter.value);
}, 1000);

// number to currency formatter
const filPeso = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "PHP",
  maximumFractionDigits: 0,
});

//Get and calculate collections
const getTotalCollections = async () => {
  const response = await axios.get(`total_collections/${filterForTotal.value}`);
  //convert to currency format
  totalCollected.value = filPeso.format(response.data.total);
};

//Get and calculate sales
const getTotalSales = async () => {
  const response = await axios.get(`total_sales/${filterForTotal.value}`);
  //convert to currency format
  totalSales.value = filPeso.format(response.data.total);
};

watch(
  () => filterForTotal.value,
  async () => {
    await getTotalCollections();
    await getTotalSales();
  }
);

onMounted(async () => {
  dtrstore.loadDTR();
  watchAds;
  await getTotalCollections();
  await getTotalSales();
});
onUnmounted(() => {
  clearInterval(watchAds);
});
</script>

<style>
.grid-auto-cols {
  display: grid;
  grid-gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(208px, 1fr));
  /* grid-template-rows: repeat(auto-fit, 208px); */
}
.w-ads {
  width: 40rem;
}
.w-ads-controls {
  width: 45rem;
}
</style>
