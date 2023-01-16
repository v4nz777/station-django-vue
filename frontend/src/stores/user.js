import { defineStore } from "pinia";
import router from "../router";
import axios from "axios";
import staticAvatar from "@/assets/avatar.png"

export const userStore = defineStore({
    id: "userStore",

    state: () => ({
        user: null,
        avatar: staticAvatar,
        accessToken: null,
        dtrIsLogged: false,
        userLoaded: false,
        userDetails: {}
    }),

    actions: {
        initUser() {
            if(localStorage.getItem("accessToken")) {
                console.log("🔑 Acces token detected!")
                // If access token is in local storage, assign to state [accessToken]
                // Set new axios Authorization header
                // set logged username as User
                this.accessToken = localStorage.getItem("accessToken")
                this.user = localStorage.getItem("user")
                axios.defaults.headers.common["Authorization"] = "Bearer " + this.accessToken
                //axios.defaults.headers.common["user"] = this.user
                console.log("🔓 logged!")
            }
            else {
                // Clear access state
                // Set new Authorization header
                this.accessToken = ""
                axios.defaults.headers.common["Authorization"] = ""
                console.log("🔒 No saved access token detected!")
            }  
        },

        logOutUser() {
            console.log(`💻 Removing ${this.user}'s session from this browser...`)
            if (this.user) {
                this.user = null
                this.accessToken = null
                this.userLoaded = false
                this.userDetails = {}
                localStorage.clear()

                console.log("🔒 User logged out!")
                router.push("/login")
                
            } 
            else {
                console.log(`❌ ${this.user} failed to log out 😞. Manually clear "localStorage"`)
            }
            location.reload(true)
        },
        async loadUser() {
            if (!this.userLoaded) {
        
               if (this.user && this.accessToken) {
              
                    const response = await axios.get(`/user/${this.user}`)
            
                        localStorage.setItem("userDetails", JSON.stringify(response.data))
                        const saveUserDetails = localStorage.getItem("userDetails")
                        this.userDetails = JSON.parse(saveUserDetails)
                
                        localStorage.setItem("userLoaded", true)
                        const saveUserLoaded = localStorage.getItem("userLoaded")
                        this.userLoaded = JSON.parse(saveUserLoaded)
                
                        localStorage.setItem("dtrIsLogged", response.data.is_logged)
                        const dtrIsLogged = JSON.parse(localStorage.getItem("dtrIsLogged"))
                        this.dtrIsLogged = dtrIsLogged
                        if(response.data.avatar){
                            
                            localStorage.setItem("avatar", axios.defaults.baseURL + response.data.avatar)
                            this.avatar = localStorage.getItem("avatar")
                        }
               } else {
                 console.log("❌ No user is logged😞")
               } 
            }
        },
        dtrIsLoggedUpdate() {
            this.dtrIsLogged = JSON.parse(localStorage.getItem("dtrIsLogged"))
        },
        async changePic(file){
            const fd = new FormData()
            fd.append("avatar", file, file.name)
            const response = await axios.post(`/change/avatar/${this.user}/`,fd)

            localStorage.setItem("avatar", axios.defaults.baseURL + response.data.new_avatar)
            setTimeout(() => {
                this.avatar = localStorage.getItem("avatar")  
            }, 500);

            return response
        }
    }
})