<template>
    <div class="h-full w-max flex flex-col px-16 py-14">
        <div class="bg-white text-lg text-center text-gray-500 font-bold px-5 py-2 border-b border-gray-300">
            Daily Time Records
        </div>
        <div class="flex justify-around items-start bg-white text-gray-500 font-normal px-5 py-0 border-b border-gray-300 text-sm">
            <button class="px-2 w-full mx-1 rounded-b-lg flex flex-col text-center"
            @click="selected = 'records'">
                <span class="w-full  mx-auto my-3 px-3 py-2" :class="selected==='records'? 'text-red-500': 'hover:bg-red-100 rounded-md'">Records</span>
                <div class="w-full h-1 rounded-t-md" :class="selected==='records'? 'bg-red-500': 'bg-white'"></div>    
            </button>
            <button class="px-2 w-full mx-1 rounded-b-lg flex flex-col text-center"
            @click="selected = 'export'">
                <span class="w-full mx-auto my-3 px-3 py-2" :class="selected==='export'? 'text-red-500': 'hover:bg-red-100 rounded-md'">Export</span>
                <div class="w-full h-1 rounded-t-md" :class="selected==='export'? 'bg-red-500': 'bg-white'"></div>    
            </button>
        </div>
        
        
        <div class="w-dtr h-screen shadow bg-white overflow-auto red-scroll"
        v-if="selected === 'records'">
            <div class="bg-red-100 border flex justify-center">
                <input @change="sample" v-model="filterValue" id="dtrFilterMonth" type="month" class="my-1 px-2 rounded-md text-red-500 font-thin shadow-lg">
            </div>
            <table class="w-full">
                
                <tbody class="">
                    <tr class="relative text-justify transform scale-100 text-sm py-1 border-b-2 border-red-100 cursor-default">
                        <th class="pl-5 pr-3 whitespace-no-wrap">
                            <div class="text-gray-400">Date</div>
                        </th>
                        <th class="pl-5 pr-3 whitespace-no-wrap">
                            <div class="text-gray-400">Time in</div>
                        </th>
                        <th class="pl-5 pr-3 whitespace-no-wrap">
                            <div class="text-gray-400">Time out</div>
                        </th>
                        <th class="pl-5 pr-3 whitespace-no-wrap">
                            <div class="text-gray-400">Total</div>
                        </th>
                        <th class="pl-5 pr-3 whitespace-no-wrap">
                            <div class="text-gray-400">Overtime</div>
                        </th>
                        <th class="pl-5 pr-3 whitespace-no-wrap">
                            <div class="text-gray-400">Night Diff</div>
                        </th>
                    </tr>
                    <tr class="relative text-justify transform scale-100 text-xs py-1 border-b-2 border-red-100 cursor-default"
                        v-for="item in dtrstore.dtr_logs">
                        <td class="pl-5 pr-3 py-2 whitespace-no-wrap">
                            <div class="leading-5 text-gray-500 font-medium">{{item.month}}</div>
                            <div class="leading-5 text-gray-500 font-medium">{{item.date}}, {{item.year}}</div>
                        </td>
                        <td class="pl-5 pr-3 py-2 whitespace-no-wrap">
                            <div class="leading-5 text-gray-500 font-medium">{{item.time_in_day}}</div>
                            <div class="leading-5 text-gray-500 font-medium">{{item.time_in}}</div>
                        </td>
                        <td class="pl-5 pr-3 py-2 whitespace-no-wrap">
                            <div class="leading-5 text-gray-500 font-medium">{{item.time_out_day}}</div>
                            <div class="leading-5 text-gray-500 font-medium">{{item.time_out}}</div>
                        </td>
                        <td class="pl-5 pr-3 py-2 whitespace-no-wrap">
                            <div class="leading-5 text-gray-500 font-medium">{{item.total}}</div>
                        </td>
                        <td class="pl-5 pr-3 py-2 whitespace-no-wrap">
                            <div class="leading-5 text-gray-500 font-medium">{{item.overtime}}</div>
                        </td>
                        <td class="pl-5 pr-3 py-2 whitespace-no-wrap">
                            <div class="leading-5 text-gray-500 font-medium">{{item.night_diff}}</div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <!--:::::::::::::::: TOGGLE SEPARATOR:::::::::::::::::::::::::::::::::::::::-->
        <div class="w-dtr h-screen shadow bg-red-100 overflow-auto flex justify-center items-center"
        v-else>
            <div class="h-96 w-72 bg-white border shadow-md rounded-lg flex flex-col items-center">
                <div class="w-full text-center pt-2 mb-5">
                    <span class="font-bold text-gray-800">Generate Printable</span>
                    <hr>
                </div>
                <div class="my-5 text-right">
                    <label for="from" class="text-red-500">From: </label>
                    <input type="date" id="from" class="bg-red-300 font-thin text-sm px-2 py-1 shadow-md rounded-sm"
                    v-model="from">
                    <div class="my-5"></div>
                    <label for="to" class="text-red-500">To: </label>
                    <input type="date" id="to" class="bg-red-300 font-thin text-sm px-2 py-1 shadow-md rounded-sm"
                    v-model="to">
                </div>
                <div class="my-5 flex flex-col justify-center items-center">
                    <hr>
                    <Loader v-if="loading"/>
                    <button class="hover:bg-red-500 bg-red-400 text-white text-2xl px-5 py-2 mt-5 rounded-full w-min"
                    @click="generate"
                    v-else>
                        Generate
                    </button>

                    <div class="flex flex-col mt-8 py-1 px-2 hover:bg-white bg-green-500 rounded-sm"
                    v-if="file"
                    @mouseover="dl_btn_hovered = true" @mouseout="dl_btn_hovered = false">
                        
                        <button class="font-light text-white" v-if="!dl_btn_hovered">
                            <i class="block h-4 w-4"><DownloadIcon /></i>
                        </button>
                        <a :href="file" class="font-light text-green-500 text-xs" v-if="dl_btn_hovered">{{fileName}}</a>
                    </div>
                    
                </div>
                
                
                

            </div>
        </div>
    </div>
</template>

<script setup>
    import { dtrStore } from '@/stores/dtr';
    import { userStore } from '@/stores/user';
    import { ref } from 'vue';
    import moment from 'moment';
    import Loader from "@/components/Loader.vue"
    import axios from 'axios';
    import { DownloadIcon } from '@heroicons/vue/outline';

    const dtrstore = dtrStore()
    
    
    const selected = ref("records")
    const filterValue = ref(moment().format("YYYY-MM"))
    const from = ref(null)
    const to = ref(null)

    const file = ref(null)
    const fileName = ref(null)
    const dl_btn_hovered = ref(false)


    setInterval(() => {
        dtrstore.filterDTR(filterValue.value)
    }, 1000);

    const loading = ref(false)

    const generate = async () => {

        if (from.value && to.value){
            loading.value = true
            const userstore = userStore()
            const response = await axios.post(`/generate/dtr/${userstore.user}`,{
                from: from.value,
                to: to.value
            })
            loading.value = false
            file.value = `http://localhost:8000${response.data.file}`
            fileName.value = response.data.title
        }
        
    }



</script>

<style>
    .w-dtr {
        width: 40rem;
    }
    .red-scroll::-webkit-scrollbar {
        width: 4px;
        cursor: pointer;
        /*background-color: rgba(229, 231, 235, var(--bg-opacity));*/

    }
    .red-scroll::-webkit-scrollbar-track {
        /* background-color: rgba(229, 231, 235, var(--bg-opacity)); */
        cursor: pointer;
        background: #c0a0a0;
    }
    .red-scroll::-webkit-scrollbar-thumb {
        cursor: pointer;
        background-color: rgb(224, 73, 73);
        /*outline: 1px solid slategrey;*/
    }
  </style>