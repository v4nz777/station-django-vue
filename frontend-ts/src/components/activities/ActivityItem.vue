<template>
    <li class="flex my-6">

          <div class="w-10 h-10 border-2 border-gray-300 rounded-full flex item-center justify-center overflow-hidden mr-2 shadow-sm shadow-black bg-white">
            <img
              :src="activity.userpic?baseURL + activity.userpic:staticAvatar"
              class="object-cover w-full h-full"
            />
          </div>
          <div>
            <div class="text-gray-800">
              <span class="font-bold">{{ activity.username }}</span>
              <span>{{ " " + activity.subject }}</span>
            </div>

            <div class="text-gray-800 text-sm font-thin">
              {{ posted }}
            </div>
          </div>
      
    </li>
</template>

<script setup>
    import { ref, onMounted,onUnmounted } from 'vue';
    import { timeStamp } from "@/composables/datetimes"
    import staticAvatar from "@/assets/avatar.png";
    import axios from 'axios';

    const baseURL = axios.defaults.baseURL

    const props = defineProps({
        activity: Object
    })
    /** A.K.A. Timestamp*/
    const posted = ref(timeStamp(props.activity.created))

    /** Active timer to keep the timestamp updated */
    let postedTimer = setInterval(() => {
        posted.value = timeStamp(props.activity.created)
    }, 5000);

    onMounted(() => {
        postedTimer
    })

    onUnmounted(() => {
        clearInterval(postedTimer)
    })
    
</script>