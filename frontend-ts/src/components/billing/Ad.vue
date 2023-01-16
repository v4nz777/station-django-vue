<template>
  <!-- component -->
  <div
    :id="'contract-' + ad.contract"
    class="bg-white border-2 shadow-md h-full w-full rounded-xl hover:shadow-xl overflow-hidden flex flex-col items-center py-3 px-3 relative cursor-pointer"
    :class="
      adVersionView.ex_deal
        ? 'hover:shadow-orange-300 shadow-orange-100'
        : 'hover:shadow-primary shadow-secondary'
    "
    @click="open = true"
  >
    <!-- <span class="flex h-3 w-3 absolute top-1 right-1"
            v-if="codeOrange">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-yellow-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-3 w-3 bg-yellow-500"></span>
        </span>
        <span class="flex h-3 w-3 absolute top-1 right-1"
            v-else-if="codeRed">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-3 w-3 bg-primary"></span>
        </span> -->
    <div class="w-full">
      <p class="text-center font-bold w-full text-sm">
        {{ ad.title.toUpperCase() }}
      </p>
      <p class="text-xs text-center font-semibold w-full text-primary">
        #{{ ad.contract.toUpperCase() }}
      </p>
      <!-- <p class="text-xs text-center text-gray-700">{{advertiser.name}}</p> -->
    </div>

    <div class="w-full h-full relative border-t border-b mb-1">
      <div
        class="absolute w-full h-full bg-white bg-opacity-80 top-0 bottom-0 left-0 right-0 flex justify-center items-center"
        v-if="!unpaid"
      ></div>

      <div class="flex flex-col items-center w-full">
        <p
          class="text-2xl text-center font-bold text-gray-500"
          v-if="adVersionView.amount"
        >
          ₱{{ adVersionView.amount.toLocaleString("en-US") }}
        </p>
        <p class="text-xs text-center italic">{{ adVersionView.pricing }}</p>
      </div>
    </div>
    <div v-if="invoices.length && !unpaid">
      <p class="text-green-400 text-xs font-bold">
        <i class="inline-block w-4 h-4 align-middle"><CheckCircleIcon /></i>
        Last paid {{ lastPaid }}
      </p>
    </div>
    <div v-else-if="invoices.length && unpaid">
      <p class="text-red-400 text-xs font-bold">
        <i class="inline-block w-4 h-4 align-middle"
          ><InformationCircleIcon
        /></i>
        {{ unpaid }} uncollected payment
      </p>
    </div>
    <div v-else>
      <p class="text-yellow-400 text-xs font-bold">
        <i class="inline-block w-4 h-4 align-middle"
          ><ExclamationCircleIcon
        /></i>
        No recorded payment
      </p>
    </div>
  </div>
  <teleport to="body">
    <div
      v-if="open"
      @click.self="open = false"
      class="bg-slate-800 bg-opacity-50 flex justify-center items-center absolute top-0 right-0 bottom-0 left-0"
    >
      <div class="bg-white rounded-md w-adcontract h-5/6 px-5 py-5 relative">
        <!-- Options -->

        <div class="border-b-2 w-full text-center">
          <h1 class="text-3xl font-bold">{{ ad.title.toUpperCase() }}</h1>
          <p class="text-xs font-bold text-primary">
            #{{ ad.contract }}
            <span v-if="adVersionView.ex_deal" class="text-orange-500"
              >#EX-DEAL</span
            >
          </p>
          <p class="text-sm text-primary">{{ advertiser.name }}</p>
        </div>

        <!-- BILLING VIEW -->
        <AdInvoice
          :contract="ad.contract"
          :amount="adVersionView.amount"
          :pricing="adVersionView.pricing"
          :ae="ae"
          :advertiser="advertiser"
        />
        <!-- BILLING END -->
      </div>
    </div>
  </teleport>
</template>

<script setup>
import { ref, onMounted, onBeforeMount, onUpdated, watch } from "vue";
import axios from "axios";
import { userStore } from "@/stores/user";
import AudioItem from "@/components/AudioItem.vue";
import AdInvoice from "@/components/advertisements/AdInvoice.vue";
import {
  CheckCircleIcon,
  InformationCircleIcon,
  ExclamationCircleIcon,
} from "@heroicons/vue/solid";
import moment from "moment";

const baseURL = axios.defaults.baseURL;
const open = ref(false);
const adMenu = ref(false);
const contractView = ref("main");
const userstore = userStore();
const invoices = ref([]);
const unpaid = ref(0);
const lastPaid = ref("");
const props = defineProps({
  ad: Object,
  adscount: Number,
});
// Look for invoices in this contract

const lookForInvoices = async () => {
  const response = await axios.get(`invoices/${props.ad.contract}`);
  response.data.forEach((data) => {
    if (!data.paid) unpaid.value++;
  });
  invoices.value = response.data;
};
const getLatestPaymentDate = async () => {
  const now = moment();
  const dates = invoices.value.map((inv) => moment(inv.or_date));
  const latest = moment.max(dates);
  if (invoices.value.length) {
    if (now.isSame(latest, "day")) lastPaid.value = "Today";
    else lastPaid.value = latest.fromNow();
  }
};

const adVersionView = ref({});

// Reload version
const getVersionView = async () => {
  const response = await axios.get(
    `ad/${props.ad.contract}/${props.ad.current_ver}`
  );
  adVersionView.value = response.data;
};

const advertiser = ref({});

const ae = ref("");
const getAE = async () => {
  if (
    adVersionView.value &&
    adVersionView.value.account_executive !== "office"
  ) {
    const response = await axios.get(
      `user/${adVersionView.value.account_executive}`
    );
    ae.value =
      response.data.first_name.charAt(0).toUpperCase() +
      response.data.first_name.slice(1) +
      " " +
      response.data.last_name.charAt(0).toUpperCase() +
      response.data.last_name.slice(1);
  } else ae.value = "Office";
};

const isLoaded = ref(false);
const getadvertiser = async () => {
  const response = await axios.get(`/advertiser/${props.ad.advertiser}`);
  if (response.status === 200) advertiser.value = response.data;
};

const refresh = async () => {
  // get advertiser
  await getadvertiser();

  await getAE();

  isLoaded.value = true;
};

onMounted(async () => {
  // get ad details by version
  await getVersionView();
  await lookForInvoices();
  setTimeout(async () => {
    await refresh();
  }, 1000);
  getLatestPaymentDate();
});

//refresh if added new ad to list
watch(
  () => props.adscount,
  async (newval, oldval) => {
    if (newval !== oldval) {
      await getVersionView();
      await refresh();
      contractView.value = "main";
    }
  }
);

// refresh if current version is changed
watch(
  () => props.ad.current_ver,
  async (newval, oldval) => {
    if (newval !== oldval) {
      await getVersionView();
      await refresh();
    }
  }
);
</script>

<style>
.sched-grid {
  display: grid;
  grid-gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(50px, 1fr));
  /* grid-template-rows: repeat(auto-fit, 208px); */
}
.tagline {
  z-index: 1;
  position: absolute;
  top: -5px;
  right: -10px;
  font-size: 0.55rem;
  line-height: 0.75rem;
  border-radius: 0.25rem;
}

.none-scroll::-webkit-scrollbar {
  width: 4px;
  cursor: pointer;
  /*background-color: rgba(229, 231, 235, var(--bg-opacity));*/
  display: none;
}
.none-scroll::-webkit-scrollbar-track {
  /* background-color: rgba(229, 231, 235, var(--bg-opacity)); */
  cursor: pointer;
  background: #a0b7c0b4;
  display: none;
}
.none-scroll::-webkit-scrollbar-thumb {
  cursor: pointer;
  background-color: rgba(73, 121, 224, 0.667);
  display: none;
  /*outline: 1px solid slategrey;*/
}
.w-adcontract {
  width: 35rem;
}
</style>
