import { defineStore } from "pinia";
import router from "../router";
import axios from "axios";
import { userStore } from "./user";
import moment from "moment";
import staticAvatar from "@/assets/avatar.png";
import { openActivitiesConnection } from "@/composables/activities";

interface Activity {
  user: number;
  username: string;
  userpic: string;
  sub_user: string;
  sub_username: string;
  sub_userpic: string;
  created: string;
  subject: string;
  other: object;
}

export const activityStore = defineStore({
  id: "activitystore",
  state: () => ({
    userActivities: [],
    filteredActivities: [] as Array<Activity>,
    activitySocket: undefined as WebSocket|undefined,
  }),
  actions: {
    connectToActivitySocket(){
      this.activitySocket = openActivitiesConnection()
    },
    async getUserActivity() {
      const userstore = userStore();
      const response = await axios.get(`/activity/${userstore.user}`);
      this.userActivities = response.data;
    },
    async getFilteredActivity(filter: string) {
      const response = await axios.get(`/activities/${filter}`);
      this.filteredActivities = response.data;
    },
    humanizeDate(date: string) {
      const humanized = moment(date).fromNow();
      return humanized;
    },
    humanizeUser(username: string) {
      const userstore = userStore();
      if (userstore.user === username) return "You";
      return username;
    },
    simplifyDate(date: string) {
      return moment(date).format("MM/DD/YYYY");
    },
    simplifyDateTimeRange(from: string, to: string) {
      const from_ = moment(from);
      const to_ = moment(to);
      // if (from_.format("MM-DD-YYYY") === to_.format("MM-DD-YYYY")){

      //     return `${from_.format("hh:mm A")} - ${to_.format("hh:mm A")}` //only returns hour -> use simpyfyDate to add date
      // }else{
      //     return `${from_.format("MM/DD/YYYY")} ${from_.format("hh:mm A")} - ${to_.format("MM/DD/YYYY")} ${to_.format("hh:mm A")}`
      // }

      return {
        date: from_.format("MM/DD/YYYY"),
        from_day: from_.format("ddd"),
        to_day: to_.format("ddd"),
        from_time: from_.format("hh:mm A"),
        to_time: to_.format("hh:mm A"),
      };
    },
    setAvatar(avatar: any) {
      if (avatar === "" || avatar === null) return staticAvatar;

      return axios.defaults.baseURL + avatar;
    },
  },
});
