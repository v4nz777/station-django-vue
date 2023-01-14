<template>
  <header class="h-12 flex flex-row-reverse md:flex-row">
    <div class="shadow-3xl overflow-hidden rounded-full object-fill">
      <img
        class="h-11 self-center"
        src="../assets/stationlogo.png"
        alt="StationLogo"
      />
    </div>

    <div v-if="userstore.user" class="flex justify-center">
      <BurgerMenu class="md:hidden block" />
      <LogOut class="md:block hidden" />
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from "vue";
import axios from "axios";
import { userStore } from "../stores/user";
import { dtrStore } from "../stores/dtr";
import BurgerMenu from "@/components/BurgerMenu.vue";
import LogOut from "@/components/LogOut.vue";

const dtrstore = dtrStore();
const userstore = userStore();
const open = ref(false);

const logoutToDTR = async () => {
  const response = await axios.put("/dtr_out/", {
    username: userstore.user,
    month: dtrstore.month,
    date: dtrstore.date,
    year: dtrstore.year,
  });
  userstore.dtrIsLogged = false;

  open.value = false;
  userstore.logOutUser();
};
</script>
