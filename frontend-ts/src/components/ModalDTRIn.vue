<template>
  <button
    @click="logoutToDTR"
    class="bg-red-500 text-white font-bold text-sm px-2 py-1 rounded-full"
  >
    Time Out
  </button>
  <!-- component -->
  <teleport to="body">
    <div v-if="!userstore.dtrIsLogged">
      <div
        class="bg-slate-800 bg-opacity-50 flex justify-center items-center absolute top-0 right-0 bottom-0 left-0"
      >
        <div
          class="bg-white px-16 py-14 rounded-md text-center justify-center flex flex-col"
        >
          <h1 class="text-xl mb-4 font-bold text-slate-500">
            Logging in to DTR...
          </h1>
          <!-- <button class="bg-green-500 px-7 py-2 ml-2 rounded-md text-md text-white font-semibold"
                        @click="loginToDTR">
                        Check in for DTR
                </button> -->
          <div
            class="w-12 h-12 mx-auto border-4 border-red-500 rounded-full"
            id="loader"
          ></div>
        </div>
      </div>
    </div>
  </teleport>
</template>

<script setup>
import { reactive, ref, onMounted } from "vue";
import axios from "axios";
import { userStore } from "@/stores/user";
import { dtrStore } from "@/stores/dtr";

const userstore = userStore();
const dtrstore = dtrStore();

const loginToDTR = async () => {
  if (!userstore.dtrIsLogged) {
    const response = await axios.put("/dtr_in/", {
      username: userstore.user,
    });
    localStorage.removeItem("dtrIsLogged");
    localStorage.setItem("dtrIsLogged", response.data.is_logged);
    userstore.dtrIsLoggedUpdate();
    location.reload(true);
  }
};

onMounted(() => {
  setTimeout(() => {
    loginToDTR();
  }, 3000);
});

const logoutToDTR = async () => {
  await axios.put("dtr_out/", {
    username: userstore.user,
    month: dtrstore.month,
    date: dtrstore.date,
    year: dtrstore.year,
  });
};
</script>

<style>
@keyframes loader-rotate {
  0% {
    transform: rotate(0);
  }
  100% {
    transform: rotate(360deg);
  }
}
#loader {
  border-right-color: transparent;
  animation: loader-rotate 5s linear infinite;
}
</style>
