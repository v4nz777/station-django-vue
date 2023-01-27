<template>
  <header class="h-16 flex flex-row-reverse md:flex-row">
    <div class="flex flex-row-reverse md:flex-row justify-start items-center gap-1">
      <div class="shadow-3xl overflow-hidden rounded-sm object-fill">
        <img
          class="h-11 self-center"
          :src="station.logo?baseURL+station.logo:logo"
          alt="StationLogo"
        />
      </div>
      <p class="font-bold text-xl" id="stationTitle">{{ station.call_sign }} <span class="font-thin">{{ station.frequency }}</span></p>
    </div>
    
    

    <div v-if="userstore.user" class="flex justify-center">
      <BurgerMenu class="md:hidden block" />
      <LogOut class="md:block hidden" />
    </div>
  </header>
</template>

<script setup lang="ts">
// import logo from "@"
import { ref, onMounted } from "vue";
import axios from "axios";
import { userStore } from "../stores/user";
import { dtrStore } from "../stores/dtr";
import BurgerMenu from "@/components/BurgerMenu.vue";
import LogOut from "@/components/LogOut.vue";
import logo from "@/assets/logow.png"

const baseURL = axios.defaults.baseURL
const dtrstore = dtrStore();
const userstore = userStore();
const open = ref(false);
const station = ref({} as any)

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

const loadStationInfo = async ()=> {
  const response = await axios.get("about")
  station.value = response.data
  const title = document.querySelector('#stationTitle') as HTMLElement
  title.style.color = station.value.main_font_color??'white'
}

onMounted(async() => {
  await loadStationInfo()

})
</script>
