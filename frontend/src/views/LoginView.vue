<template>
  <div class="min-h-full flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-96 space-y-8 bg-white px-6 py-6 b-border shadow-md rounded-3xl">
      <div>
        <img class="mx-auto h-12 w-auto" src="../assets/stationlogo.jpg" alt="StationLogo" />
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">Log In</h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Or
          {{ ' ' }}
          <RouterLink class="font-medium text-red-600 hover:text-red-500" to="/register">Create Account</RouterLink>
        </p>
      </div>


      <form class="mt-8 space-y-6" @submit.prevent="logUser" method="POST">
        <input type="hidden" name="remember" value="true" />
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="usernameInput" class="sr-only">Username</label>
            <input id="usernameInput" name="username" type="text" required 
                v-model="username"
                class="appearance-none rounded-none relative block w-full px-3 py-2 border
                border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md 
                focus:outline-none focus:ring-red-500 focus:border-red-500 
                focus:z-10 sm:text-sm" placeholder="Username" />
          </div>
          <div>
            <label for="passwordInput" class="sr-only">Password</label>
            <input id="passwordInput" name="password" type="password" required
                v-model="password"
                class="appearance-none rounded-none relative block w-full px-3 py-2 border
                border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md 
                focus:outline-none focus:ring-red-500 focus:border-red-500 
                focus:z-10 sm:text-sm" placeholder="Password" />
          </div>
        </div>


        <div>
          <button type="submit" class="group relative w-full flex justify-center py-2 px-4 border border-transparent
                                      text-sm font-medium rounded-md text-white bg-red-600
                                    hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500">
            <span class="absolute left-0 inset-y-0 flex items-center pl-3">
              <!-- <LockClosedIcon class="h-5 w-5 text-red-500 group-hover:text-red-400" aria-hidden="true" /> -->
            </span>
            Log In
          </button>
        </div>
      </form>
    </div>
  </div>
</template>


<script setup>
    import { ref } from "vue"
    import { userStore } from "@/stores/user"
    import axios from "axios"
    import router from "@/router";
    import { RouterLink } from "vue-router";
    // import { LockClosedIcon } from "@heroicons/vue/solid"

    const username = ref("")
    const password = ref("")
    const store = userStore()

    // Login -> collect access token and save to local storage
    // Axios -> used post method to send API request
    const logUser = async () => {
        const response = await axios.post("/login/", {
            username: username.value, 
            password: password.value 
        })
            localStorage.setItem("accessToken", response.data.access)
            localStorage.setItem("user", username.value)

            store.initUser()
            router.push("/")
    }

    
</script>