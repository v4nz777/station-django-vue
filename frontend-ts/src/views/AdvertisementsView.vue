<template>
  <div class="flex flex-col w-full px-5 items-center">
    <div class="md:w-full w-screen h-max bg-white rounded-3xl my-5 px-5 py-2 shadow-md">
      <NewAds buttonTitle="Add New" @submitted="appendToAdsList"/>
    </div>
    <div v-if="loaded" class="md:w-full w-screen">
      <div class="w-full h-full">
        <div tag="div"
          v-if="adsList.length"
          class="m-5 mb-10 pb-10 h-max gap-4 grid-auto-cols"
          :class="adsList.length < 4 ? 'w-max' : 'w-full'"
        >
       
          <Ad
            v-for="i in adsList"
            :key="i.id"
            :ad="i"
            :adscount="adsList.length"
          />
        
        </div>
        <div v-else>
          <p class="text-center font-bold">No advertisement yet!</p>
        </div>
      </div>
    </div>
    <div
      v-else
      class="w-full h-screen flex flex-col justify-center items-center"
    >
      <div
        class="w-12 h-12 mx-auto border-4 border-primary rounded-full"
        id="loader"
      ></div>
    </div>
  </div>
</template>
<script setup lang="ts">
import axios from "axios";
import { ref, onMounted, onUnmounted } from "vue";
import Ad from "@/components/advertisements/Ad.vue";
import { dtrStore } from "@/stores/dtr";
import { userStore } from "@/stores/user";
import NewAds from "@/components/advertisements/NewAds.vue";
const filter = ref("all" as string);
const adsList = ref([] as Array<any>);
const loaded = ref(false);
const dtrstore = dtrStore();
const userstore = userStore()
let adSocket:WebSocket;

const getAds = async (_filter:string) => {
  const currentcount = adsList.value.length;
  const response = await axios.get(`ads/${_filter}`);

  if (currentcount !== response.data.length) {
    loaded.value = false;
    adsList.value = [];
  }
  adsList.value = response.data;
  loaded.value = true;
};



const appendToAdsList = (data:any)=> {
  adsList.value = [data,...adsList.value]
  adSocket.send(JSON.stringify({'author':userstore.user,'item':data.id}))
}

onMounted(async () => {
  await getAds(filter.value)
  await dtrstore.loadDTR();
  adSocket = new WebSocket(`${import.meta.env.VITE_DJANGO_SERVER_WEBSOCKET_URL}/sockets/ads`)
  adSocket.addEventListener('message', (e)=> {
    const response = JSON.parse(e.data)
    if(response.author !== userstore.user)adsList.value = [response.message,...adsList.value]
  })
});

onUnmounted(() => {
});
</script>

<style>
.grid-auto-cols {
  display: grid;
  grid-gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(208px, 1fr));
  /* grid-template-rows: repeat(auto-fit, 208px); */
}
.w-ads {
  width: 40rem;
}
.w-ads-controls {
  width: 45rem;
}
</style>
