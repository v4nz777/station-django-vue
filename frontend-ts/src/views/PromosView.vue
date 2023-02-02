<template>
  <div class="flex flex-col justify-center items-center gap-20 w-full">
    <div class="flex">
      <img :src="onGoing" alt="" class="md:w-24 h-24 w-max animate-bounce">
      <p class="font-bold text-3xl w-full h-full text-center self-baseline">Build ongoing...</p>
      <button @click="trying">click</button>
      <div>{{ activityData }}</div>
    </div>
    
  </div>
</template>
<script setup lang="ts">
  import { onMounted,onUnmounted } from "vue";
  import onGoing from "@/assets/ongoing.png"
  import { activityData, openActivitiesConnection, sendActivity } from "@/composables/activities"
  

  let socket:WebSocket;

  const trying = ()=> {
    sendActivity(socket, "new obj")
    console.log(activityData.value)
  }
  
  onMounted(async ()=> {
      socket = openActivitiesConnection()
  })

  onUnmounted(() => {
    socket.close()
  })

 
  
</script>
