<template>
  <div class="relative flex items-center justify-center">
    <button @click="toggle" id="menu-opener">
      <i class="block h-9 w-9">
        <MenuIcon />
      </i>
    </button>
    <div
      class="absolute left-0 top-0 bg-white w-max h-max z-10 mt-12 b-border shadow-lg flex flex-col"
      v-if="open"
      v-click-away="toggle"
    >
      <SideBar @afterset="toggle" />

      <hr />
      <div class="flex flex-col pt-12 m-4 justify-center items-center">
        <RouterLink v-if="userstore.user" to="/profile/">
          <div class="flex flex-col justify-center items-center">
            <div
              class="m-1 rounded-full overflow-hidden mx-auto h-9 w-9 flex justify-center items-center border-solid border-yellow-500 border-x-2 border-y-2 shadow-sm shadow-black"
            >
              <img :src="userstore.avatar" class="object-cover w-full h-full" />
            </div>
            <span class="text-gray-900 text-sm font-light"
              >{{ titleCaseSentence(userstore.first_name+' '+userstore.last_name) }}</span
            >
            
          </div>
        </RouterLink>
        <DTRTimer :socket="useActivity.activitySocket"/>
        <hr />
        <Logout />
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { MenuIcon } from "@heroicons/vue/outline";
import Logout from "@/components/LogOut.vue";
import DTRTimer from "@/components/DTRTimer.vue";
import { userStore } from "../stores/user";
import { activityStore } from "@/stores/activity";
import { ref, onMounted, onUnmounted } from "vue";
import SideBar from "@/components/SideBar.vue";
import { titleCaseSentence } from "@/composables/texts";

const userstore = userStore();
const useActivity = activityStore();
const open = ref(false);

const toggle = () => {
  // open if closed -> close if opened
  open.value ? (open.value = false) : (open.value = true);
};

onMounted(() => {
  useActivity.connectToActivitySocket()
})

onUnmounted(() => {
  useActivity.activitySocket?.close()
})
</script>
