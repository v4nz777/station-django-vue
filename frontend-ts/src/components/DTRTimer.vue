<template>
  <button
    @click="logoutToDTR"
    v-if="logged"
    class="bg-red-500 text-white font-bold text-sm px-2 py-1 rounded-full"
  >
    Time Out
  </button>
  <div
    class="flex bg-white rounded-2xl b-border shadow-md justify-center items-center px-2 h-9"
  >
    <p class="justify-self-start py-2" v-if="logged">
      ⏱️<span class="text-red-500 text-sm font-normal">{{
        dtrstore.formatLogTimer
      }}</span>
    </p>
    <p
      class="justify-self-start py-2 cursor-pointer"
      v-else
      @click="loginToDTR"
    >
      <span class="text-red-500 text-sm font-bold">Time In</span>
    </p>
  </div>
</template>

<script setup>
import { dtrStore } from "@/stores/dtr";
import { userStore } from "@/stores/user";
import { ref, onMounted, watch } from "vue";
import axios from "axios";
const userstore = userStore();
const dtrstore = dtrStore();
const logged = ref(false);

const loginToDTR = async () => {
  if (!logged.value) {
    const response = await axios.put("/dtr_in/", {
      username: userstore.user,
    });
    logged.value = response.data.is_logged;
    // localStorage.removeItem("dtrIsLogged")
    // localStorage.setItem("dtrIsLogged", response.data.is_logged)
    // userstore.dtrIsLoggedUpdate()
    await dtrstore.loadDTR();
    dtrstore.watchTimer();
  }
};
const logoutToDTR = async () => {
  if (logged.value) {
    const response = await axios.put("dtr_out/", {
      username: userstore.user,
      month: dtrstore.month,
      date: dtrstore.date,
      year: dtrstore.year,
    });
    logged.value = response.data.is_logged;
    dtrstore.clear();
  }
};

const watchUser = async () => {
  const response = await axios.get(`user/${userstore.user}`);
  logged.value = response.data.is_logged;
};

onMounted(async () => {
  await watchUser();
  await dtrstore.loadDTR();
  dtrstore.watchTimer();
});
</script>
