<template>
  <tr class="m-2 w-full h-max relative text-sm hover:bg-primary hover:text-white" 
      :class="marked ? 'border-2 border-emerald-500' :''">
    <td><input type="checkbox" @change="toggleMark"></td>
    <td>{{ equipment.name?toTitleCase(equipment.name):'' }}</td>
    <td>{{ brand.brand_name?toTitleCase(brand.brand_name):'' }}</td>
    <td>{{ equipment.model?.toUpperCase() }}</td>
    <td>{{ equipment.serial_no }}</td>
    <td>{{ equipment.owner?toTitleCase(equipment.owner):'' }}</td>
    <td>{{ equipment.property_no }}</td>
    <td>{{ equipment.status?toTitleCase(equipment.status):'' }}</td>
    <td class="cursor-pointer" @click="open=true">open</td>


    <teleport to="body">
      <div
        v-if="open"
        @click.self="open = false"
        class="bg-slate-800 bg-opacity-50 flex justify-center items-center absolute top-0 right-0 bottom-0 left-0"
      >
        <div class="bg-white w-screen rounded-md h-5/6 px-5 py-5 relative">
          <div class="w-full h-max flex justify-between border-b-2 pb-2 gap-2">
            <div class="bg-black w-full h-72 relative">
              <div v-if="camera&&!uploadGalleryList.length " class="absolute w-full h-full bg-black">
                <WebCamUI fullscreenState @photoTaken="snapshot" @exitFullscreen="camera=false"/>
              </div>
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
            <div class="w-32 h-full flex flex-col">
              <div
                class="bg-gray-300 w-full h-60 overflow-y-scroll none-scroll">
                <div
                  v-for="(img, index) in eqGallery"
                  :key="index"
                  @click="eqPicPreview = img"
                  class="overflow-hidden shadow-md w-12 h-9 my-2 mx-auto"
                  :class="
                    img.id === eqPicPreview.id
                      ? 'border-2 border-primary'
                      : 'hover:border-2 border-yellow-400 hover:shadow-yellow-300'">
                  <img
                    :src="baseURL + img.file"
                    :alt="img.file_name"
                    class="w-full h-full object-cover"/>
                </div>
              </div>
              <div class="bg-emerald-100 w-full h-9 relative flex justify-around">
                <input
                  type="file"
                  ref="uploadGallery"
                  accept="image/*"
                  class="hidden"
                  @change="galleryPrepareUpload()"
                  multiple/>

                <div v-if="uploadTabOpen"
                  class="w-7 h-7 my-2 border-4 border-x-primary border-emerald-300 rounded-full animate-spin mx-auto">
                </div>
                <button
                  v-else-if="!uploadTabOpen && uploadGalleryList.length"
                  class="my-2 mx-auto text-primary flex justify-center items-center">
                  <i class="block h-7 w-7"><UploadIcon /></i>
                </button>
                <button
                  v-else
                  class="w-full my-2 mx-auto text-primary flex justify-center items-center"
                  @click="($refs.uploadGallery as HTMLInputElement).click">
                  <i class="block h-7 w-7"><UploadIcon /></i>
                </button>
                <div class="my-2 w-full">
                  <button
                    class="mx-auto text-primary flex justify-center items-center"
                    @click="camera = true">
                    <i class="block h-7 w-7"><CameraIcon /></i>
                  </button>
                  
                </div>

                <div
                  class="absolute bg-white w-72 h-52 right-0 shadow-md grid shadow-emerald-100"
                  v-if="uploadTabOpen">
                  <div
                    class="p-3 small-grid-auto-cols overflow-scroll none-scroll">
                    <button
                      class="shadow-md w-9 h-12 bg-white border-primary border-2 border-dashed text-primary hover:bg-primary hover:text-white"
                      @click="($refs.uploadGallery as HTMLInputElement).click">
                      <i class="block h-6 w-6 mx-auto text-center">
                        <PlusIcon/>
                      </i>
                    </button>

                    <div
                      v-for="(imgurl, index) in uploadGalleryListForShow"
                      :key="index"
                      class="overflow-hidden shadow-md w-9 h-12">
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
                        uploadGalleryListForShow = [];">
                      Cancel
                    </button>
                    <button
                      class="my-2 mx-auto flex justify-center items-center text-white w-28 px-5 h-9 font-bold shadow-md"
                      @click="eqGalleryUpload()"
                      :disabled="!uploadGalleryList.length"
                      :class="
                        uploadGalleryList.length
                          ? 'bg-primary hover:bg-emerald-600'
                          : 'bg-emerald-300'">
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
  </tr>
</template>

<script lang="ts" setup>
import { ref, onMounted, onUnmounted, watch, onBeforeMount } from "vue";
import { CameraIcon, PlusIcon, UploadIcon } from "@heroicons/vue/solid";
import axios from "axios";
import moment from "moment";
import { userStore } from "@/stores/user";
import StaticEquipmentPic from "@/assets/equipment.png";
import { WebCamUI } from "vue-camera-lib";
import {toTitleCase} from "@/composables/texts"

const baseURL = axios.defaults.baseURL;
const userstore = userStore();
const open = ref(false);
const camera = ref(false)
const props = defineProps({
  id: Number,
  mother: Object,
  batchedItems: Array,
  alled: Boolean,
});
const emits = defineEmits(["mark", "unmark", "notify", "unnotify","dbTouched"]);
const marked = ref(false);
const toggleMark = () => {
  if (props.batchedItems?.includes(props.id)) {
    unmark(props.id);
  } else mark(props.id);
};
const mark = (itemID:any) => {
  emits("mark", itemID);
  marked.value = true;
  // if(marked.value)marked.value = false
  // else marked.value = true
};
const unmark = (itemID:any) => {
  emits("unmark", itemID);
  marked.value = false;
  // if(marked.value)marked.value = false
  // else marked.value = true
};

const eqPicPreview = ref({} as any);
const avatar = ref({} as any);
const eqGallery = ref([] as any);
const getPic = async (id:any) => {
  const response = await axios.get(`equipment_image/${id}`);
  return response.data;
};
const loadEqGallery = async () => {
  eqGallery.value = [];
  await equipment.value.gallery.forEach(async (image:any) => {
    const asyncImage = await getPic(image) as any;
    eqGallery.value.push(asyncImage);
  });
};

const uploadGallery = ref<HTMLInputElement|null>(null);
const uploadGalleryList = ref([] as Array<any>);
const uploadGalleryListForShow = ref([] as Array<any>);
const galleryPrepareUpload = async () => {
  //Ready for upload
  uploadGalleryList.value = [...uploadGallery.value?.files??[]as any];
  //For show before upload
  uploadGalleryList.value.forEach((item:any) => {
    const new_ = URL.createObjectURL(item);
    uploadGalleryListForShow.value.push(new_);
  });
};

const eqGalleryUpload = async () => {
  const fd = new FormData();
  fd.append("uploader", userstore.user as string);
  fd.append("equipment", props.id as any);
  uploadGalleryList.value.forEach((upload) =>
    fd.append("uploads", upload, upload.name)
  );

  try {
    await axios.post("eq_upload", fd);
    uploadGallery.value = null;
    uploadGalleryList.value = [];
    uploadGalleryListForShow.value = [];
    camera.value = false
    emits("dbTouched")
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
const equipment = ref({} as any);
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
const brand = ref({} as any);
const getBrand = async () => {
  const response = await axios.get(`brand/${equipment.value.brand}`);
  brand.value = response.data;
};
const humanizeDate = (date:any) => {
  if (date !== "") return moment(date).format("LL");
  else return "";
};

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
  () => props.mother?.equipments.length,
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
        if (props.batchedItems?.includes(props.id)) {
          marked.value = true;
        } else marked.value = false;
      }, 1000);
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
  async () => {
    if (props.batchedItems?.includes(props.id)) {
      marked.value = true;
    } else marked.value = false;
  }
);


const snapshot = async (data:any)=> {
  const blob = await data.blob as Blob
  const datetime = moment().format("MM_DD_YYYY_HH_mm_ss")
  const file = new File([blob],`snap_${datetime}.jpg`,{
    type:blob.type
  })
  uploadGalleryList.value.push(file)
  uploadGalleryListForShow.value.push(data.image_data_url);
}

onMounted(async () => {
  // await getEquipment();
  // setTimeout(async () => {
  //   await getBrand();
  //   await getGroup();
  //   await loadEqGallery();
  //   if (equipment.value.avatar) {
  //     eqPicPreview.value = avatar.value;
  //   }
  // }, 1000);
  await getEquipment();
  await getBrand();
  await getGroup();
  emits("unnotify");
});
onBeforeMount(async () => {
  if (props.batchedItems?.includes(props.id)) {
    marked.value = true;
  }
});
onUnmounted(() => {
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
