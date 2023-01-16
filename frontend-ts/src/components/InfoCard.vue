<template>
  <div class="text-left grid place-items-left space-y-4 py-3 px-3 min-w-max">
    <hr />

    <div
      v-if="userstore.first_name"
      class="flex justify-start text-sm"
    >
      <i class="h-6 w-6 mr-3">
        <IdentificationIcon />
      </i>
      {{ userstore.first_name }}
      {{ userstore.last_name }}
    </div>
    <div v-if="userstore.email" class="flex justify-start text-sm">
      <i class="h-6 w-6 mr-3">
        <MailOpenIcon />
      </i>
      <span class="text-gray-700">{{ userstore.email }}</span>
    </div>
    <div
      v-if="userstore.address"
      class="flex justify-start text-sm"
    >
      <i class="h-6 w-6 mr-3">
        <HomeIcon />
      </i>
      <span class="text-gray-700">{{ userstore.address }}</span>
    </div>
    <div
      v-if="userstore.facebook"
      class="flex justify-start text-sm"
    >
      <i class="h-6 w-6 mr-3">
        <GlobeAltIcon />
      </i>
      <span class="text-gray-700"
        >fb.com/{{ userstore.facebook }}</span
      >
    </div>
    <div v-if="userstore.mobile" class="flex justify-start text-sm">
      <i class="h-6 w-6 mr-3">
        <DeviceMobileIcon />
      </i>
      <span class="text-gray-700">{{ userstore.mobile }}</span>
    </div>
    <div
      v-if="userstore.telephone"
      class="flex justify-start text-sm"
    >
      <i class="h-6 w-6 mr-3">
        <PhoneIcon />
      </i>
      <span class="text-gray-700">{{ userstore.telephone }}</span>
    </div>
  </div>
</template>

<script setup>
import { userStore } from "@/stores/user";
import {
  HomeIcon,
  MailOpenIcon,
  GlobeAltIcon,
  DeviceMobileIcon,
  PhoneIcon,
  IdentificationIcon,
} from "@heroicons/vue/outline";

const userstore = userStore();
</script>
