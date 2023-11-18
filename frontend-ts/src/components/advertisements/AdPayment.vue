<template>
  <button
    class="bg-blue-900 text-white w-max px-3 py-1 rounded-xl flex items-center font-bold hover:bg-blue-500"
    :disabled="open"
    @click="togglePayment"
  >
    <span
      v-if="open"
      class="animate-spin h-5 w-5 border-white border-b-3 border-x-2 rounded-full"
    ></span>
    <span v-else>pay</span>
  </button>

  <div
    v-if="open"
    v-click-away="togglePayment"
    class="absolute z-20 bottom-0 right-10 w-52 h-max bg-blue-100 shadow-md border p-2"
  >
    <div class="flex justify-between mb-3">
      <p class="font-bold">Payment for Invoice#{{ invoice.invoice_no }}</p>
    </div>
    <div class="flex justify-between my-1">
      <label for="" class="mr-2">Amount:</label>
      <input
        type="text"
        class="focus-visible:outline-2 w-24 bg-sky-300 focus-within:outline-sky-500 font-thin text-sm px-2 py-1 shadow-md rounded-r-md text-sky-900 focus-within:bg-sky-100"
        v-model="receivedAmount"
      />
    </div>
    <div class="flex justify-between my-1">
      <label for="" class="mr-2">OR #:</label>
      <input
        type="text"
        class="focus-visible:outline-2 w-24 bg-sky-300 focus-within:outline-sky-500 font-thin text-sm px-2 py-1 shadow-md rounded-r-md text-sky-900 focus-within:bg-sky-100"
        v-model="orNumber"
      />
    </div>
    <div class="flex justify-between my-1">
      <label for="" class="mr-2">OR Date:</label>
      <input
        type="date"
        class="focus-visible:outline-2 w-24 bg-sky-300 focus-within:outline-sky-500 font-thin text-sm px-2 py-1 shadow-md rounded-r-md text-sky-900 focus-within:bg-sky-100"
        v-model="orDate"
      />
    </div>
    <div class="flex justify-end my-3">
      <button
        class="text-white font-bold rounded-md px-2 py-1"
        :class="!isValid ? 'bg-blue-200' : 'bg-blue-900 hover:bg-blue-500'"
        :disabled="!isValid"
        @click="submitPayment"
      >
        Save Payment
      </button>
    </div>
  </div>
</template>
<script setup>
import axios from "axios";
import { ref, onMounted, onUnmounted } from "vue";
const receivedAmount = ref(0);
const orNumber = ref("");
const orDate = ref("");

const props = defineProps({
  invoice: Object,
});
const emits = defineEmits(["submitted"]);
const open = ref(false);
const togglePayment = () => {
  if (open.value === false) open.value = true;
  else open.value = false;
};
const isValid = ref(false);
const chackValidity = setInterval(() => {
  if (receivedAmount.value && orNumber.value && orDate.value) {
    isValid.value = true;
  } else {
    isValid.value = true;
  }
}, 1000);
const submitPayment = async () => {
  const fd = new FormData();
  fd.append("invoice_no", props.invoice.invoice_no);
  fd.append("or_date", orDate.value);
  fd.append("or_number", orNumber.value);
  fd.append("amount_received", receivedAmount.value);

  const response = await axios.post("pay_invoice", fd);
  if (response.status === 200) emits("submitted");
};
onMounted(() => {
  receivedAmount.value = props.invoice.amount;
  chackValidity;
});
onUnmounted(() => {
  clearInterval(chackValidity);
});
</script>
