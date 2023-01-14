<template>
  <div class="m-2 w-36 h-36 relative">
    <div
      class="w-36 h-36 overflow-hidden shadow-md relative"
      :class="marked ? 'border-4 border-emerald-500' : ''"
      @click="toggleMark"
    >
      <span
        v-if="equipment.status === 'active'"
        class="absolute top-1 right-1 text-xs shadow-md bg-emerald-500 text-white font-bold px-1 rounded"
        >Active</span
      >
      <span
        v-else-if="equipment.status === 'standby'"
        class="absolute top-1 right-1 text-xs shadow-md bg-gray-500 text-white font-bold px-1 rounded"
        >Standby</span
      >
      <span
        v-else-if="equipment.status === 'test'"
        class="absolute top-1 right-1 text-xs shadow-md bg-yellow-500 text-white font-bold px-1 rounded"
        >Test</span
      >
      <img
        :src="avatar.file ? baseURL + avatar.file : StaticEquipmentPic"
        class="w-full h-full object-cover"
      />
    </div>
    <button
      class="z-10 absolute bottom-custom w-28 h-12 left-2"
      @click="open = true"
    >
      <div
        class="shadow-md w-full h-full bg-sky-500 bg-opacity-80 hover:bg-opacity-100 rounded-lg"
        v-if="equipment.owner === 'mbc'"
      >
        <span class="text-xs text-white px-1 rounded font-semibold">MBC</span>
        <p class="text-sm text-center font-bold rounded-md text-white">
          {{ equipment.name }}
        </p>
      </div>
      <div
        class="shadow-md w-full h-full bg-emerald-500 bg-opacity-80 hover:bg-opacity-100 rounded-lg"
        v-else-if="equipment.owner === 'partner'"
      >
        <span class="text-xs text-white px-1 rounded font-semibold"
          >Partner</span
        >
        <p class="text-sm text-center font-bold rounded-md text-white">
          {{ equipment.name }}
        </p>
      </div>
    </button>

    <teleport to="body">
      <div
        v-if="open"
        @click.self="open = false"
        class="bg-slate-800 bg-opacity-50 flex justify-center items-center absolute top-0 right-0 bottom-0 left-0"
      >
        <div class="bg-white rounded-md w-adcontract h-5/6 px-5 py-5 relative">
          <div class="w-full h-max flex justify-around border-b-2 pb-2">
            <div class="bg-emerald-100 w-80 h-72 relative">
              <img
                v-if="avatar.file"
                :src="
                  eqPicPreview.file
                    ? baseURL + eqPicPreview.file
                    : baseURL + avatar.file
                "
                alt="preview image"
                class="w-full h-full object-contain"
              />
              <img
                v-else
                :src="
                  eqPicPreview.file
                    ? baseURL + eqPicPreview.file
                    : StaticEquipmentPic
                "
                alt="preview image"
                class="w-full h-full object-contain"
              />

              <div
                class="absolute top-1 right-2 text-xs font-bold w-max text-white"
              >
                <div
                  v-if="settingDisplay"
                  class="animate-spin w-5 h-5 border-4 border-x-primary border-y-emerald-200 rounded-full"
                ></div>

                <button
                  v-else
                  class="bg-primary px-2 py-1 rounded-lg w-full hover:bg-primary"
                  v-if="avatar.id !== eqPicPreview.id"
                  @click="setAsDisplay()"
                >
                  <p>Set as display</p>
                </button>
              </div>
            </div>
            <div class="w-max h-max">
              <div
                class="bg-emerald-100 w-32 h-60 overflow-y-scroll none-scroll"
              >
                <div
                  v-for="(img, index) in eqGallery"
                  :key="index"
                  @click="eqPicPreview = img"
                  class="overflow-hidden shadow-md w-12 h-9 my-2 mx-auto"
                  :class="
                    img.id === eqPicPreview.id
                      ? 'border-2 border-primary'
                      : 'hover:border-2 border-yellow-400 hover:shadow-yellow-300'
                  "
                >
                  <img
                    :src="baseURL + img.file"
                    :alt="img.file_name"
                    class="w-full h-full object-cover"
                  />
                </div>
              </div>
              <div class="bg-emerald-100 w-full h-9 relative">
                <input
                  type="file"
                  ref="uploadGallery"
                  accept="image/*"
                  class="hidden"
                  @change="galleryPrepareUpload()"
                  multiple
                />

                <div
                  v-if="uploadTabOpen"
                  class="w-7 h-7 my-2 border-4 border-x-primary border-emerald-300 rounded-full animate-spin mx-auto"
                ></div>
                <button
                  v-else-if="!uploadTabOpen && uploadGalleryList.length"
                  class="my-2 mx-auto text-primary flex justify-center items-center"
                >
                  <i class="block h-8 w-8"><UploadIcon /></i>
                </button>
                <button
                  v-else
                  class="my-2 mx-auto text-primary flex justify-center items-center"
                  @click="$refs.uploadGallery.click"
                >
                  <i class="block h-8 w-8"><UploadIcon /></i>
                </button>

                <div
                  class="absolute bg-white w-72 h-52 right-0 shadow-md grid shadow-emerald-100"
                  v-if="uploadTabOpen"
                >
                  <div
                    class="p-3 small-grid-auto-cols overflow-scroll none-scroll"
                  >
                    <button
                      class="shadow-md w-9 h-12 bg-white border-primary border-2 border-dashed text-primary hover:bg-primary hover:text-white"
                      @click="$refs.uploadGallery.click"
                    >
                      <i class="block h-6 w-6 mx-auto text-center"
                        ><PlusIcon
                      /></i>
                    </button>

                    <div
                      v-for="(imgurl, index) in uploadGalleryListForShow"
                      :key="index"
                      class="overflow-hidden shadow-md w-9 h-12"
                    >
                      <img
                        :src="imgurl"
                        :alt="imgurl.file_name"
                        srcset=""
                        class="w-full h-full object-cover"
                      />
                    </div>
                  </div>
                  <div class="w-full flex">
                    <button
                      class="my-2 mx-auto flex justify-center items-center text-white w-28 px-5 h-9 font-bold shadow-md bg-red-500 hover:bg-red-600"
                      @click="
                        uploadGallery = null;
                        uploadGalleryList = [];
                        uploadGalleryListForShow = [];
                      "
                    >
                      Cancel
                    </button>
                    <button
                      class="my-2 mx-auto flex justify-center items-center text-white w-28 px-5 h-9 font-bold shadow-md"
                      @click="eqGalleryUpload()"
                      :disabled="!uploadGalleryList.length"
                      :class="
                        uploadGalleryList.length
                          ? 'bg-primary hover:bg-emerald-600'
                          : 'bg-emerald-300'
                      "
                    >
                      <p>save</p>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="w-full">
            <div class="w-full my-2 mb-4 bg-emerald-100 px-5" v-if="equipment">
              <p class="text-xl font-bold text-left text-primary">
                {{ equipment.name.toUpperCase() }}
              </p>
            </div>

            <div class="grid grid-cols-2 my-2" v-if="brand.brand_name">
              <div class="px-5">
                <p class="font-bold">Brand:</p>
              </div>
              <div>
                <p>{{ brand.brand_name.toUpperCase() }}</p>
              </div>
            </div>
            <div class="grid grid-cols-2 my-2" v-if="equipment.model">
              <div class="px-5">
                <p class="font-bold">Model:</p>
              </div>
              <div>
                <p>{{ equipment.model.toUpperCase() }}</p>
              </div>
            </div>
            <div class="grid grid-cols-2 my-2" v-if="equipment.serial_no">
              <div class="px-5">
                <p class="font-bold">Serial Number:</p>
              </div>
              <div>
                <p>{{ equipment.serial_no }}</p>
              </div>
            </div>
            <div class="grid grid-cols-2 my-2" v-if="equipment.property_no">
              <div class="px-5">
                <p class="font-bold">Property Number:</p>
              </div>
              <div>
                <p>{{ equipment.property_no }}</p>
              </div>
            </div>

            <div class="grid grid-cols-2 my-2" v-if="equipment.date_acquired">
              <div class="px-5">
                <p class="font-bold">Date Acquired:</p>
              </div>
              <div>
                <p>{{ humanizeDate(equipment.date_acquired) }}</p>
              </div>
            </div>
            <div class="grid grid-cols-2 my-2" v-if="equipment.purchase_cost">
              <div class="px-5">
                <p class="font-bold">Purchase Cost:</p>
              </div>
              <div>
                <p>₱ {{ equipment.purchase_cost }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, onBeforeMount } from "vue";
import { CameraIcon, PlusIcon, UploadIcon } from "@heroicons/vue/solid";
import axios from "axios";
import moment from "moment";
import { userStore } from "@/stores/user";
import StaticEquipmentPic from "@/assets/equipment.png";
const baseURL = axios.defaults.baseURL;
const userstore = userStore();
const open = ref(false);
const props = defineProps({
  id: Number,
  mother: Object,
  batchedItems: Array,
  alled: Boolean,
});
const emits = defineEmits(["mark", "unmark", "notify", "unnotify"]);
const marked = ref(false);
const toggleMark = () => {
  if (props.batchedItems.includes(props.id)) {
    unmark(props.id);
  } else mark(props.id);
};
const mark = (itemID) => {
  emits("mark", itemID);
  marked.value = true;
  // if(marked.value)marked.value = false
  // else marked.value = true
};
const unmark = (itemID) => {
  emits("unmark", itemID);
  marked.value = false;
  // if(marked.value)marked.value = false
  // else marked.value = true
};

const eqPicPreview = ref({});
const avatar = ref({});
const eqGallery = ref([]);
const getPic = async (id) => {
  const response = await axios.get(`equipment_image/${id}`);
  return response.data;
};
const loadEqGallery = async () => {
  eqGallery.value = [];
  await equipment.value.gallery.forEach(async (image) => {
    const asyncImage = await getPic(image);
    eqGallery.value.push(asyncImage);
  });
};

const uploadGallery = ref(null);
const uploadGalleryList = ref([]);
const uploadGalleryListForShow = ref([]);
const galleryPrepareUpload = async () => {
  //Ready for upload
  uploadGalleryList.value = [...(await uploadGallery.value.files)];
  //For show before upload
  uploadGalleryList.value.forEach((item) => {
    const new_ = URL.createObjectURL(item);
    uploadGalleryListForShow.value.push(new_);
  });
};

const eqGalleryUpload = async () => {
  const fd = new FormData();
  fd.append("uploader", userstore.user);
  fd.append("equipment", props.id);
  uploadGalleryList.value.forEach((upload) =>
    fd.append("uploads", upload, upload.name)
  );

  try {
    await axios.post("eq_upload", fd);
    uploadGallery.value = null;
    uploadGalleryList.value = [];
    uploadGalleryListForShow.value = [];
  } catch (e) {
    console.log(e);
  }
};
const settingDisplay = ref(false);
const setAsDisplay = async () => {
  settingDisplay.value = true;
  const response = await axios.put(
    `set_eq_avatar/${props.id}/${eqPicPreview.value.id}`
  );
  if (response.status === 200) {
    setTimeout(() => {
      settingDisplay.value = false;
    }, 2000);
  }
};

const uploadTabOpen = ref(false);
const equipment = ref({});
const getEquipment = async () => {
  const response = await axios.get(`equipment/${props.id}`);
  equipment.value = response.data;
  if (response.data.avatar) avatar.value = await getPic(response.data.avatar);
  if (
    !avatar.value.file &&
    eqGallery.value.length &&
    !eqPicPreview.value.file
  ) {
    eqPicPreview.value = eqGallery.value[0];
  }
};
const group = ref({});
const getGroup = async () => {
  const response = await axios.get(`group/${equipment.value.group}`);
  group.value = response.data;
};
const brand = ref({});
const getBrand = async () => {
  const response = await axios.get(`brand/${equipment.value.brand}`);
  brand.value = response.data;
};
const humanizeDate = (date) => {
  if (date !== "") return moment(date).format("LL");
  else return "";
};
const watchUpdates = setInterval(async () => {
  await getEquipment();
  await getBrand();
  await getGroup();
}, 5000);

const watchUploadTab = setInterval(() => {
  if (uploadGalleryList.value.length) uploadTabOpen.value = true;
  else uploadTabOpen.value = false;
}, 500);

/*
WATCHER - watch for any changes of from gallery
        - if so, update the equipment
*/ watch(
  () => (equipment.value.gallery ? equipment.value.gallery.length : 0),
  async (newval, oldval) => {
    if (oldval !== newval) await loadEqGallery();
  },
  { deep: true }
);

/*
WATCHER - watches avatar is changed from the database
        - if so, update the avatar
*/ watch(
  () => equipment.value.avatar,
  async (newval, oldval) => {
    if (newval !== oldval) {
      if (newval !== null) avatar.value = await getPic(newval);
    }
  },
  { deep: true }
);

/*
WATCHER - if the number of items in group changes, it means there is moved or added.
        - if so, update the item
*/ watch(
  () => props.mother.equipments.length,
  async (newval, oldval) => {
    if (newval !== oldval) {
      await getEquipment();
      setTimeout(async () => {
        await getBrand();
        await getGroup();
        await loadEqGallery();
        if (equipment.value.avatar) {
          eqPicPreview.value = avatar.value;
        } else {
          avatar.value = {};
          eqPicPreview.value = {};
        }
        if (props.batchedItems.includes(props.id)) {
          marked.value = true;
        } else marked.value = false;
      }, 1000);
      watchUpdates;
    }
    if (newval > oldval) {
      emits("notify");
    }
  },
  { deep: true }
);

/*
WATCHER - watch for group checkbox
 */
watch(
  () => props.alled,
  async (newval, oldval) => {
    if (props.alled) {
      marked.value = true;
    } else marked.value = false;
  }
);
/*
WATCHER - watch for status update
*/
watch(
  () => equipment.value.status,
  async (newval, oldval) => {
    if (props.batchedItems.includes(props.id)) {
      marked.value = true;
    } else marked.value = false;
  }
);

onMounted(async () => {
  await getEquipment();
  setTimeout(async () => {
    await getBrand();
    await getGroup();
    await loadEqGallery();
    if (equipment.value.avatar) {
      eqPicPreview.value = avatar.value;
    }
  }, 1000);
  watchUpdates;
  emits("unnotify");
});
onBeforeMount(async () => {
  if (props.batchedItems.includes(props.id)) {
    marked.value = true;
  }
});
onUnmounted(() => {
  clearInterval(watchUpdates);
  clearInterval(watchUploadTab);
});
</script>

<style>
.bottom-custom {
  bottom: -3%;
}
.small-grid-auto-cols {
  display: grid;
  grid-gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(32px, 1fr));
  /* grid-template-rows: repeat(auto-fit, 208px); */
}
</style>
