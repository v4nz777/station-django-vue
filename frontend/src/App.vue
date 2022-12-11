<template>
  
    <Header class="flex justify-between px-3 bg-primary flex-wrap text-white font-medium b-border shadow-lg"
            v-if="userstore.user"/>

    <div class="flex flex-row h-screen w-screen fixed bg-secondary">
      <Sidebar class="flex-shrink md:flex hidden" 
              v-if="userstore.user"/>

      <div class="overflow-y-scroll mx-auto w-full flex justify-center mb-14" id="mainview-scroll">
        <RouterView />
      </div>

      <!-- <Rightbar class="md:block hidden w-56"
            v-if="userstore.user" /> -->
    </div>

  
</template>

<script setup>
  import { onMounted, watch } from "vue";
  import { userStore } from "@/stores/user";
  import axios from "axios";
  import Header from "./components/Header.vue"
  import Sidebar from "./components/Sidebar.vue";
  import Rightbar from "@/components/Rightbar.vue";
  import { RouterView } from 'vue-router';
  const userstore = userStore()

  // Refresh user details
  onMounted(() => {
    if (localStorage.getItem("accessToken")) {
      userstore.initUser()
    }
    userstore.loadUser()
    
  })

  // Need to use arrow fucntions for watching Pinia states
  watch(()=> userstore.user, ()=> userstore.loadUser())

 

</script>

<style>
  #mainview-scroll::-webkit-scrollbar {
      width: 5px;
      cursor: pointer;
      /*background-color: rgba(229, 231, 235, var(--bg-opacity));*/

  }
  #mainview-scroll::-webkit-scrollbar-track {
      /* background-color: rgba(229, 231, 235, var(--bg-opacity)); */
      cursor: pointer;
      background: #d1a9a962;
      border-radius: 1rem;
      margin-top: 0.5rem;
      margin-bottom: 5rem;
  }
  #mainview-scroll::-webkit-scrollbar-thumb {
      cursor: pointer;
      background-color: rgba(224, 73, 73, 0.315);
      border-radius: 1rem;
      /*outline: 1px solid slategrey;*/
  }
</style>