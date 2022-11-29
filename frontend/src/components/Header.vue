<template>
    <header class="h-12">
        <img class="h-11 self-center" src="../assets/stationlogo.png" alt="StationLogo" />
        <nav v-if="userstore.user" class="flex justify-center">
          <Menu class="md:hidden block"/>
          <Logout class="md:block hidden"/>
        </nav>
  </header>
</template>


<script setup>
  import { ref } from 'vue';
  import axios from 'axios';
  import { userStore } from '../stores/user';
  import { dtrStore } from '../stores/dtr';
  import Menu from '@/components/Menu.vue';
  import Logout from '@/components/Logout.vue'


  const dtrstore = dtrStore()
  const userstore = userStore()
  const open = ref(false)

  const logoutToDTR = async () => {
          const response = await axios.put("/dtr_out/", {
            username: userstore.user,
            month: dtrstore.month,
            date: dtrstore.date,
            year: dtrstore.year
          })
          userstore.dtrIsLogged = false

          open.value = false
          userstore.logOutUser()
  }


</script>