<template>
    <div class="flex w-inventory-controls px-5">
        
        
        <div class="w-full">

            <div class="w-full h-max bg-white rounded-3xl my-5 px-5 py-2 shadow-xl shadow-yellow-500 flex">
                <NewTransmitterLog 
                @new="filterLogs(today)"/>
            </div>

            <div class="w-full px-5">
                <TransmitterLogTable
                :logs="logs"
                :filter="today"
                @search="filterLogs"
                />
            </div>

            
        </div>

    </div>
</template>

<script setup>

    import TransmitterLogTable from "@/components/transmitter/TransmitterLogTable.vue"
    import NewTransmitterLog from "@/components/transmitter/NewTransmitterLog.vue"


    import { onMounted } from "vue";
    import { ref } from "vue";
    import axios from "axios";
    import moment from "moment";

    
    const logs = ref([])
    const today = ref("")

    const filterLogs = async (filter)=> {
        const response = await axios.get(`tx_logs/${filter}`)
            logs.value = response.data
    }
    const getLogsToday = async ()=> {
        const now = moment()
        today.value = now.format("YYYY-MM-DD")
        await filterLogs(today.value)
    }


    onMounted(async () => {
        await getLogsToday()
    })

</script>