import { defineStore } from "pinia";
import router from "../router";
import axios from "axios";
import moment from "moment";
import { userStore } from "./user";

const ALL_MONTHS = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
]

export const dtrStore = defineStore({
  id: "dtrStore",

  state: () => ({
    pathForCurrent: "",
    loaded: false,
    year: null,
    month: null,
    date: null,
    in: null,
    out: null,
    timer_ms: 0,
    timed: false,
    as_obj: {},
    dtr_logs: [] as Array<any>,
  }),
  getters: {
    getSeconds: (state: any) => {
      return Math.floor((state.timer_ms / 1000) % 60);
    },
    getMinutes: (state: any) => {
      return Math.floor((state.timer_ms / 1000 / 60) % 60);
    },
    getHours: (state: any) => {
      return Math.floor(state.timer_ms / 1000 / 60 / 60);
    },
    formatLogTimer: (getters: any) => {
      return [
        getters.getHours.toString().padStart(2, "0"),
        getters.getMinutes.toString().padStart(2, "0"),
        getters.getSeconds.toString().padStart(2, "0"),
      ].join(":");
    },
  },
  actions: {
    watchTimer() {
      if (!this.timed && this.as_obj) {
        setInterval(() => {
          const now = moment();
          this.timer_ms = now.diff(this.as_obj);
        }, 1000);
        this.timed = true;
      }
    },
    setPathForCurrent() {
      const userstore = userStore();
      const current = new Date();
      const currentYear = current.getFullYear();
      const currentMonth = ALL_MONTHS[current.getMonth()];
      const currentDate = ("0" + current.getDate()).slice(-2);
      

      if (localStorage.getItem("dtrCurrent")) {
        this.pathForCurrent = localStorage.getItem("dtrCurrent") as string;
      } else {
        localStorage.setItem(
          "dtrCurrent",
          `/get_history/${userstore.user}/${currentYear}/${currentMonth}/${currentDate}/`
        );
        this.pathForCurrent = localStorage.getItem("dtrCurrent") as string;
      }
    },
    async loadDTR() {
      if (!this.loaded) {
        this.setPathForCurrent()
        try{
          const response = await axios.get(this.pathForCurrent);
          if (response.status === 200) {
            this.year = response.data.year;
            this.month = response.data.month;
            this.date = response.data.date;
            this.in = response.data.time_in;
            console.log(response.data.time_in_datetime)
            this.as_obj = moment(response.data.time_in_datetime)
            this.loaded = true;
          }
        }catch(error){
          localStorage.removeItem("dtrCurrent")
          this.pathForCurrent = ""
        }
      }
    },
    async getMonthlyDTRList() {
      const userstore = userStore();
      const response = await axios.get(
        `/get_history/${userstore.user}/${this.year}/${this.month}/`
      );
      this.dtr_logs = response.data.history;
    },
    async getRecentDTRList() {
      const userstore = userStore();
      const response = await axios.get(`/get_history/${userstore.user}/`);
      this.dtr_logs = response.data.history;
    },
    async filterDTR(value: string) {
      const userstore = userStore();
      const year = value.split("-")[0];
      const month = ALL_MONTHS[parseInt(value.split("-")[1], 10) - 1];

      const response = await axios.get(
        `/get_history/${userstore.user}/${year}/${month}/`
      );
      this.dtr_logs = response.data.history;
    },
    clear() {
      this.pathForCurrent = "";
      this.loaded = false;
      this.year = null;
      this.month = null;
      this.date = null;
      this.in = null;
      this.out = null;
      this.timer_ms = 0;
      this.timed = false;
      this.as_obj = {};
      this.dtr_logs = [];
      localStorage.removeItem("dtrCurrent");
    },
  },
});
