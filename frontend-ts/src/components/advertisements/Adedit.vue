<template>
  <div class="w-full h-5/6 overflow-y-scroll none-scroll pt-3">
    <!-- :Title: -->
    <StringField
      @done="setAdTitle"
      :default="adTitle"
      title="Title"
      type="text"
      disabled
    />

    <!-- :Advertiser: -->
    <StringField
      @done="setAdvertiser"
      :default="adAdvertiser"
      title="Advertiser"
      type="text"
      disabled
      end
    />

    <!-- :Type: -->
    <StringField
      @done="setAdType"
      :default="adType"
      title="Type"
      type="text"
      disabled
    />

    <!-- :Contract: -->
    <StringField
      @done="setAdContract"
      :default="adContract"
      :title="adType === 'local' ? 'Contract' : 'IM'"
      queryURL="ads/all"
      queryKey="contract"
      :end="adType === 'local'"
      type="text"
      disabled
    />

    <!-- :BO Number: -->
    <StringField
      v-if="adType == 'national'"
      @done="setBO"
      :default="adBONum"
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
      <div v-if="savingInProgress">
        <div
          class="w-8 h-8 mx-auto border-4 border-primary rounded-full"
          id="loader"
        ></div>
      </div>
      <button v-else class="text-white w-full bg-primary" @click="saveAd">
        Save
      </button>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from "vue";
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

import { openActivitiesConnection, sendActivity } from "@/composables/activities";

let ACTIVITY_SOCKET:WebSocket;


const props = defineProps({
  ad: Object,
  versionDetails: Object,
  advertiser: Object,
  ae: String,
});

const emits = defineEmits(["saved"]);

const adTitle = ref(props.ad?.title);
const setAdTitle = (val:string) => (adTitle.value = val);

const adType = ref(props.ad?.type);
const setAdType = async (val:string) => (adType.value = val);

const adAdvertiser = ref(props.advertiser?.name);
const setAdvertiser = (val:string) => (adAdvertiser.value = val);

const adContract = ref(props.ad?.contract);
const validContract = ref(false);
const setAdContract = (val:string, validity:boolean) => {
  adContract.value = val;
  validContract.value = validity;
};

const adBONum = ref(props.ad?.bo_number);
const setBO = (val:string) => (adBONum.value = val);

const adPricing = ref(props.versionDetails?.pricing);
const setAdPricing = (val:string) => (adPricing.value = val);

const exDeal = ref(props.versionDetails?.ex_deal);
const setExDeal = (val:boolean) => (exDeal.value = val);

const adAmount = ref(props.versionDetails?.amount);
const setAdAmount = (val:number) => (adAmount.value = val);

const dateValid = ref(false);
const adStart = ref(props.versionDetails?.broadcast_start);
const setAdStart = (val:string) => {
  adStart.value = val;
};

const adEnd = ref(props.versionDetails?.broadcast_end);
const setAdEnd = (val:string, validity:boolean) => {
  adEnd.value = val;
  dateValid.value = validity;
};

const totalBroadcastRange = ref("");

const adSpot = ref(props.versionDetails?.ad_spots);
const setAdSpot = (val:number) => (adSpot.value = val);

const adSchedule = ref(props.versionDetails?.schedule);
const setAdSchedule = (val:string) => (adSchedule.value = val);

const adMaterialDuration = ref(props.versionDetails?.material_duration);
const setMaterialDuration = (val:number) => (adMaterialDuration.value = val);

const adAudioFiles = ref(props.versionDetails?.files);
const adAudioForRemoval = ref([] as any)
const setAudioFiles = (val:Array<any>,existing:Array<any>,forRemoval:Array<any>) => {
  adAudioFiles.value = [...val];
  adAudioForRemoval.value = [...forRemoval]
};
const savingInProgress = ref(false)


const adTaglines = ref(props.versionDetails?.has_tagline);
const setAdTaglines = (val:boolean) => {
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

const adTagAOBspot = ref(props.versionDetails?.aob_spots);
const setAdTagAOBspot = (val:number) => (adTagAOBspot.value = val);

const adAOBsched = ref(props.versionDetails?.aob_sched);
const setAdTagAOBsched = (val:string) => (adAOBsched.value = val);

const adTagTCspot = ref(props.versionDetails?.tc_spots);
const setAdTagTCspot = (val:number) => (adTagTCspot.value = val);

const adTCsched = ref(props.versionDetails?.tc_sched);
const setAdTagTCsched = (val:string) => (adTCsched.value = val);

const adTagSSspot = ref(props.versionDetails?.ss_spots);
const setAdTagSSspot = (val:number) => (adTagSSspot.value = val);

const adSSsched = ref(props.versionDetails?.ss_sched);
const setAdTagSSsched = (val:string) => (adSSsched.value = val);

const adAE = ref(props.versionDetails?.account_executive);
const setAdAE = (val:string) => (adAE.value = val);

//AD PACKAGE SETUP
const adPackage = ref(props.versionDetails?.package_name);
const setPackage = (value:string) => (adPackage.value = value);


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
  adAudioForRemoval.value = [];
};

const saveAd = async () => {
  savingInProgress.value = true

  const fd = new FormData();
  const userstore = userStore();
  fd.append("uploader", userstore.user as string);
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

  fd.append("existing_files", props.versionDetails?.files);
  fd.append("files_remove", adAudioForRemoval.value);
  
  adAudioFiles.value.forEach((f:File) => {
    fd.append("files", f, f.name);
  });
  

  const response = await axios.post("/new_ads", fd);
  if (response.status <= 400) {
    console.log("OK")
    setTimeout(() => {
      sendActivity(ACTIVITY_SOCKET,`revised the contract: ${props.ad?.contract}`)
      setDefault();
      savingInProgress.value = false;
      emits("saved");
    }, 1000);
  }
  
  
  

};
onMounted(async () => {
  validityWatcher;
  //packageDealWatcher
  ACTIVITY_SOCKET = openActivitiesConnection()
});

onUnmounted(() => {
  clearInterval(validityWatcher);
  ACTIVITY_SOCKET.close()
});
</script>
