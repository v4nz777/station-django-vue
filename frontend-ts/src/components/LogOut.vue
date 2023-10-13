<template>
  <div>
    <button
      @click="open = true"
      class="px-4 py-3 md:text-white md:hover:text-white md:hover:bg-primary text-primary hover:text-white hover:bg-primary"
    >
      Log out
    </button>
    <teleport to="body">
      <div v-if="open">
        <div
          class="bg-slate-800 bg-opacity-50 flex justify-center items-center absolute top-0 right-0 bottom-0 left-0 z-40"
          @click.self="open = false"
        >
          <div class="bg-white px-16 py-14 rounded-md text-center">
            <h1 class="text-xl mb-4 font-bold text-slate-500">Are you sure?</h1>
            <div class="flex">
              <button
                class="bg-primary px-7 py-2 ml-2 rounded-md text-md text-white font-semibold z-50"
                @click.self="logoutToDTR"
              >
                Logout
              </button>
              <button
                class="bg-white px-7 py-2 ml-2 rounded-md text-md text-primary font-semibold border-primary border-x-2 border-y-2"
                @click="open = false"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      </div>
    </teleport>
  </div>
</template>
<script setup>
import { ref } from "vue";
import axios from "axios";
import { userStore } from "../stores/user";
import { dtrStore } from "../stores/dtr";

const dtrstore = dtrStore();
const userstore = userStore();
const open = ref(false);

const logoutToDTR = async () => {
  const response = await axios.put("/dtr_out/", {
    username: userstore.user,
    month: dtrstore.month,
    date: dtrstore.date,
    year: dtrstore.year,
  });
  userstore.dtrIsLogged = false;

  open.value = false;
  userstore.logOutUser();
};
</script>
