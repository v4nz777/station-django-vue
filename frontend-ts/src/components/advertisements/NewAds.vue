<template>
  <div class="mx-auto my-3">
    <button
      @click="open = true"
      @mouseover="parentIsHovered = true"
      @mouseout="parentIsHovered = false"
      class="w-32 rounded-md hover:shadow-md flex items-center justify-start px-2 h-9 hover:bg-primary hover:text-white"
    >
      <i
        class="h-6 w-6"
        :class="parentIsHovered ? 'text-white' : 'text-primary'"
        ><MegaphoneIcon
      /></i>
      <h3 class="text-sm font-light">{{ buttonTitle }}</h3>
    </button>
    <teleport to="body">
      <div
        class="bg-slate-800 bg-opacity-50 flex justify-center items-center absolute top-0 right-0 bottom-0 left-0"
        v-if="open"
        ref="outer"
        @click.self="open = false"
      >
        <div
          class="w-max bg-white rounded-md text-start justify-center items-center flex flex-col"
        >
          <div class="flex flex-col justify-center text-center pt-4 w-full">
            <h1 class="font-bold text-gray-500 text-xl">
              Add New Advertisement
            </h1>
            <hr class="mt-4 w-full" />
          </div>
          <div
            id="newads-scroll"
            class="w-full h-96 overflow-y-scroll"
            v-if="display === 'composition'"
          >
            <!-- :Title: -->
            <StringField
              @done="setAdTitle"
              :default="adTitle"
              title="Title"
              type="text"
            />

            <!-- :Advertiser: -->
            <SearchOrAdd
              @done="setAdvertiser"
              :default="adAdvertiser"
              title="Advertiser"
              searchURL="search_advertiser/"
              searchFilter="all"
              end
            />

            <!-- :Type: -->
            <Select
              @done="setAdType"
              :default="adType"
              title="Type"
              :offlineOptions="['local', 'national']"
            />

            <!-- :Contract: -->
            <StringField
              @done="setAdContract"
              :default="adContract"
              :title="adType === 'local' ? 'Contract' : 'IM'"
              queryURL="ads/all"
              queryKey="contract"
              unique
              :end="adType === 'local'"
              type="text"
            />

            <!-- :BO Number: -->
            <StringField
              v-if="adType == 'national'"
              @done="setBO"
              :default="adBO"
              title="BO"
              :end="adType === 'national'"
              type="text"
            />

            <!-- :Ex Deal: -->
            <CheckBox
              @done="setExDeal"
              :default="exDeal"
              title="This is an ex-deal"
            />

            <!-- :Pricing: -->
            <Select
              @done="setAdPricing"
              :default="adPricing"
              title="Pricing"
              :offlineOptions="['package_deal', 'monthly', 'daily']"
            />

            <!-- :Package: -->
            <SearchOrAdd
              v-if="adPricing === 'package_deal'"
              @done="setPackage"
              :default="adPackage"
              title="Package"
              searchURL="load_packages/"
              searchFilter="all"
            />

            <!-- :Amount: -->
            <NumberField
              v-if="adPricing"
              @done="setAdAmount"
              :default="adAmount"
              title="₱ Amount"
              :disabled="adPricing === 'package_deal'"
            />

            <!-- :Broadcast Start: -->
            <DateField
              @done="setAdStart"
              :default="adStart"
              title="Broadcast Start"
            />

            <!-- :Broadcast End: -->
            <DateField
              @done="setAdEnd"
              :default="adEnd"
              title="Broadcast End"
              :match="adStart"
              end
            />

            <!-- :Spots/day: -->
            <NumberField
              @done="setAdSpot"
              :default="adSpot"
              title="Spots/day"
              :disabled="adPricing === 'package_deal'"
            />

            <!-- :Schedule: -->
            <StringToList
              @done="setAdSchedule"
              :default="adSchedule"
              title="Schedule"
              placeholder="ex: 6:10am,7:40am"
              type="text"
              end
              :basedOn="adSpot"
            />

            <!-- :AudioFile: -->
            <UploadZone
              @done="setAudioFiles"
              :default="adAudioFiles"
              title="Audio Upload"
              accepts="audio/*"
            />

            <!-- :MaterialDuration: -->
            <NumberField
              @done="setMaterialDuration"
              :default="adMaterialDuration"
              title="Material Duration"
              placeholder="seconds"
              :disabled="adPricing === 'package_deal'"
              end
            />

            <!-- :Taglines: -->
            <div class="my-3 w-96 text-right">
              <CheckBox
                @done="setAdTaglines"
                :default="adTaglines"
                title="This ad has taglines? (e.g: aob,ss,tc)"
                :disabled="adPricing === 'package_deal'"
              />

              <div v-if="adTaglines" class="my-2 w-full">
                <!-- /AOB/ -->
                <NumberField
                  @done="setAdTagAOBspot"
                  :default="adTagAOBspot"
                  title="AOB spots/day"
                  :disabled="adPricing === 'package_deal'"
                />
                <div class="text-xs text-primary text-center -mt-2 mx-5">
                  leave blank if none
                </div>

                <StringToList
                  @done="setAdTagAOBsched"
                  :default="adAOBsched"
                  title="Schedule"
                  :basedOn="adTagAOBspot"
                  end
                />

                <!-- /TC/ -->
                <NumberField
                  @done="setAdTagTCspot"
                  :default="adTagTCspot"
                  title="TC spots/day"
                  :disabled="adPricing === 'package_deal'"
                />
                <div class="text-xs text-primary text-center -mt-2 mx-5">
                  leave blank if none
                </div>
                <StringToList
                  @done="setAdTagTCsched"
                  :default="adTCsched"
                  title="Schedule"
                  :basedOn="adTagTCspot"
                  end
                />
                <!-- /SS/ -->
                <NumberField
                  @done="setAdTagSSspot"
                  :default="adTagSSspot"
                  title="SS spots/day"
                  :disabled="adPricing === 'package_deal'"
                />
                <div class="text-xs text-primary text-center -mt-2 mx-5">
                  leave blank if none
                </div>
                <StringToList
                  @done="setAdTagSSsched"
                  :default="adSSsched"
                  title="Schedule"
                  :basedOn="adTagSSspot"
                  end
                />
                <!-- /// -->
              </div>
            </div>
            <!-- :Account Executive: -->
            <Select
              @done="setAdAE"
              :default="adAE"
              title="AE"
              :offlineOptions="['office']"
              onlineURL="users/"
              onlineFilter=""
              onlineKey="username"
            />

            <!-- :: -->

            <div class="mx-10 my-5">
              <button
                class="text-white w-full"
                :class="submitEnabled ? 'bg-primary' : 'bg-disabled'"
                :disabled="!submitEnabled"
                @click="display = 'preview'"
              >
                Submit
              </button>
            </div>
          </div>
          <div
            id="newads-scroll"
            class="w-full h-96 overflow-y-scroll"
            v-else-if="display === 'preview'"
          >
            <div class="text-left font-normal flex flex-col px-10">
              <span class="mb-5">Review before submission...</span>
              <span
                >Title:
                <span class="font-light text-primary">{{ adTitle }}</span></span
              >
              <span
                >Advertiser:
                <span class="font-light text-primary">{{
                  adAdvertiser
                }}</span></span
              >
              <span
                >Type:
                <span class="font-light text-primary">{{ adType }}</span></span
              >
              <span
                >{{ adType === "local" ? "Contract: " : "IM: "
                }}<span class="font-light text-primary">{{
                  adContract
                }}</span></span
              >
              <span v-if="adType === 'national'"
                >B.O:
                <span class="font-light text-primary">{{ adBONum }}</span></span
              >
              <span
                >Ex-deal?:
                <span class="font-light text-primary">{{
                  exDeal ? "yes" : "no"
                }}</span></span
              >
              <span
                >Pricing type:
                <span class="font-light text-primary">{{
                  adPricing
                }}</span></span
              >
              <span
                >Amount:
                <span class="font-light text-primary"
                  >₱ {{ adAmount }}</span
                ></span
              >
              <span
                >Starts:
                <span class="font-light text-primary">{{ adStart }}</span></span
              >
              <span
                >Ends:
                <span class="font-light text-primary">{{ adEnd }}</span></span
              >
              <span
                >Spots:
                <span class="font-light text-primary"
                  >{{ adSpot }}/day</span
                ></span
              >
              <span
                >Schedule:
                <span class="font-light text-primary">{{
                  adSchedule
                }}</span></span
              >
              <span
                >Duration:
                <span class="font-light text-primary">{{
                  adMaterialDuration
                }}</span></span
              >
              <span
                >Has Taglines?:
                <span class="font-light text-primary">{{
                  adTaglines ? "yes" : "no"
                }}</span></span
              >
              <div class="flex flex-col" v-if="adTaglines">
                <span
                  >AOB spots:
                  <span class="font-light text-primary">{{
                    adTagAOBspot
                  }}</span></span
                >
                <span
                  >AOB schedule:
                  <span class="font-light text-primary">{{
                    adAOBsched
                  }}</span></span
                >
                <span
                  >TC spots:
                  <span class="font-light text-primary">{{
                    adTagTCspot
                  }}</span></span
                >
                <span
                  >TC schedule:
                  <span class="font-light text-primary">{{
                    adTCsched
                  }}</span></span
                >
                <span
                  >SS spots:
                  <span class="font-light text-primary">{{
                    adTagSSspot
                  }}</span></span
                >
                <span
                  >SS schedule:
                  <span class="font-light text-primary">{{
                    adSSsched
                  }}</span></span
                >
              </div>
              <div>
                Audio Files: <br />
                <ul>
                  <li>
                    <span
                      class="font-light text-primary text-xs"
                      v-for="f in adAudioFiles"
                      :key="f.id"
                      >&nbsp;&nbsp;&nbsp;&nbsp; {{ f.name }}</span
                    >
                  </li>
                </ul>
              </div>
            </div>
            <hr />
            <div class="grid grid-cols-2 space-x-5 px-5 py-5">
              <button
                @click="display = 'composition'"
                class="text-primary hover:bg-secondary hover:shadow-md rounded-md"
              >
                Edit
              </button>
              <button
                @click="submitNewAds"
                class="bg-primary shadow-md text-white hover:bg-primary rounded-md"
              >
                Confirm
              </button>
            </div>
          </div>
        </div>
      </div>
    </teleport>
  </div>
</template>
<script setup>
import MegaphoneIcon from "@/components/icons/MegaphoneIcon.vue";
import { CheckCircleIcon, XCircleIcon } from "@heroicons/vue/solid";
import { ref, onMounted, onUnmounted, watch } from "vue";
import moment from "moment";
import axios from "axios";
import { userStore } from "@/stores/user";

import SearchOrAdd from "@/components/forms/inputs/SearchOrAdd.vue";
import StringField from "@/components/forms/inputs/StringField.vue";
import DateField from "@/components/forms/inputs/DateField.vue";
import StringToList from "@/components/forms/inputs/StringToList.vue";
import NumberField from "@/components/forms/inputs/NumberField.vue";
import Select from "@/components/forms/inputs/Select.vue";
import CheckBox from "@/components/forms/inputs/CheckBox.vue";
import UploadZone from "@/components/forms/inputs/UploadZone.vue";

const props = defineProps({
  buttonTitle: String,
});

const emits = defineEmits(["submitted"])
const open = ref(false);
const parentIsHovered = ref(false);
const outer = ref("");

const display = ref("composition");

const adTitle = ref("");
const setAdTitle = (val) => (adTitle.value = val);

const adType = ref("");
const setAdType = async (val) => (adType.value = val);

const adAdvertiser = ref("");
const setAdvertiser = (val) => (adAdvertiser.value = val);

const adContract = ref("");
const validContract = ref(false);
const setAdContract = (val, validity) => {
  adContract.value = val;
  validContract.value = validity;
};

const adBONum = ref("");
const setBO = (val) => (adBONum.value = val);

const adPricing = ref("");
const setAdPricing = (val) => (adPricing.value = val);

const exDeal = ref(false);
const setExDeal = (val) => (exDeal.value = val);

const adAmount = ref(0);
const setAdAmount = (val) => (adAmount.value = val);

const dateValid = ref(false);
const adStart = ref("");
const setAdStart = (val) => {
  adStart.value = val;
};

const adEnd = ref("");
const setAdEnd = (val, validity) => {
  adEnd.value = val;
  dateValid.value = validity;
};

const totalBroadcastRange = ref("");

const adSpot = ref(0);
const setAdSpot = (val) => (adSpot.value = val);

const adSchedule = ref("");
const setAdSchedule = (val) => (adSchedule.value = val);

const adMaterialDuration = ref(0);
const setMaterialDuration = (val) => (adMaterialDuration.value = val);

const adAudioFiles = ref([]);
const setAudioFiles = (val) => (adAudioFiles.value = [...val]);

const adTaglines = ref(false);
const setAdTaglines = (val) => {
  if (val === false) {
    setAdTagAOBspot(0);
    setAdTagAOBsched("");
    setAdTagTCspot(0);
    setAdTagTCsched("");
    setAdTagSSspot(0);
    setAdTagSSsched("");
  }
  adTaglines.value = val;
};

const adTagAOBspot = ref(0);
const setAdTagAOBspot = (val) => (adTagAOBspot.value = val);

const adAOBsched = ref("");
const setAdTagAOBsched = (val) => (adAOBsched.value = val);

const adTagTCspot = ref(0);
const setAdTagTCspot = (val) => (adTagTCspot.value = val);

const adTCsched = ref("");
const setAdTagTCsched = (val) => (adTCsched.value = val);

const adTagSSspot = ref(0);
const setAdTagSSspot = (val) => (adTagSSspot.value = val);

const adSSsched = ref("");
const setAdTagSSsched = (val) => (adSSsched.value = val);

const adAE = ref("");
const setAdAE = (val) => (adAE.value = val);

//AD PACKAGE SETUP
const adPackage = ref("");
const setPackage = (value) => (adPackage.value = value);

watch(
  () => adPackage.value,
  async (newVal, oldVal) => {
    if (newVal && adPricing.value === "package_deal") {
      const fd = new FormData();
      fd.append("package", adPackage.value);
      const response = await axios.post("get_package", fd);
      const {
        price,
        spots_per_day,
        aob_per_day,
        ss_per_day,
        tc_per_day,
        material_duration,
      } = response.data;

      setAdAmount(price);
      setAdSpot(spots_per_day);
      setMaterialDuration(material_duration);

      if (aob_per_day || ss_per_day || tc_per_day) setAdTaglines(true);
      else setAdTaglines(false);

      if (aob_per_day) setAdTagAOBspot(aob_per_day);

      if (ss_per_day) setAdTagSSspot(ss_per_day);

      if (tc_per_day) setAdTagTCspot(tc_per_day);
    }
  }
);

const submitEnabled = ref(false);
const validityWatcher = setInterval(() => {
  submitEnabled.value =
    adTitle.value &&
    adType.value &&
    adAdvertiser.value &&
    adContract.value &&
    validContract.value &&
    adPricing.value &&
    adAmount.value &&
    adStart.value &&
    adEnd.value &&
    adSpot.value &&
    adSchedule.value &&
    adMaterialDuration.value &&
    adAE.value &&
    dateValid.value;
}, 1000);

const setDefault = () => {
  display.value = "composition";
  adTitle.value = "";
  adType.value = "";
  adAdvertiser.value = "";
  adContract.value = "";
  adBONum.value = "";
  adPricing.value = "";
  exDeal.value = false;
  adAmount.value = 0;
  dateValid.value = false;
  adStart.value = "";
  adEnd.value = "";
  adSpot.value = 0;
  adSchedule.value = "";
  adMaterialDuration.value = 0;
  adAudioFiles.value = [];
  adTaglines.value = false;
  adTagAOBspot.value = 0;
  adAOBsched.value = "";
  adTagTCspot.value = 0;
  adTCsched.value = "";
  adTagSSspot.value = 0;
  adSSsched.value = "";
  adAE.value = "";
  adPackage.value = "";
};

const submitNewAds = async () => {
  const fd = new FormData();
  const userstore = userStore();
  fd.append("uploader", userstore.user);
  fd.append("duration", totalBroadcastRange.value);
  fd.append("title", adTitle.value);
  fd.append("contract", adContract.value);
  fd.append("type", adType.value);
  fd.append("ex_deal", exDeal.value);
  fd.append("pricing", adPricing.value);
  fd.append("amount", adAmount.value);
  fd.append("bo_number", adBONum.value);
  fd.append("advertiser", adAdvertiser.value);
  fd.append("broadcast_start", adStart.value);
  fd.append("broadcast_end", adEnd.value);
  fd.append("ad_spots", adSpot.value);
  fd.append("schedule", adSchedule.value);
  fd.append("has_tagline", adTaglines.value);
  fd.append("aob_spots", adTagAOBspot.value);
  fd.append("aob_sched", adAOBsched.value);
  fd.append("tc_spots", adTagTCspot.value);
  fd.append("tc_sched", adTCsched.value);
  fd.append("ss_spots", adTagSSspot.value);
  fd.append("ss_sched", adSSsched.value);
  fd.append("account_executive", adAE.value);
  fd.append("material_duration", adMaterialDuration.value);
  fd.append("ad_package", adPackage.value);

  adAudioFiles.value.forEach((f) => {
    fd.append("files", f, f.name);
  });

  const response = await axios.post("/new_ads", fd);
  if (response.status === 200) {
    open.value = false;

    emits("submitted",response.data)
    setDefault();
  }
  
  
  

};
onMounted(async () => {
  validityWatcher;
  //packageDealWatcher
});

onUnmounted(() => {
  clearInterval(validityWatcher);
});
</script>

<style>
.w-ads {
  width: 25rem;
}
#newads-scroll::-webkit-scrollbar {
  width: 4px;
  cursor: pointer;
  /*background-color: rgba(229, 231, 235, var(--bg-opacity));*/
}
#newads-scroll::-webkit-scrollbar-track {
  /* background-color: rgba(229, 231, 235, var(--bg-opacity)); */
  cursor: pointer;
  background: #c0b5a0;
}
#newads-scroll::-webkit-scrollbar-thumb {
  cursor: pointer;
  background-color: rgb(109, 79, 4);
  /*outline: 1px solid slategrey;*/
}
</style>
