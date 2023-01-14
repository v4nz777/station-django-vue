<template>
  <div class="w-full md:px-32 h-max p-3 my-5 relative">
    <Line
      class="overflow-x-scroll bg-white shadow-lg rounded-lg relative"
      :chart-options="chartOptions"
      :chart-data="chartData"
      :chart-id="chartId"
      :dataset-id-key="datasetIdKey"
      :plugins="plugins"
      :css-classes="cssClasses"
      :styles="styles"
      :width="width"
      :height="height"
    />
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue";
import { Line } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Chart,
} from "chart.js";
import Hammer from "hammerjs";
import { objectToString } from "@vue/shared";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  PointElement,
  LineElement,
  CategoryScale,
  LinearScale
);

const props = defineProps({
  chartId: {
    type: String,
    default: "bar-chart",
  },
  datasetIdKey: {
    type: String,
    default: "label",
  },
  width: {
    type: Number,
    default: 600,
  },
  height: {
    type: Number,
    default: 400,
  },
  cssClasses: {
    default: "",
    type: String,
  },
  styles: {
    type: Object,
    default: () => {},
  },
  data_labels: Object,
});

const chartOptions = ref({
  responsive: true,
  layout: {
    padding: {
      right: 18,
    },
  },
  scales: {
    x: {
      min: 0,
      max: 12,
    },
    y: {
      beginAtZero: true,
    },
  },

  animations: {
    tension: {
      duration: 1500,
      easing: "linear",
      from: 1,
      to: 0.3,
      loop: false,
    },
  },
});

const plugins = [
  {
    afterDraw: (chart, args) => {
      const {
        ctx,
        canvas,
        chartArea: { left, right, top, bottom, width, height },
      } = chart;

      const hammer = new Hammer(canvas);
      hammer.on("swipe", (event) => {
        // Object.assign(chartOptions)
        if (event.direction === 2) {
          //swipeleft

          if (
            chart.scales.x.max + 1 >=
            chartData.value.datasets[0].data.length
          ) {
            return;
          } else {
            chartOptions.value.scales.x.min = chart.scales.x.min + 1;
            chartOptions.value.scales.x.max = chart.scales.x.max + 1;
          }
        } else if (event.direction === 4) {
          //swipe right
          if (chart.scales.x.min + 1 <= 1) {
            return;
          } else {
            chartOptions.value.scales.x.min = chart.scales.x.min - 1;
            chartOptions.value.scales.x.max = chart.scales.x.max - 1;
          }
        }
      });
    },
  },
];

const chartData = ref({
  labels: [],
  datasets: [
    {
      label: "Power Consumption",
      data: [],
      backgroundColor: "#ffcc33",
      borderColor: "#ffcc33",
    },
  ],
});

const updateGraph = (labelsAndData) => {
  chartData.value = {
    labels: labelsAndData.labels,
    datasets: [
      {
        label: "Power Consumption",
        data: labelsAndData.data,
        backgroundColor: "#ffcc33",
        borderColor: "#ffcc33",
      },
    ],
  };
};

watch(
  () => props.data_labels,
  (newVal, oldVal) => {
    updateGraph(newVal);
  },
  { deep: true }
);
</script>
