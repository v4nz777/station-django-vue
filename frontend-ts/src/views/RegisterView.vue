<script setup lang="ts">
  import { ref } from "vue";
  import axios from "axios";
  import router from "@/router";

  interface Registration {
    username: string;
    email: string;
    password: string;
    confirmation: string;
    gender: string;
    address: string;
    firstName: string;
    lastName: string;
    telephone: string;
    mobile: string;
    facebook: string;
  }

  const registration = ref<Registration>({
    username: "",
    email: "",
    password: "",
    confirmation: "",
    gender: "",
    address: "",
    firstName: "",
    lastName: "",
    telephone: "",
    mobile: "",
    facebook: "",
  });

  const message = ref<string>("");

  async function submitRegistration() {
    try {
      await axios.post("/register/", registration.value);
      router.push("login/");
    } catch (error:any) {
      message.value = error.message;
    }
  }
</script>

<template>
  <div
    class="min-h-full flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8"
  >
    <div
      class="max-w-md w-96 space-y-8 bg-white px-6 py-6 b-border shadow-md rounded-3xl"
    >
      <div>
        <!-- <img class="mx-auto h-12 w-auto" src="../assets/stationlogo.jpg" alt="StationLogo" /> -->
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Register
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Or
          {{ " " }}
          <RouterLink
            class="font-medium text-primary hover:text-primary"
            to="/login"
            >Log In</RouterLink
          >
        </p>
      </div>

      <form
        class="mt-8 space-y-6"
        @submit.prevent="submitRegistration"
        method="POST"
      >
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="username" class="sr-only">Username</label>
            <input
              id="username"
              name="username"
              type="text"
              required
              v-model="registration.username"
              class="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-sm"
              placeholder="Username"
            />
          </div>
        </div>

        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="password" class="sr-only">Password</label>
            <input
              id="password"
              name="password"
              type="password"
              required
              v-model="registration.password"
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-sm"
              placeholder="Password"
            />
          </div>
          <div>
            <label for="confirmation" class="sr-only">Confirm password</label>
            <input
              id="confirmation"
              name="confirmation"
              type="password"
              required
              v-model="registration.confirmation"
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-sm"
              placeholder="Confirm password"
            />
          </div>
        </div>

        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="firstName" class="sr-only">First Name</label>
            <input
              id="firstName"
              name="firstName"
              type="text"
              required
              v-model="registration.firstName"
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-sm"
              placeholder="First name"
            />
          </div>
          <div>
            <label for="lastName" class="sr-only">Last Name</label>
            <input
              id="lastName"
              name="lastName"
              type="text"
              required
              v-model="registration.lastName"
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-sm"
              placeholder="Surname"
            />
          </div>
          <div>
            <label for="gender" class="sr-only">Gender</label>
            <select
              id="gender"
              name="gender"
              required
              v-model="registration.gender"
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-sm"
              placeholder="Gender"
            >
              <option value="" selected disabled>Select gender</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
            </select>
          </div>
        </div>

        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="email" class="sr-only">Email</label>
            <input
              id="email"
              name="email"
              type="email"
              required
              v-model="registration.email"
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-sm"
              placeholder="Email"
            />
          </div>
          <div>
            <label for="facebook" class="sr-only">Facebook</label>
            <input
              id="facebook"
              name="facebook"
              type="text"
              required
              v-model="registration.facebook"
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-sm"
              placeholder="Facebook"
            />
          </div>
          <div>
            <label for="mobile" class="sr-only">Mobile</label>
            <input
              id="mobile"
              name="mobile"
              type="text"
              required
              v-model="registration.mobile"
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-sm"
              placeholder="Mobile number"
            />
          </div>
          <div>
            <label for="address" class="sr-only">Address</label>
            <input
              id="address"
              name="address"
              type="text"
              required
              v-model="registration.address"
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-sm"
              placeholder="Address"
            />
          </div>
        </div>

        <div>
          <button
            type="submit"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-primary hover:bg-primary focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
          >
            <span class="absolute left-0 inset-y-0 flex items-center pl-3">
              <!-- <LockClosedIcon class="h-5 w-5 text-primary group-hover:text-red-400" aria-hidden="true" /> -->
            </span>
            Register
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
