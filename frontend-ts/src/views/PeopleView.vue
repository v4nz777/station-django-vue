<template>
  <div class="md:w-3/4 w-screen h-full p-10 flex gap-10 flex-col">
    <TransitionGroup>
      <PosPerson
        v-for="(person, index) in people"
        :key="index"
        :person="person"
        :viewer="useUser.positionSTR"
      />
    </TransitionGroup>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import axios from "axios";
import PosPerson from "@/components/people/PosPerson.vue";
import { userStore } from "@/stores/user";
import type { Person } from "@/stores/user";

const useUser = userStore();

const people = ref([] as Array<Person>);

const getPeople = async () => {
  const response = await axios.get("users/");
  people.value = response.data;
};

onMounted(async () => {
  await getPeople();
});
const watchUpdate = setInterval(async () => await getPeople(), 50000);
onUnmounted(() => {
  clearInterval(watchUpdate);
});
</script>
