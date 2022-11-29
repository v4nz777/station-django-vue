<template>

    <div class="w-full h-5/6 overflow-y-scroll none-scroll pt-3">
        
        <div class="flex flex-col items-center" v-if="versionsObjects.length > 0">
            <!-- X mean older , Y means newer -->
            <div v-for="batch in versionsObjects"
                class="w-full flex justify-start">
                <div class="w-20 h-full mx-5 grid grid-rows-3">
                    <div class="w-1 mx-auto" :class="batch.y.version === (versionsObjects.length + 1)?'':'bg-gray-200' ">
                    </div>
                    <AdRevisionChangeButton
                        :batch="batch"
                        :current="current"
                        :contract="contract"
                        @selected="selectVersion()"/>

                    <div class="w-1 mx-auto" :class="batch.y.version === 2?'':'bg-gray-200' ">
                    </div>
                </div>
                <div class="text-left flex flex-col justify-center text-gray-500">
                    <p class="text-sm font-bold text-gray-600 py-2">Changes for  v{{batch.y.version}}.0 <span class="text-xs font-sans text-gray-400">({{humanDate(batch.y.added)}})</span></p>

                    <div v-if="batch.x.amount !== batch.y.amount">
                        <!-- Amount -->
                        <p class="text-xs">🌀 {{batch.y.amount > batch.x.amount? 'Increased':'Reduced'}} the amount from ₱{{batch.x.amount}} to ₱{{batch.y.amount}}</p>
                    </div>

                    <div v-if="batch.x.pricing !== batch.y.pricing">
                        <!-- Pricing -->
                        <p class="text-xs">🌀 Changed the pricing from {{batch.x.pricing}} to {{batch.y.pricing}}</p>
                    </div>

                    <div v-if="batch.x.ex_deal !== batch.y.ex_deal">
                        <!-- ExDeal -->
                        <p class="text-xs">🌀 {{batch.y.ex_deal?'Now an EX DEAL':'Not an EX DEAL anymore'}}</p>
                    </div>

                    <div v-if="batch.x.broadcast_start !== batch.y.broadcast_start">
                        <!-- broadcast_start -->
                        <p class="text-xs">🌀 New broadcast start: {{batch.y.broadcast_start}}</p>
                    </div>

                    <div v-if="batch.x.broadcast_end !== batch.y.broadcast_end">
                        <!-- broadcast_end -->
                        <p class="text-xs">🌀 New broadcast end: {{batch.y.broadcast_end}}</p>
                    </div>

                    <div v-if="batch.x.ad_spots !== batch.y.ad_spots">
                        <!-- ad_spots -->
                        <p class="text-xs">🌀 {{batch.y.ad_spots>batch.x.ad_spots?'Added '+(batch.y.ad_spots - batch.x.ad_spots):'Removed '+(batch.x.ad_spots - batch.y.ad_spots)}} spots. New total: {{batch.y.ad_spots}} spots</p>
                    </div>

                    <div v-if="batch.x.schedule !== batch.y.schedule">
                        <!-- schedule -->
                        <p class="text-xs">🌀 Resheduled ad spots </p>
                    </div>

                    <div v-if="batch.x.files.length !== batch.y.files.length">
                        <!-- files -->
                        <p class="text-xs">🌀 {{batch.y.files.length>batch.x.files.length?'Added new audio files':'Removed some audio files'}} </p>
                    </div>

                    <div v-if="batch.x.material_duration !== batch.y.material_duration">
                        <!-- material_duration -->
                        <p class="text-xs">🌀 {{batch.y.material_duration>batch.x.material_duration?
                        ('Increased duration to '+batch.y.material_duration):
                        ('Reduced duration to '+batch.y.material_duration)}} seconds </p>
                    </div>

                    <div v-if="batch.x.has_tagline !== batch.y.has_tagline">
                        <!-- has_tagline -->
                        <p class="text-xs" v-if="batch.y.aob_spots > batch.y.aob_spots">🌀 Added {{batch.y.aob_spots-batch.x.aob_spots}} aob spots</p>
                        <p class="text-xs" v-else-if="batch.y.aob_spots < batch.y.aob_spots">🌀 Removed {{batch.x.aob_spots-batch.y.aob_spots}} aob spots</p>
                        <p class="text-xs" v-if="batch.y.tc_spots > batch.y.tc_spots">🌀 Added {{batch.y.tc_spots-batch.x.tc_spots}} timecheck spots</p>
                        <p class="text-xs" v-else-if="batch.y.tc_spots < batch.y.tc_spots">🌀 Removed {{batch.x.tc_spots-batch.y.tc_spots}} timecheck spots</p>
                        <p class="text-xs" v-if="batch.y.ss_spots > batch.y.ss_spots">🌀 Added {{batch.y.ss_spots-batch.x.ss_spots}} song spon spots</p>
                        <p class="text-xs" v-else-if="batch.y.ss_spots < batch.y.ss_spots">🌀 Removed {{batch.x.ss_spots-batch.y.ss_spots}} song spon spots</p>
                    </div>

                    <div v-if="batch.x.remarks !== batch.y.remarks">
                        <!-- remarks -->
                        <p class="text-xs">🌀 New remark: "{{batch.y.remarks}}" </p>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>
<script setup>
    import { ref, onMounted, onUnmounted } from "vue";
    import moment from 'moment';
    import axios from 'axios';
    import { CheckCircleIcon, XCircleIcon, TrashIcon } from "@heroicons/vue/solid";
    import { userStore } from '@/stores/user';
    import AudioItem from "@/components/AudioItem.vue"
    import AdRevisionChangeButton from "@/components/advertisements/AdRevisionChangeButton.vue"

    const props = defineProps({
        current: Number,
        versions: Array,
        contract: String
    })
    const emits = defineEmits(["selected"])

    const selectVersion = () => emits("selected")

    const humanDate = (date)=> {
        const humadate = moment(date).format("lll")
        return humadate
    }

    const versionsObjects = ref([])

    // Get pair of versions for an ad
    const getEachVersionPair = async(index)=> {
        const indexX = index + 1
        const indexY = indexX + 1
        if(indexX===props.versions.length) return
        const response = await axios.get(`compare/${props.contract}/${indexX}/${indexY}`)
        return response.data
    }

    // Generate List of revisions
    const createVersionsList = async ()=> { 
        let index = 0
        for(const i of props.versions){
            const pair = await getEachVersionPair(index)
            if (pair)versionsObjects.value.push(pair)
            index++
        }
        versionsObjects.value = versionsObjects.value.sort().reverse()
    }

    onMounted(()=> {
        createVersionsList()
       
    })

    
    
</script>