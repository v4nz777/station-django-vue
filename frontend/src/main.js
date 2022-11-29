
import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import './index.css'
import router from "./router";
import axios from "axios";
import VueClickAway from "vue3-click-away";

const app = createApp(App);
const baseURL = location.protocol + '//' + location.hostname + ':8000'

axios.defaults.baseURL = baseURL

app.use(createPinia())
app.use(router, axios)
app.use(VueClickAway)

app.mount("#app");