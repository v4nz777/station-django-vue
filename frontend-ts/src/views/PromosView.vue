<template>
  <div class="flex flex-col justify-center items-center gap-20 w-full">
    <div class="flex">
      <img :src="onGoing" alt="" class="md:w-24 h-24 w-full animate-bounce">
      <p class="font-bold text-3xl w-full h-full text-center self-baseline">Build ongoing...</p>
      
    </div>
    
  </div>
</template>
<script setup lang="ts">
  import onGoing from "@/assets/ongoing.png"
</script>
