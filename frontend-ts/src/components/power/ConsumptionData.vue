<template>
  <div
    class="md:w-96 w-full h-max bg-white p-3 shadow-lg rounded-2xl my-5 mx-auto flex justify-between"
  >
    <div>
      <p class="text-lg font-bold mb-2 text-gray-600">{{ dt.complete_date }}</p>
      <p class="text-sm">
        Meter: <span class="text-sky-500 font-bold">{{ datum.meter }}</span>
      </p>
      <p class="text-sm">
        Time: <span class="text-sky-500">{{ dt.complete_time }}</span>
      </p>
    </div>
    <div class="w-max flex items-center justify-center">
      <i v-if="datum.trend === 'up'" class="block w-9 h-9 text-red-500"
        ><TrendingUpIcon
      /></i>
      <i v-else-if="datum.trend === 'down'" class="block w-9 h-9 text-green-500"
        ><TrendingDownIcon
      /></i>
      <i v-else-if="datum.trend === 'same'" class="block w-9 h-9 text-sky-500"
        ><ArrowNarrowRightIcon
      /></i>

      <p v-if="datum.trend === 'up'" class="text-lg text-red-500 font-bold">
        {{ datum.consumed }} kwH
      </p>
      <p
        v-else-if="datum.trend === 'down'"
        class="text-lg text-green-500 font-bold"
      >
        {{ datum.consumed }} kwH
      </p>
      <p
        v-else-if="datum.trend === 'same'"
        class="text-lg text-sky-500 font-bold"
      >
        {{ datum.consumed }} kwH
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import {
  TrendingUpIcon,
  TrendingDownIcon,
  ArrowNarrowRightIcon,
} from "@heroicons/vue/solid";
import moment from "moment";

const props = defineProps({
  datum: Object,
});

const emits = defineEmits(["send"]);

const dt = ref({});

const generateDate = () => {
  const datetime = moment(props.datum.date_time.slice(0, -1));
  dt.value = {
    complete_date: datetime.format("MMMM D ,GGGG"),
    complete_time: datetime.format("h:mm a"),
    year: datetime.format("GGGG"),
    month: datetime.format("MMMM"),
    day: datetime.format("D"),
    hour: datetime.format("h"),
    minute: datetime.format("mm"),
    am_pm: datetime.format("a"),
  };
};

watch(
  () => props.datum,
  (newVal, oldVal) => {
    if (newVal !== oldVal) {
      console.log(newVal);
      generateDate();
      emits("send", { dt: dt.value, kwh_used: newVal.consumed });
    }
  }
);

onMounted(() => {
  generateDate();
  emits("send", { dt: dt.value, kwh_used: props.datum.consumed });
});
</script>
