import { defineStore } from "pinia";
import router from "../router";
import axios from "axios";
import moment from "moment";
import { userStore } from "./user";

interface Logs {
  month?: string;
}

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
    async loadDTR() {
      if (!this.loaded) {
        const userstore = userStore();
        const current = new Date();
        const all_months = [
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
        ];
        const curr_year = current.getFullYear();
        const curr_month = all_months[current.getMonth()];
        const curr_date = ("0" + current.getDate()).slice(-2);

        if (localStorage.getItem("dtrCurrent")) {
          this.pathForCurrent = localStorage.getItem("dtrCurrent") as string;
        } else {
          localStorage.setItem(
            "dtrCurrent",
            `/get_history/${userstore.user}/${curr_year}/${curr_month}/${curr_date}/`
          );
          this.pathForCurrent = localStorage.getItem("dtrCurrent") as string;
        }
        const response = await axios.get(this.pathForCurrent);
        if (response.status === 200) {
          this.year = response.data.year;
          this.month = response.data.month;
          this.date = response.data.date;
          this.in = response.data.time_in;
          this.as_obj = moment(response.data.time_in_datetime).subtract(
            8,
            "hours"
          );
          this.loaded = true;
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
      const all_months = [
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
      ];
      const userstore = userStore();
      const year = value.split("-")[0];
      const month = all_months[parseInt(value.split("-")[1], 10) - 1];

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
