<template>
  <div class="flex flex-col justify-center items-center gap-20 w-full">
    <div class="flex">
      <img :src="onGoing" alt="" class="md:w-24 h-24 w-max animate-bounce">
      <p class="font-bold text-3xl w-full h-full text-center self-baseline">Build ongoing...</p>
      
    </div>
    
  </div>
</template>
<script setup lang="ts">
  import { onMounted } from "vue";
  import onGoing from "@/assets/ongoing.png"
  
  // const socket = new WebSocket("wss://127.0.0.1:8000")
  // console.log(socket)

  


  onMounted(async ()=> {

    const sse = new EventSource("http://127.0.0.1:8000/events/data-sent")

    
    // sse.addEventListener('stream-open',(event)=> {
    //   console.log(event)
    // })
    // sse.addEventListener('message',(event)=> {
    //   console.log(event)
    // })

    sse.addEventListener('data-sent',(event)=> {
      console.log(event)
    })
    // sse.addEventListener('data-sent', (event)=> {
    //   console.log(event)
    // })
 
    
    
    
    
  })
  
  // sse.onopen((event:any) => {
  //   console.log(event)
  // })
 
  
</script>
