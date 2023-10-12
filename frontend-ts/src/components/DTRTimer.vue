<template>
  <Transition>
    <button
      @click="logoutToDTR"
      v-if="dtrstore.timed"
      class="bg-red-500 text-white font-bold text-sm px-2 py-1 rounded-full"
    >
      Time Out
    </button>
  </Transition>
  <div
    class="flex bg-white rounded-2xl b-border shadow-md justify-center items-center px-2 h-9"
  >
    <p class="justify-self-start py-2" v-if="dtrstore.timed">
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
import { ref, onMounted } from "vue";
import { sendActivity } from '@/composables/activities'
import axios from "axios";

const props = defineProps({
  socket:WebSocket|null|undefined
})


const userstore = userStore();
const dtrstore = dtrStore();



const loginToDTR = async () => {
  console.log(props.socket.readyState)
  if (!dtrstore.timed) {
    let response;
    try{
      response = await axios.put("/dtr_in/", {
        username: userstore.user,
      });
      
      await dtrstore.loadDTR();
      dtrstore.watchTimer();
      dtrstore.timed = await response.data.is_logged;
      sendActivity(props.socket,"logged in!")
      return;
    }
    catch(error){
      alert('DTR Login Unsuccessful!')
      console.log('DTR Login Unsuccessful!')
    }
    
  }
};


const logoutToDTR = async () => {
  if (dtrstore.timed) {
    let response;
    try{
        response = await axios.put("dtr_out/", {
        username: userstore.user,
        month: dtrstore.month,
        date: dtrstore.date,
        year: dtrstore.year,
      });
      
      const total = dtrstore.formatLogTimer;
      dtrstore.timed = await response.data.is_logged;
      // dtrstore.clear();
      sendActivity(props.socket,`logged out! (total: ${total})`)
      return;
    }
    catch(error){
      alert('DTR Logout Unsuccessful!')
      console.log('DTR Logout Unsuccessful!')
    }
    
  }
};



const watchUser = async () => {
  const response = await axios.get(`user/${userstore.user}`);
  dtrstore.timed = response.data.is_logged;
};

onMounted(async () => {
  if(userstore.dtrIsLogged){
    await dtrstore.loadDTR();
    dtrstore.watchTimer();
  }
  await watchUser();
  
});

</script>






<style>
.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
