import { defineStore } from "pinia";
import router from "../router";
import axios from "axios";
import { userStore } from "./user";
import moment from "moment";
import staticAvatar from "@/assets/avatar.png"

export const activityStore = defineStore({
    id: "activitystore",
    state: () => ({
        userActivities: null,
        filteredActivities: null
    }),
    actions: {
        async getUserActivity(){
            const userstore = userStore()
            const response = await axios.get(`/activity/${userstore.user}`)
            this.userActivities = response.data

        },
        async getFilteredActivity(filter){
            const response = await axios.get(`/activities/${filter}`)
            this.filteredActivities = response.data
        },
        humanizeDate(date) {
            const humanized = moment(date).subtract(8,"hours").fromNow()
            return humanized
        },
        humanizeUser(username){
            const userstore = userStore()
            if(userstore.user === username) return "You"
            return username
        },
        simplifyDate(date) {
            return moment(date).format("MM/DD/YYYY")
        },
        simplifyDateTimeRange(from,to){
            const from_ = moment(from)
            const to_ = moment(to)
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
                to_time:to_.format("hh:mm A"),

            }
            
        },
        setAvatar(avatar){
            if(avatar === "" | avatar === null) return staticAvatar
     
            return axios.defaults.baseURL + avatar
        },


    }
})