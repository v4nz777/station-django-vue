import { defineStore } from "pinia";
import router from "../router";
import axios from "axios";
import staticAvatar from "@/assets/avatar.png";
import { getPosition } from "@/composables/userdetails";
import type { Position } from "@/composables/userdetails";

export interface Person {
  id: number | null;
  username: string | null;
  user: string | null;
  first_name: string | null;
  last_name: string | null;
  email: string | null;
  position: number | null;
  positionSTR: string | undefined;
  gender: string | null;
  address: string | null;
  mobile: string | null;
  telephone: string | null;
  facebook: string | null;
  avatar: any;
  is_in_charge: boolean | null;
  is_logged: boolean | null;
  designation: Array<number> | null;
  in_charge_of: Array<number> | null;
  accessToken: string | null;
  dtrIsLogged: boolean | null;
  userLoaded: boolean | null;
  last_login: string | null;
  key: number | null;
}
export interface Details {
  first_name?: string;
  last_name?: string;
  position?: number;
}

export const userStore = defineStore({
  id: "userStore",

  state: (): Person => {
    return {
      user: "",
      id: null,
      username: "",
      avatar: staticAvatar ?? "",
      accessToken: "",
      dtrIsLogged: false,
      userLoaded: false,
      first_name: "",
      last_name: "",
      email: "",
      position: null,
      gender: "",
      address: "",
      mobile: "",
      telephone: "",
      facebook: "",
      is_in_charge: false,
      is_logged: false,
      designation: [],
      in_charge_of: [],
      last_login: "",
      key: null,
      positionSTR: "",
    };
  },

  actions: {
    initUser() {
      if (localStorage.getItem("accessToken")) {
        console.log("🔑 Acces token detected!");
        // If access token is in local storage, assign to state [accessToken]
        // Set new axios Authorization header
        // set logged username as User
        this.accessToken = localStorage.getItem("accessToken") as string;
        this.user = localStorage.getItem("user") as string;
        axios.defaults.headers.common["Authorization"] =
          "Bearer " + this.accessToken;
        //axios.defaults.headers.common["user"] = this.user
        console.log("🔓 logged!");
      } else {
        // Clear access state
        // Set new Authorization header
        this.accessToken = "";
        axios.defaults.headers.common["Authorization"] = "";
        console.log("🔒 No saved access token detected!");
      }
    },

    logOutUser() {
      console.log(`💻 Removing ${this.user}'s session from this browser...`);
      if (this.user) {
        this.$reset();
        localStorage.clear();

        console.log("🔒 User logged out!");
        router.push("/login");
      } else {
        console.log(
          `❌ ${this.user} failed to log out 😞. Manually clear "localStorage"`
        );
      }
      location.reload();
    },
    async loadUser() {
      if (!this.userLoaded) {
        if (this.user && this.accessToken) {
          const response = await axios.get(`/user/${this.user}`);

          localStorage.setItem("userDetails", JSON.stringify(response.data));
          const userDetails = JSON.parse(
            localStorage.getItem("userDetails") as string
          );
          this.userLoaded = userDetails.userLoaded;
          this.id = userDetails.id;
          this.username = userDetails.username;
          this.first_name = userDetails.first_name;
          this.last_name = userDetails.last_name;
          this.email = userDetails.email;
          this.position = userDetails.position;
          this.gender = userDetails.gender;
          this.address = userDetails.address;
          this.mobile = userDetails.mobile;
          this.telephone = userDetails.telephone;
          this.facebook = userDetails.facebook;
          this.is_in_charge = userDetails.is_in_charge;
          this.is_logged = userDetails.is_logged;
          this.designation = userDetails.designation;
          this.in_charge_of = userDetails.in_charge_of;
          this.last_login = userDetails.last_login;
          this.positionSTR = userDetails.position_str;

          localStorage.setItem("userLoaded", "true");
          this.userLoaded = JSON.parse(
            localStorage.getItem("userLoaded") as string
          );

          localStorage.setItem("dtrIsLogged", response.data.is_logged);
          this.dtrIsLogged = JSON.parse(
            localStorage.getItem("dtrIsLogged") as string
          );
          if (response.data.avatar) {
            localStorage.setItem(
              "avatar",
              axios.defaults.baseURL + response.data.avatar
            );
            this.avatar = localStorage.getItem("avatar") as string;
          }
        } else {
          console.log("❌ No user is logged😞");
        }
      }
    },
    dtrIsLoggedUpdate() {
      this.dtrIsLogged = JSON.parse(
        localStorage.getItem("dtrIsLogged") as string
      );
    },
    async changePic(file: any) {
      const fd = new FormData();
      fd.append("avatar", file, file.name);
      const response = await axios.post(`/change/avatar/${this.user}/`, fd);

      localStorage.setItem(
        "avatar",
        axios.defaults.baseURL + response.data.new_avatar
      );
      setTimeout(() => {
        this.avatar = localStorage.getItem("avatar") as string;
      }, 500);

      return response;
    },
  },
});
