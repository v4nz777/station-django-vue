
<template>
  <main>
    <ModalDTRIn />
    <div class="flex w-activity-controls h-20 bg-white border shadow-lg rounded-2xl p-2 mb-8 my-6 mx-2">
        <NewAds buttonTitle="Advertisement"/>
        <NewPowerOutage/>
    </div>
    <div class="w-activities h-full mt-4 mb-14 flex flex-col md:px-14 px-32">
      <!--:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
      
      <div class="flex my-6"
        :class="i.other.type === 'brownout' 
          || i.other.type === 'ads'
          ? 'p-3 bg-white rounded-2xl border shadow-md':''"
        v-for="i in activitystore.filteredActivities">
        <!--:: Main Activities ::-->
          <div class="w-10 h-10 border-2 border-gray-300 rounded-full flex item-center
                      justify-center overflow-hidden mr-2 shadow-sm shadow-black bg-white">
              <img :src="activitystore.setAvatar(i.userpic)" class="object-cover w-full h-full">  
          </div>
          <div>
            <div class="text-gray-800">
                <span class="font-bold">{{i.username}}</span> 
                <span v-if="i.other.type === 'ads'">{{' ' + i.subject }} <a href="/ads/" class="text-blue-500">#{{i.other.contract}}</a></span>
                <span v-else>{{' ' + i.subject }}</span>
            </div>
 
            <!--Brownouts-->
            <div class="text-gray-800 text-sm font-thin"
                v-if="i.other.type==='brownout'">
                {{activitystore.humanizeDate(i.created)}}
                <hr class="mb-3 mt-1 w-full">
                📅Date: {{activitystore.simplifyDateTimeRange(i.other.interrupted,i.other.restored).date}} <br>
                🔦Interrupted : {{activitystore.simplifyDateTimeRange(i.other.interrupted,i.other.restored).from_time}} |  {{activitystore.simplifyDateTimeRange(i.other.interrupted,i.other.restored).from_day}}<br>
                🔅Restored: {{activitystore.simplifyDateTimeRange(i.other.interrupted,i.other.restored).to_time}} | {{activitystore.simplifyDateTimeRange(i.other.interrupted,i.other.restored).to_day}}<br>
                ⏱️Duration: {{i.other.duration}}
            </div>
            <!--Ads-->
            <div class="text-gray-800 text-sm font-thin"
                v-if="i.other.type==='ads'">
                {{activitystore.humanizeDate(i.created)}}
                <hr class="mb-3 mt-1 w-full">
                <h2 class="text-lg font-bold">{{i.other.title?i.other.title.toUpperCase():null}}</h2>
                <p>Duration: <span class="font-normal">will run for {{i.other.duration}}</span></p>
                <!-- <ul class="my-5">
                  <li v-for="f,index in i.other.audio_files">
                    <AudioItem :id="f" :index="index" />
                  </li>
                </ul> -->
            </div>
            <!--Simple-->
            <div class="text-gray-800 text-sm font-thin"
                v-else>
                {{activitystore.humanizeDate(i.created)}}
            </div>

          </div>
        <!--:: :::::::::::: ::-->
      </div>
      



      <!--:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
    </div>
  </main>
</template>

<script setup>
  import ModalDTRIn from '@/components/ModalDTRIn.vue';
  import { userStore } from '@/stores/user';
  import { dtrStore } from '@/stores/dtr'
  import { activityStore } from '@/stores/activity';
  import NewPowerOutage from '@/components/power/NewPowerOutage.vue';
  import NewAds from '@/components/advertisements/NewAds.vue';
  import AudioItem from '@/components/AudioItem.vue';
  import { ref, onMounted, onUnmounted } from 'vue';

  const userstore = userStore()
  const dtrstore = dtrStore()
  const activitystore = activityStore()

  //intitialize dtr
  dtrstore.loadDTR()

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