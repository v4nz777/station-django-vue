<template>
  <div class="relative">
    <span
      class="absolute -bottom-7 text-xs bg-black px-2 py-1 z-20 shadow-xl text-white w-max bg-opacity-50"
      v-if="parentIsHovered"
    >
      Add new equipment
    </span>
    <button
      v-if="onMain"
      @click="open = true"
      @mouseover="parentIsHovered = true"
      @mouseout="parentIsHovered = false"
      class="w-max rounded-md hover:shadow-md flex items-center justify-start px-2 h-9 hover:bg-primary hover:text-white"
    >
      <i
        class="h-6 w-6"
        :class="parentIsHovered ? 'text-white' : 'text-primary'"
        ><ArchiveIcon
      /></i>
    </button>
    <button
      v-else
      class="ml-2 border border-dashed border-primary text-primary hover:bg-primary hover:text-white"
      @click="open = true"
    >
      <i class="block h-4 w-4"><PlusSmIcon /></i>
    </button>
  </div>

  <teleport to="body">
    <div
      class="bg-slate-800 bg-opacity-50 flex justify-center items-center absolute top-0 right-0 bottom-0 left-0"
      v-if="open"
      ref="outer"
      @click.self="open = false"
    >
      <!-- start of inside modal -->

      <div
        id="inventory-scroll"
        class="w-inventory-add h-96 bg-white overflow-y-scroll pb-8"
      >
        <h1 class="font-bold m-5 text-center text-primary">
          Add New Equipment
        </h1>
        <hr />
        <!-- Name of equipment -->
        <div class="flex justify-between px-6 my-3">
          <div class="w-32 px-4">
            <p class="text-left text-xs w-full text-primary font-bold p-1">
              Name of equipment
            </p>
          </div>
          <input
            type="text"
            v-model="eqName"
            @keyup="checkName()"
            class="w-64 p-1 text-sm shadow"
            :class="
              takenName
                ? 'bg-red-100 text-red-500 outline-red-500 shadow-red-500'
                : 'bg-secondary text-primary focus-within:outline-primary'
            "
          />
        </div>
        <p class="text-xs text-right text-red-500 px-6 mb-5" v-if="takenName">
          <strong>{{ eqName }}</strong> is taken, try another!
        </p>
        <!-- Brand of equipment -->
        <div class="flex justify-between px-6 my-3">
          <div class="w-32 px-4">
            <p class="text-left text-xs w-full text-primary font-bold p-1">
              Brand
            </p>
          </div>
          <div class="w-64 relative">
            <input
              type="text"
              v-model="eqBrand"
              class="bg-secondary w-full focus-within:outline-primary text-primary p-1 text-sm shadow"
              @keyup="searchBrand()"
            />
            <ul class="w-full h-max bg-white absolute top-7">
              <li
                v-for="(brand, index) in brands"
                :key="index"
                class="hover:bg-primary hover:text-white text-primary border-b"
              >
                <button
                  class="text-xs text-left px-1 w-full h-full"
                  @click.self="
                    eqBrand = brand.brand_name;
                    brands = [];
                  "
                >
                  {{ brand.brand_name }}
                </button>
              </li>
            </ul>
          </div>
        </div>
        <!-- Model of equipment -->
        <div class="flex justify-between px-6 my-3">
          <div class="w-32 px-4">
            <p class="text-left text-xs w-full text-primary font-bold p-1">
              Model
            </p>
          </div>
          <input
            type="text"
            v-model="eqModel"
            class="bg-secondary w-64 focus-within:outline-primary text-primary p-1 text-sm shadow"
          />
        </div>
        <!-- SerialNo of equipment -->
        <div class="flex justify-between px-6 my-3">
          <div class="w-32 px-4">
            <p class="text-left text-xs w-full text-primary font-bold p-1">
              Serial #
            </p>
          </div>
          <input
            type="text"
            v-model="eqSerialNo"
            class="bg-secondary w-64 focus-within:outline-primary text-primary p-1 text-sm shadow"
          />
        </div>
        <!-- PropertyNo of equipment -->
        <div class="flex justify-between px-6 my-3">
          <div class="w-32 px-4">
            <p class="text-left text-xs w-full text-primary font-bold p-1">
              Property #
            </p>
          </div>

          <input
            type="text"
            v-model="eqPropertyNo"
            class="bg-secondary w-64 focus-within:outline-primary text-primary p-1 text-sm shadow"
          />
        </div>
        <!-- Purchase Cost of equipment -->
        <div class="flex justify-between px-6 my-3">
          <div class="w-32 px-4">
            <p class="text-left text-xs w-full text-primary font-bold p-1">
              Purchase cost
            </p>
          </div>
          <input
            type="number"
            v-model="eqCost"
            class="bg-secondary w-64 focus-within:outline-primary text-primary p-1 text-sm shadow"
          />
        </div>

        <!-- Owner -->
        <div class="flex justify-between px-6 my-3">
          <div class="w-32 px-4">
            <p class="text-left text-xs w-full text-primary font-bold p-1">
              Owner
            </p>
          </div>

          <select
            class="bg-secondary w-64 focus-within:outline-primary text-primary p-1 text-sm shadow"
            v-model="eqOwner"
          >
            <option value="partner">Partner</option>
            <option value="mbc">MBC</option>
          </select>
        </div>
        <!-- Status -->
        <div class="flex justify-between px-6 my-3">
          <div class="w-32 px-4">
            <p class="text-left text-xs w-full text-primary font-bold p-1">
              Status
            </p>
          </div>

          <select
            class="bg-secondary w-64 focus-within:outline-primary text-primary p-1 text-sm shadow"
            v-model="eqStatus"
          >
            <option value="active">Active</option>
            <option value="test">Test</option>
            <option value="standby">Standby</option>
          </select>
        </div>
        <!-- Date Acquired -->
        <div class="flex justify-between px-6 my-3">
          <div class="w-32 px-4">
            <p class="text-left text-xs w-full text-primary font-bold p-1">
              Date acquired
            </p>
          </div>
          <input
            type="date"
            v-model="eqAcquired"
            class="bg-secondary w-64 focus-within:outline-primary text-primary p-1 text-sm shadow"
          />
        </div>
        <!-- Group -->

        <div class="flex justify-between px-6 my-3">
          <div class="w-32 px-4">
            <p class="text-left text-xs w-full text-primary font-bold p-1">
              Group
            </p>
          </div>
          <div class="w-64 relative">
            <input
              type="text"
              v-model="eqGroup"
              placeholder="Add to group or create new"
              class="bg-secondary w-full focus-within:outline-primary text-primary p-1 text-sm shadow"
              @keyup="searchGroup()"
            />
            <ul class="w-full h-max bg-white absolute top-7">
              <li
                v-for="group in groups"
                :key="group.id"
                class="hover:bg-primary hover:text-white text-primary border-b"
              >
                <button
                  class="text-xs text-left px-1 w-full h-full"
                  @click.self="
                    eqGroup = group.group_name;
                    groups = [];
                  "
                >
                  {{ group.group_name }}
                </button>
              </li>
            </ul>
          </div>
        </div>

        <!-- SUBMIT -->
        <div class="mt-5 w-full flex justify-around border-t">
          <button
            class="mt-5 w-32 h-max text-white text-sm py-1"
            :class="validForm ? 'bg-primary hover:bg-primary' : 'bg-disabled'"
            :disabled="!validForm"
            @click.once="submitEquipment(true)"
          >
            Save & Exit
          </button>
          <button
            class="mt-5 w-32 h-max text-white text-sm py-1"
            :class="validForm ? 'bg-primary hover:bg-primary' : 'bg-disabled'"
            :disabled="!validForm"
            @click="submitEquipment(false)"
          >
            Save & Add New
          </button>
        </div>
      </div>
      <!-- end of inside modal -->
    </div>
  </teleport>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { ArchiveIcon, PlusSmIcon } from "@heroicons/vue/solid";
import axios from "axios";
import { userStore } from "@/stores/user";

const props = defineProps({
  onMain: Boolean,
  preGroup: String,
});

const userstore = userStore();

const open = ref(false);

const parentIsHovered = ref(false);

const eqName = ref("");
const eqBrand = ref("");
const eqModel = ref("");
const eqSerialNo = ref("");
const eqPropertyNo = ref("");
const eqCost = ref(null);
const eqOwner = ref("");
const eqStatus = ref("");
const eqAcquired = ref("");
const eqGroup = ref("");

const brands = ref([] as Array<any>);
const searchBrand = async () => {
  if (eqBrand.value === "") {
    brands.value = [];
  } else {
    const response = await axios.get(`seach_brand/${eqBrand.value}`);
    brands.value = response.data;
  }
};
const groups = ref([] as Array<any>);
const searchGroup = async () => {
  if (eqGroup.value === "") {
    groups.value = [];
  } else {
    const response = await axios.get(`seach_group/${eqGroup.value}`);
    groups.value = response.data;
  }
};

const takenName = ref(false);
const checkName = async () => {
  if (eqName.value !== "") {
    const response = await axios.get(`check_name/${eqName.value}`);
    takenName.value = response.data.taken;
  } else takenName.value = false;
};

const validForm = ref(false);
const checkForm = () => {
  setInterval(() => {
    validForm.value =
      !takenName.value as any && eqName.value as any && eqOwner.value as any && eqStatus.value as any; 
  }, 1000);
};

onMounted(() => {
  checkForm();
  if (!props.onMain) eqGroup.value = props.preGroup as string;
});

const setDefault = () => {
  eqName.value = "";
  eqBrand.value = "";
  eqModel.value = "";
  eqSerialNo.value = "";
  eqPropertyNo.value = "";
  eqCost.value = null;
  eqOwner.value = "";
  eqStatus.value = "";
  eqAcquired.value = "";
  eqGroup.value = "";
  validForm.value = false;
  takenName.value = false;
  brands.value = [];
};
const setAddNew = () => {
  eqName.value = "";
  eqBrand.value = "";
  eqModel.value = "";
  eqSerialNo.value = "";
  eqPropertyNo.value = "";
  eqCost.value = null;
  eqOwner.value = "";
  eqStatus.value = "";
  eqAcquired.value = "";
  //eqGroup.value = ""
  validForm.value = false;
  takenName.value = false;
  brands.value = [];
};

const submitEquipment = async (andExit:boolean) => {
  const fd = new FormData();
  fd.append("user", userstore.user as string);
  fd.append("name", eqName.value);
  fd.append("brand", eqBrand.value);
  fd.append("model", eqModel.value);
  fd.append("serial_no", eqSerialNo.value);
  fd.append("property_no", eqPropertyNo.value);
  fd.append("purchase_cost", eqCost.value as any);
  fd.append("owner", eqOwner.value);
  fd.append("status", eqStatus.value);
  fd.append("date_acquired", eqAcquired.value);
  fd.append("group", eqGroup.value);

  try {
    await axios.post("add_equipment", fd);
    if (andExit) {
      setDefault();
      open.value = false;
    } else setAddNew();
  } catch (e) {
    console.log(e);
  }
};
</script>
<style>
.w-inventory-add {
  width: 25rem;
}
#inventory-scroll::-webkit-scrollbar {
  width: 4px;
  cursor: pointer;
  /*background-color: rgba(229, 231, 235, var(--bg-opacity));*/
}
#inventory-scroll::-webkit-scrollbar-track {
  /* background-color: rgba(229, 231, 235, var(--bg-opacity)); */
  cursor: pointer;
  background: #a0a1c0;
}
#inventory-scroll::-webkit-scrollbar-thumb {
  cursor: pointer;
  background-color: rgb(112, 88, 39);
  /*outline: 1px solid slategrey;*/
}
</style>
