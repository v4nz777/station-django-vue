import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import "./style.css";
import router from "./router";
import axios from "axios";
import VueClickAway from "vue3-click-away";
import VueCameraLib from "vue-camera-lib";
import Camera from 'simple-vue-camera';






const app = createApp(App);
console.log(import.meta.env)
axios.defaults.baseURL = import.meta.env.VITE_DJANGO_SERVER_HTTP_URL??location.protocol + "//" + location.hostname + ":8443";
app.component("camera",Camera)
app.use(createPinia());
app.use(router, axios);
app.use(VueClickAway);
app.use(VueCameraLib);



app.mount("#app");