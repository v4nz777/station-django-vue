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
const baseURL = location.protocol + "//" + location.hostname + ":8000";

axios.defaults.baseURL = baseURL;
app.component("camera",Camera)
app.use(createPinia());
app.use(router, axios);
app.use(VueClickAway);
app.use(VueCameraLib);



app.mount("#app");
