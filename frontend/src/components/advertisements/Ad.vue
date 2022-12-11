<template>
    <!-- component -->
    <div :id="'contract-'+ ad.contract" class="bg-white border shadow-md h-full w-full rounded-xl
        hover:shadow-xl overflow-hidden flex flex-col items-center
        py-5 px-5 relative"
        :class="adVersionView.ex_deal?'hover:shadow-orange-300 shadow-orange-100':'hover:shadow-primary shadow-secondary'">
        <span class="flex h-3 w-3 absolute top-1 right-1"
            v-if="codeOrange">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-yellow-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-3 w-3 bg-yellow-500"></span>
        </span>
        <span class="flex h-3 w-3 absolute top-1 right-1"
            v-else-if="codeRed">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-3 w-3 bg-primary"></span>
        </span>
        <div class="w-full">
            <p class="text-center font-bold w-full">{{ad.title.toUpperCase()}}</p>
            <p class="text-xs text-center font-semibold w-full text-primary">#{{ad.contract.toUpperCase()}}</p>
            <p class="text-xs text-center text-gray-700">{{advertiser.name}}</p>
        </div>
        
        <div class="grid grid-cols-2 mt-3 w-full h-full relative">
            <div class="absolute w-full h-full bg-white opacity-80 top-0 bottom-0 left-0 right-0"
                v-if="daysLeft < 0">
            </div>
            
            <div class="h-24 w-24 overflow-hidden rounded-md">
                <img :src="ad.ad_avatar?'http://localhost:8000'+ad.ad_avatar:'/src/assets/ad.png'" class="w-full h-full object-cover">
            </div>


            <div class="flex flex-col justify-center">
                <p class="text-5xl text-center">{{adVersionView.ad_spots}}</p>
                <p class="text-xs text-center">spot{{adVersionView.ad_spots>1?'s':''}} per day</p>
            </div>
        </div>
        <div class="border-t-2 w-full flex justify-end">
            <button class="text-xs font-bold text-right mx-5" 
                :class="adVersionView.ex_deal?'text-orange-500': 'text-primary'"
                @click="open=true">
                view details
            </button>
        </div>
    </div>
    <teleport to='body'>
        <div v-if="open" @click.self="open = false" 
            class="bg-slate-800 bg-opacity-50 flex justify-center items-center absolute top-0 right-0 bottom-0 left-0">
            <div class="bg-white rounded-md w-adcontract h-5/6 px-5 py-5 relative"
                id="mainContract">
                <!-- Options -->
                <div class="w-32 absolute top-2 right-2 flex flex-col">
                    <button class="self-end" @click="toggleAdMenu">
                        <i class="block h-5 w-5"><DotsVerticalIcon /></i>
                    </button>
                    <div class="bg-white w-full h-max flex flex-col items-start shadow-md border"
                        v-if="adMenu"
                        v-click-away="toggleAdMenu">
                        <button class="w-full border-b text-start hover:bg-gray-500 hover:text-white px-2 text-sm"
                                @click="contractView = 'billing'; adMenu=false">Billing</button>
                        <button class="w-full border-b text-start hover:bg-gray-500 hover:text-white px-2 text-sm"
                                @click="contractView = 'edit'; adMenu=false">Edit Contract</button>
                        <button class="w-full border-b text-start hover:bg-gray-500 hover:text-white px-2 text-sm"
                                @click="contractView = 'revisions'; adMenu=false">Revisions</button>

                    </div>
                </div>
                <div class="absolute top-2 left-2 flex flex-col" v-if="contractView !== 'main'">
                    <button class="self-start" @click="contractView = 'main'">
                        <i class="block h-5 w-5"><ArrowNarrowLeftIcon /></i>
                    </button>
                </div>
                <div class="border-b-2 w-full text-center">
                    <h1 class="text-3xl font-bold">{{ad.title.toUpperCase()}}</h1>
                    <p class="text-xs font-bold text-primary">#{{ad.contract}} <span v-if="adVersionView.ex_deal" class="text-orange-500">#EX-DEAL</span></p>
                    <p class="text-sm text-primary">{{advertiser.name}}</p>
                </div>
                <!-- MAIN VIEW -->
                <div class="w-full h-5/6 overflow-y-scroll none-scroll pb-3" v-if="contractView === 'main'">
                    <div class="pb-2">
                        <p class="text-xs text-gray-500">Version {{ad.current_ver}}.0</p>
                    </div>
                    <div class="grid grid-cols-2 gap-2">
                        <div class="h-64 w-64 overflow-hidden rounded-md relative flex shadow">
                            <img v-if="adAvatarUrl" :src="adAvatarUrl" class="w-full h-full object-cover">
                            <img v-else :src="ad.ad_avatar?'http://localhost:8000'+ad.ad_avatar:'/src/assets/ad.png'" class="w-full h-full object-cover">
                            
                            <button class="absolute font-sans text-lg font-black text-white bg-black bg-opacity-30 w-full h-full"
                            v-if="adAvatarChangeMode"
                            @click.self="$refs.adAvatarFile.click">
                                CHANGE
                            </button>
                            <input type="file" class="hidden" ref="adAvatarFile" accept="image/*" @change="uploadAndView" capture>
                            <button v-if="adAvatarUrl" class="absolute top-1 right-1 bg-primary text-white font-bold text-sm px-2 py-1 rounded-md"
                            @click.self="changeAdAvatar">
                                save
                            </button>
                            <button v-else class="absolute top-0 right-0 text-primary hover:text-primary font-bold text-sm px-2 py-1 rounded-md"
                            @click="toggleAdAvatarChangeMode">
                                <i class="block h-6 w-6"><RefreshIcon/></i>
                            </button>


                        </div>
                        <div class="flex flex-col justify-around border-l px-1">
                            <p class="text-sm font-thin my-1">Type: <span class="font-bold">{{ad.type}}</span></p>
                            <p class="text-sm font-thin my-1">BO: <span class="font-bold">{{ad.bo_number}}</span></p>
                            <p class="text-sm font-thin my-1">Starts: <span class="font-bold">{{adVersionView.broadcast_start}}</span></p>
                            <p class="text-sm font-thin my-1">Ends: <span class="font-bold">{{adVersionView.broadcast_end}}</span></p>
                            <p class="text-sm font-thin my-1">Pricing: <span class="font-bold">{{adVersionView.pricing}}</span></p>
                            <p class="text-sm font-thin my-1" v-if="adVersionView.pricing === 'fixed'">Amount: <span class="font-bold">₱{{adVersionView.amount}}</span></p>
                            <p class="text-sm font-thin my-1" v-else>Amount: <span class="font-bold">₱{{adVersionView.amount}}/{{adVersionView.pricing === 'monthly'?'month':'day'}}</span></p>
                            <p class="text-sm font-thin my-1">Airing: <span class="font-bold">{{adVersionView.ad_spots}} spots/day</span></p>
                            <p class="text-sm font-thin my-1">Account Executive: <span class="font-bold">{{ae}}</span>
                            </p>
                        
                        </div>
                    </div>
                    
                    <div class="my-3 px-5 py-2 bg-red-100"
                        v-if="codeRed">
                        <p class="text-sm text-red-500">Will end in {{24 + hoursLeft}} hour{{24+hoursLeft > 1?'s':''}}</p>
                    </div>
                    <div class="my-3 px-5 py-2 bg-orange-100"
                        v-else-if="codeOrange">
                        <p class="text-sm text-orange-500">Will end in {{daysLeft}} day{{daysLeft > 1?'s':''}}! </p>
                    </div>
                    <div class="my-3 px-5 py-2 bg-gray-100"
                        v-else-if="codeBlack">
                        <p class="text-sm text-gray-500">Inactive since {{expiredWhen}}!</p>
                    </div>
                    <div class="my-3 px-5 py-2 bg-green-100 flex justify-between items-center"
                        v-else>
                        <p class="text-sm text-green-500">Up and running</p>
                        <button><i class="flex w-5 h-5 items-center text-green-500"><StackIcon/></i></button>
                    </div>


                    
                    

                    <!-- TAGLINES -->
                    <div class="w-full h-max">
                        <div class="border-b mt-4">
                            <p class="text-center font-bold text-gray-900">Airing Schedule</p>
                        </div>
                        
                        <div class="sched-grid h-max p-5 bg-gray-200 my-3">
                            <div v-for="i in adScheduleList"
                                class="w-max text-sm text-center bg-primary hover:bg-active text-white px-2 py-1 rounded-full m-2 place-self-center">
                                {{i}}
                            </div>
                        </div>
                    </div>
                    <!-- TAGLINES SCHED -->
                    <div class="w-full h-max" v-if="adVersionView.has_tagline">
                        <div class="border-b mt-4">
                            <p class="text-center font-bold text-gray-900">AOB/SS/TC</p>
                        </div>
                        
                        <div class="sched-grid h-max p-5 bg-gray-200 my-3">
        
                            <div v-if="adVersionView.aob_sched" v-for="aob in aobScheduleList"
                                class="relative w-max text-sm text-center bg-primary hover:bg-active text-white px-2 py-1 rounded-full m-2 place-self-center">
                                <div class="tagline h-max w-max px-1 bg-primary text-white-500 flex items-center text-center justify-center">AOB</div>
                                {{aob}}
                            </div>
                            <div  v-if="adVersionView.tc_sched" v-for="tc in tcScheduleList"
                                class="relative w-max text-sm text-center bg-primary hover:bg-active text-white px-2 py-1 rounded-full m-2 place-self-center">
                                <div class="tagline h-max w-max px-1 bg-green-500 text-white-500 flex items-center text-center justify-center">TC</div>
                                {{tc}}
                            </div>
                            <div  v-if="adVersionView.ss_sched" v-for="ss in ssScheduleList"
                                class="relative w-max text-sm text-center bg-primary hover:bg-active text-white px-2 py-1 rounded-full m-2 place-self-center">
                                <div class="tagline h-max w-max px-1 bg-orange-500 text-white-500 flex items-center text-center justify-center">SS</div>
                                {{ss}}
                            </div>
                        </div>
                    </div>
                    <!-- :Materials: -->
                    <div class="w-full">
                        <div class="border-b mt-4">
                            <p class="text-center font-bold text-gray-900">Materials</p>
                        </div>
                        <div class="h-max p-5 bg-gray-200 my-3">
                            <AudioItem v-for="audioFile in adVersionView.files" :id="audioFile" class="w-11/12 mx-auto my-3"/>
                        </div>
                    </div>
                    
                </div>
                <!-- MAIN END -->
                <!-- BILLING VIEW -->
                <AdInvoice 
                    :contract="ad.contract"
                    :amount="adVersionView.amount"
                    :pricing="adVersionView.pricing"
                    :ae="ae"
                    :advertiser="advertiser"
                    v-else-if="contractView === 'billing'"/>
                <!-- BILLING END -->
                <!--EDIT VIEW-->
                <Adedit 
                    :ad="ad"
                    :versionDetails="adVersionView"
                    :advertiser="advertiser"
                    :ae="ae"

                    @saved="contractView = 'main';getVersionView();refresh()"
                    v-else-if="contractView === 'edit'" />
                <!-- EDIT END -->
                <!-- REVISIONS MODE -->
                <AdRevisions
                    :current="ad.current_ver"
                    :versions="ad.versions"
                    :contract="ad.contract"

                    @selected="contractView = 'main';applySelected()"
                    v-else-if="contractView === 'revisions'"/>
                <!-- REVISIONS END -->
            </div>
        </div>
    </teleport>
</template>

<script setup>
    import { reactive, ref, onMounted,onBeforeMount, onUpdated, watch } from 'vue';
    import axios from 'axios';
    import { userStore } from '@/stores/user';
    import AudioItem from '@/components/AudioItem.vue';
    import AdInvoice from "@/components/advertisements/AdInvoice.vue";
    import Adedit from "@/components/advertisements/Adedit.vue"
    import AdRevisions from "@/components/advertisements/AdRevisions.vue"

    import SaveIcon from "@/components/icons/SaveIcon.vue"
    import { DotsVerticalIcon, ReceiptTaxIcon, ArrowNarrowLeftIcon, CogIcon, RefreshIcon } from '@heroicons/vue/solid';
    import moment from 'moment';
    import StackIcon from '@/components/icons/StackIcon.vue';

    const open = ref(false)
    const adMenu = ref(false)
    const contractView = ref("main")
    const toggleAdMenu = ()=> {
        if(adMenu.value === false) adMenu.value = true
        else adMenu.value = false
    }
    const userstore = userStore()
    const props = defineProps({
        ad: Object,
        adscount: Number
    })
    const adVersionView = ref({})

    // Reload version
    const getVersionView = async () => {
        const response = await axios.get(`ad/${props.ad.contract}/${props.ad.current_ver}`)
        adVersionView.value = response.data
       
    }

    const advertiser = ref({})
    const adScheduleList = ref([])
    const aobScheduleList = ref([])
    const tcScheduleList = ref([])
    const ssScheduleList = ref([])

    const daysLeft = ref(0)

    const hoursLeft = ref(0)
    const minutesLeft = ref(0)
    const secondsLeft = ref(0)
    const expiredWhen = ref("")

    const codeRed = ref(false)
    const codeOrange = ref(false)
    const codeBlack = ref(false)


    const howManyDaysLeft = (endDate) => {
        const now = moment()
        const end = moment(endDate)

        daysLeft.value = end.diff(now,"days")
        hoursLeft.value = end.diff(now, "hours") % 24
        minutesLeft.value = end.diff(now, "minutes") % 60
        secondsLeft.value = end.diff(now, "seconds") % 60

        //setOrange
        if(daysLeft.value < 3 && daysLeft.value > 0) {
            codeOrange.value = true
            codeRed.value = false
            codeBlack.value = false
        }
        //setRed
        else if(daysLeft.value <= 1 && daysLeft.value >= 0) {
            codeRed.value = true
            codeOrange.value = false
            codeBlack.value = false
        }
        //setBlack
        else if(daysLeft.value < 0) {
            codeBlack.value = true
            codeRed.value = false
            codeOrange.value = false
        }
        // set OK
        else{
            codeBlack.value = false
            codeRed.value = false
            codeOrange.value = false
        }
        //set WHen is expired
        expiredWhen.value = end.from(now)


    }
    const getSchedules = () => {
        adScheduleList.value = adVersionView.value.schedule.split(",")
        aobScheduleList.value = adVersionView.value.has_tagline&&adVersionView.value.aob_sched? adVersionView.value.aob_sched.split(","):[]
        tcScheduleList.value = adVersionView.value.has_tagline&&adVersionView.value.tc_sched? adVersionView.value.tc_sched.split(","):[]
        ssScheduleList.value = adVersionView.value.has_tagline&&adVersionView.value.ss_sched? adVersionView.value.ss_sched.split(","): []
     
    }
    const ae = ref("")
    const getAE = async () => {
        
        if (adVersionView.value && adVersionView.value.account_executive !== 'office'){
            const response = await axios.get(`user/${adVersionView.value.account_executive}`) 
            ae.value = response.data.first_name.charAt(0).toUpperCase() + response.data.first_name.slice(1) + ' ' + response.data.last_name.charAt(0).toUpperCase() + response.data.last_name.slice(1)
        }else ae.value = "Office"
    }

    const isLoaded = ref(false)
    const getadvertiser = async ()=> {
        const response = await axios.get(`/advertiser/${props.ad.advertiser}`)
        if (response.status  === 200)advertiser.value = response.data
    }

    const refresh = async () => {
        // get advertiser
        await getadvertiser()
    
        await getAE()
        //check days left
        howManyDaysLeft(adVersionView.value.broadcast_end)

        //getSchedules
        getSchedules()
        isLoaded.value = true
    }
    const applySelected = async ()=> {
        await getVersionView()
       
        setTimeout(async () => {
            await refresh()
        }, 1000);
    }

    onMounted(async () => {
       // get ad details by version
       await getVersionView()
       
        setTimeout(async () => {
            await refresh()
        }, 1000);
        
    })

    //refresh if added new ad to list
    watch( ()=> props.adscount, async (newval,oldval)=> {
        if(newval !== oldval){
        await getVersionView()
        await refresh()
        contractView.value = "main"
        }
    })

    // refresh if current version is changed
    watch( ()=> props.ad.current_ver, async (newval,oldval)=> {
        if(newval !== oldval){
            await getVersionView()
            await refresh()
        }
    })



    const adAvatarChangeMode = ref(false)
    const adAvatarFile = ref(null)
    const adAvatarUrl = ref("")
    const toggleAdAvatarChangeMode = ()=> {
        if(adAvatarChangeMode.value)adAvatarChangeMode.value = false
        else adAvatarChangeMode.value = true
    }
    const uploadAndView = ()=> {
        adAvatarUrl.value = URL.createObjectURL(adAvatarFile.value.files[0])
    }
    
    const changeAdAvatar = async ()=> {
        const file = adAvatarFile.value.files[0]
        const fd = new FormData()

        fd.append("contract",props.ad.contract)
        fd.append("ad_avatar",file,file.name)
        
        const response = await axios.post("change_ad_avatar",fd)
        if(response.status === 200){
            
            adAvatarUrl.value = ""
            adAvatarFile.value = null
            adAvatarChangeMode.value = false
        }
    }

    setInterval(() => {
        howManyDaysLeft(adVersionView.value.broadcast_end)
        getSchedules()
    }, 1000);
</script>



<style>
    .sched-grid {
        display: grid;
        grid-gap: 1rem;
        grid-template-columns: repeat(auto-fit, minmax(50px, 1fr));
        /* grid-template-rows: repeat(auto-fit, 208px); */
    }
    .tagline {
        z-index: 1;
        position: absolute;
        top: -5px;
        right:-10px;
        font-size: 0.55rem; 
        line-height: 0.75rem;
        border-radius: 0.25rem;
    }

 
    .none-scroll::-webkit-scrollbar {
        width: 4px;
        cursor: pointer;
        /*background-color: rgba(229, 231, 235, var(--bg-opacity));*/
        display: none;

    }
    .none-scroll::-webkit-scrollbar-track {
        /* background-color: rgba(229, 231, 235, var(--bg-opacity)); */
        cursor: pointer;
        background: #a0b7c0b4;
        display: none;

    }
    .none-scroll::-webkit-scrollbar-thumb {
        cursor: pointer;
        background-color: rgba(73, 121, 224, 0.667);
        display: none;
        /*outline: 1px solid slategrey;*/
    }
    .w-adcontract{
        width: 35rem;
    }
</style>