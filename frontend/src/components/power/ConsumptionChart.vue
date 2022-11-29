<template>
  <div class="w-max h-max bg-white p-3 shadow-lg rounded-lg my-5">
    <Line
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
  import { ref,watch } from 'vue';
  import { Line } from 'vue-chartjs'
  import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement } from 'chart.js'
  
  ChartJS.register(Title, Tooltip, Legend, PointElement, LineElement, CategoryScale, LinearScale)

  const props = defineProps({
      chartId: {
        type: String,
        default: 'bar-chart'
      },
      datasetIdKey: {
        type: String,
        default: 'label'
      },
      width: {
        type: Number,
        default: 600
      },
      height: {
        type: Number,
        default: 400
      },
      cssClasses: {
        default: '',
        type: String
      },
      styles: {
        type: Object,
        default: () => {}
      },
      plugins: {
        type: Object,
        default: () => {}
      },
      data_labels: Object
      
    })
    const chartOptions = {
          responsive: true
    }

 

    const chartData = ref({
        labels: [],
        datasets: [ 
          { label: 'Power Consumption',data:[], backgroundColor: '#ffcc33',borderColor: '#ffcc33' } 
      ]
    })
    
    const updateGraph = (labelsAndData)=> {
      chartData.value = {
        labels: labelsAndData.labels,
        datasets: [ 
          { label: 'Power Consumption',data: labelsAndData.data, backgroundColor: '#ffcc33',borderColor: '#ffcc33' } 
        ]
      }
    }
 
    watch(()=> props.data_labels,(newVal,oldVal)=> {
      updateGraph(newVal)
    },{deep:true})

  </script>