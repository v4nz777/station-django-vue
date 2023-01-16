import { createRouter, createWebHistory } from "vue-router";
import { userStore } from "../stores/user";
import ActivitiesView from "@/views/ActivitiesView.vue";
import InventoryView from "@/views/InventoryView.vue";
import RegisterView from "@/views/RegisterView.vue";
import LoginView from "@/views/LoginView.vue";
import ProfileView from "@/views/ProfileView.vue";
import AdvertisementsView from "@/views/AdvertisementsView.vue";
import PowerView from "@/views/PowerView.vue"
import PowerOutageView from "@/views/PowerOutageView.vue"
import TransmitterView from "@/views/TransmitterView.vue"
import BillingView from "@/views/BillingView.vue"
import AdPackageView from "@/views/AdPackageView.vue"




const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "activities",
      component: ActivitiesView,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: "/profile",
      name: "profile",
      component: ProfileView,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: "/inventory",
      name: "inventory",
      component: InventoryView,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: "/register",
      name: "register",
      component: RegisterView,
      meta: {
        requiresGuest: true
      }
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
      meta: {
        requiresGuest: true
      }
    },
    {
      path: "/ads",
      name: "advertisements",
      component: AdvertisementsView,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: "/packages",
      name: "packages",
      component: AdPackageView,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: "/power",
      name: "power",
      component: PowerView,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: "/power_outage",
      name: "power_outage",
      component: PowerOutageView,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: "/transmitter",
      name: "transmitter",
      component: TransmitterView,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: "/billing",
      name: "billing",
      component: BillingView,
      meta: {
        requiresAuth: true
      }
    },
  ],
});


router.beforeEach((to, from) => {
  
  const isLogged = localStorage.getItem("accessToken") && localStorage.getItem("user")

  if (to.meta.requiresAuth && !isLogged) {
    console.warn("🔐Restricted page, you need to login!")
    return {name: "login"}
    
  } else if (to.meta.requiresGuest && isLogged) {
    console.warn("🔐Restricted page, you need to be a guest or logout!")
    return {name: "activities"}
  }
})
export default router;
