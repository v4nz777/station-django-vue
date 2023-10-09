<template>
  <div class="md:w-full h-screen md:px-24">
    <div
      class="flex justify-between items-center md:flex-row flex-col gap-20 w-full h-auto bg-white border shadow-lg rounded-2xl p-5 mb-8 my-6"
    >
      <div class="flex flex-col md:flex-row gap-2 w-max">
        <div
          class="w-20 h-20 bg-white overflow-hidden rounded-full shadow-lg border-2 border-primary"
        >
          <img :src="useUser.avatar" class="object-cover w-full h-full" />
        </div>
        <div class="">
          <p
            class="text-xl font-bold cursor-pointer"
            @click="router.push('profile/')"
            v-if="useUser.first_name && useUser.last_name"
          >
            {{ titleCaseSentence(useUser.first_name + ' ' + useUser.last_name) }}
          </p>
          <p class="mb-2 -mt-2">@{{ useUser.user }}</p>
          <div
            class="flex justify-center rounded-sm w-max px-1 py-1"
            :class="useUser.regular?'bg-orange-500 shadow-md shadow-orange-300':'bg-sky-300 shadow-md'"
          >
            <p class="text-xs font-bold text-white">
              {{ titleCaseSentence(userPosition.title) }}
            </p>
          </div>
        </div>
      </div>

      <div class="flex flex-col items-center">
        <DTRTimer :socket="useActivity.activitySocket"/>
      </div>
    </div>
    <div class="w-full mt-4 mb-14 flex flex-col px-4 md:mx-10">
      <!--:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
      <TransitionGroup tag="ul">
        <ActivityItem v-for="i,index in activitiesList"
          :activity="i" :key="index"
        />
      </TransitionGroup>
      <!--:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::-->
    </div>
  </div>
</template>

<script lang="ts" setup>
import DTRTimer from "@/components/DTRTimer.vue";
import router from "../router";
import { userStore } from "@/stores/user";
import { activityStore } from "@/stores/activity";
import { onMounted, onUnmounted, ref, watch, onUpdated} from "vue";
import { getPosition } from "@/composables/userdetails";
import type { Position } from "@/composables/userdetails";
import { titleCaseSentence } from "@/composables/texts";
import { activityData, openActivitiesConnection, sendActivity } from '@/composables/activities'
import axios from "axios";
import ActivityItem from "@/components/activities/ActivityItem.vue";
import type { Ref } from "vue";



const activitiesConnection:Ref<WebSocket|null|undefined> = ref(null)
const useUser = userStore();
const useActivity = activityStore();
const userPosition:Ref<Position> = ref({title:'unnasigned'})
const activitiesList = ref([] as Array<any>)


onMounted(async () => {
  const getInitialList = await axios.get(`/activities/general`);
  activitiesList.value = getInitialList.data
  

  useActivity.connectToActivitySocket();

  userPosition.value = await getPosition(useUser.position);
});


onUnmounted(() => {
  useActivity.activitySocket?.close()
});


watch(
  () => useUser.position,
  async (val: any) => {
    userPosition.value = await getPosition(val);
  }
);

watch(()=>activityData.value,(newVal)=> {
  activitiesList.value = [newVal,...activitiesList.value]
})
</script>

<style>
.w-activities {
  width: 40rem;
}

.w-activity-controls {
  width: 40rem;
}


</style>
