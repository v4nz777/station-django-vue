
<template>
  <div class="md:w-full h-screen md:px-24">
    
    <div class="flex justify-between items-center md:flex-row flex-col gap-20 
                w-full h-auto bg-white border shadow-lg rounded-2xl p-5 mb-8 my-6">
      <div class="flex flex-col md:flex-row gap-2 w-max">
        <div class="w-20 h-20 bg-white overflow-hidden rounded-full shadow-lg border-2 border-primary">
          <img :src="user.avatar"
            class=" object-contain">
        </div>
        <div class="">
          <p class="text-xl font-bold cursor-pointer" @click="router.push('profile/')" 
            v-if="user.userDetails.first_name&&user.userDetails.last_name">
            {{ user.userDetails.first_name.charAt(0).toUpperCase()+user.userDetails.first_name.slice(1) }} 
            {{ user.userDetails.last_name.charAt(0).toUpperCase()+user.userDetails.last_name.slice(1) }}
          </p>
          <p class="mb-2 -mt-2">@{{ user.user }}</p>
          <div class="bg-primary flex justify-center rounded-sm w-max px-1 py-1">
            <p class="text-xs font-bold text-white">Technician</p>
          </div>
        </div>
      </div>

      <div class="flex flex-col items-center">
        <!-- <ModalDTRIn /> -->
        <DTRTimer />
      </div>
    </div>
    <div class="w-full mt-4 mb-14 flex flex-col px-4 md:mx-10">
      <!--:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
      
      <div class="flex my-6" v-for="i in activitystore.filteredActivities">
        <!--:: Main Activities ::-->
          <div class="w-10 h-10 border-2 border-gray-300 rounded-full flex item-center
                      justify-center overflow-hidden mr-2 shadow-sm shadow-black bg-white">
              <img :src="activitystore.setAvatar(i.userpic)" class="object-cover w-full h-full">  
          </div>
          <div>
            <div class="text-gray-800">
                <span class="font-bold">{{i.username}}</span> 
                <span>{{' ' + i.subject }}</span>
            </div>
            <!--Simple-->
            <div class="text-gray-800 text-sm font-thin">
                {{activitystore.humanizeDate(i.created)}}
            </div>

          </div>
        <!--:: :::::::::::: ::-->
      </div>
      



      <!--:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
    </div>
  </div>
</template>

<script setup>
  import ModalDTRIn from '@/components/ModalDTRIn.vue';
  import DTRTimer from '@/components/DTRTimer.vue'
  import router from '../router';
  import { userStore } from '@/stores/user';
  import { dtrStore } from '@/stores/dtr'
  import { activityStore } from '@/stores/activity';
  import { ref, onMounted, onUnmounted } from 'vue';


  const user = userStore()
  const dtrstore = dtrStore()
  const activitystore = activityStore()


  //intitialize dtr
  //dtrstore.loadDTR()

  //load filtered
  const watchActivities = setInterval(() => {
      activitystore.getFilteredActivity("general")
    }, 1000);
  
  onMounted(() => {
    watchActivities
  })
  onUnmounted(() => {
    clearInterval(watchActivities)
  })
</script>

<style>
  .w-activities {
    width: 40rem;
  }

  .w-activity-controls {
    width: 40rem
  }
</style>