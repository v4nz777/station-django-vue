<template>
    <div class="w-full h-5/6 overflow-y-scroll none-scroll pt-3">
        
        <div class="bg-gray-200 w-full h-max text-sm font-thin p-5 grid grid-cols-3">
            <div class="mb-3 flex flex-col justify-between border-r-2 mr-3">
                <div class="mb-2">
                    <p class="font-bold text-primary mr-5">Create invoice for: </p><p class="text-primary font-sm">contract #{{contract}}</p>
                </div>
                <div class="mb-2">
                    <p class="font-bold text-primary mr-5">Pricing: <span class="bg-green-500 rounded-full px-2 py-1 text-xs text-white">{{pricing}}</span> </p><p class="text-primary font-sm">₱{{amount}} </p>
                </div>

                <div class="mb-2">
                    <p class="font-bold text-primary mr-5">Account Executive: </p><p class="text-primary font-sm">{{ae}}</p>
                </div>
                
            </div>
            <div class="mb-3 flex flex-col justify-between">
                <div class="pb-5 border-b-2">
                <p class="font-bold text-primary mr-5">From:</p>
                <input type="date" class="focus-visible:outline-2 
                                    focus-within:outline-primary font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                    text-primary focus-within:bg-secondary"
                                    :class="(invFrom&&invTo)&&invFrom > invTo?'outline outline-red-500 bg-red-300':'bg-secondary'"
                                    @change="setTotal"
                                    v-model="invFrom">
                </div>
                <div>
                    <p class="font-bold text-primary mr-5">Invoice:</p>
                    <!-- <label for="" class="inline-block">Invoice #</label> -->
                    <input type="text" class="focus-visible:outline-2 w-full
                                        font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                        text-primary focus-within:bg-secondary mb-2"
                                        :class="invoiceExists?'outline outline-red-500 bg-red-300 focus-within:outline-red-500':'bg-secondary focus-within:outline-primary'"
                                        v-model="invNum"
                                        @keyup="checkInvoiceNum"
                                        placeholder="Invoice #">

                    <!-- <label for="">Invoice Date</label> -->
                    <input type="date" class="bg-secondary focus-visible:outline-2 w-full
                                        focus-within:outline-primary font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                        text-primary focus-within:bg-secondary"
                                        placeholder="Invoice Date"
                                        v-model="invDate">
                </div>
                <div>
                    <p class="font-bold text-primary mr-5">Total:</p>
                    <input type="text" class="bg-secondary focus-visible:outline-2 w-full
                                        focus-within:outline-primary font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                        text-primary focus-within:bg-secondary"
                                        v-model="total">
                    
                </div>

            </div>
            <div class="mb-3">
                <div class="pb-5 border-b-2">
                    <p class="font-bold text-primary mr-5">To:</p>
                    <input type="date" class="focus-visible:outline-2 
                                        focus-within:outline-primary font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                        text-primary focus-within:bg-secondary"
                                        :class="(invFrom&&invTo)&&invFrom > invTo?'outline outline-red-500 bg-red-300':'bg-secondary'"
                                        @change="setTotal"
                                        v-model="invTo">
                </div>
                <div class="w-full h-min px-4 py-5 bg-yellow-100 m-2"
                v-if="isValid">

                    <p class="text-sm text-yellow-500 text-justify">You are about to bill <br>
                        <span class="font-bold">{{advertiser.name}}</span> <br>
                        total of <span class="font-bold">₱{{total}}.00</span> <br>
                        for ads => <br>
                        from <span class="font-bold">{{humanFrom}}</span> <br>
                        to <span class="font-bold">{{humanTo}}</span> <br>
                        <span v-if="pricing === 'monthly'">({{months}} months duration)</span>
                        <span v-else-if="pricing === 'daily'">({{days}} days duration)</span>
                        <span v-else-if="pricing === 'fixed'">({{days}} days duration)</span>
                    </p>
                </div>

            </div>
           
            
        </div>
        
        <div class="w-full flex justify-center my-2">
            <button class="font-bold px-2 py-1 rounded-lg text-white"
            :class="isValid?'bg-primary':'bg-disabled'"
            :disabled="!isValid"
            @click="createInvoice"
            >Create Invoice</button>
        </div>
            
        <div class="border-b mt-10">
            <p class="text-left text-lg font-bold text-primary">Recent</p>
        </div>
        <table class="w-full mt-2">
            <thead class="bg-primary text-white text-sm font-bold">
                <tr>
                    <td><i class="block h-4 w-4"><PrinterIcon/></i></td>
                    <td>Invoice</td>
                    <td>Applicable</td>
                    <td>Amount</td>
                    
                    <td>Paid?</td>
                </tr>
            </thead>
            <tbody class="text-primary text-sm font-normal">
                <tr v-if="invoices.length" v-for="invoice in invoices" class="border-b hover:bg-gray-200">
                    <td>
                        <a :href="baseURL + invoice.file"
                            class="hover:text-green-500">
                            <i class="block h-4 w-4"><DownloadIcon/>
                            </i>
                        </a>
                    </td>
                    <td>
                        <p class="font-normal">#{{invoice.invoice_no}}</p>
                        <p class="text-xs font-thin">Invoice Date: {{invoice.invoice_date}}</p>
                    </td>
                    <td class="">
                        <p class="text-xs">F: <span class="font-bold">{{invoice.applicable_month_from}}</span></p>
                        <p class="text-xs">T: <span class="font-bold">{{invoice.applicable_month_to}}</span></p>

                    </td>
                    <td>₱ {{amount}}</td>
                    <td> 
                        <div v-if="invoice.paid">
                            <p>{{invoice.paid?'₱'+ invoice.amount_received:''}}</p>
                            <p class="text-xs font-thin">{{invoice.paid? 'OR#'+ invoice.or_number:''}}</p>
                        </div>
                        <div v-else class="relative">
                            <AdPayment :invoice="invoice" @submitted="getInvoiceList(contract)"/>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>
<script setup>
    import { ref,onMounted,onUnmounted } from 'vue';
    import AdPayment from "@/components/advertisements/AdPayment.vue";
    import { DownloadIcon, PrinterIcon } from '@heroicons/vue/solid';
    import axios from 'axios';
    import moment from 'moment';
    const baseURL = axios.defaults.baseURL
    const props = defineProps({
        contract:String,
        amount:Number,
        pricing:String,
        ae:String,
        advertiser:Object,
    })
    
    const invNum = ref("")
    const invoiceExists = ref(false)
    const invDate = ref("")
    const invFrom = ref("")
    const invTo = ref("")
    const total = ref(0)

    const days = ref(0)
    const months = ref(0)

    const humanFrom = ref("")
    const humanTo = ref("")


    const invoices = ref([])
    const isValid = ref(false)
    
    const getInvoiceList = async(contract)=> {
        const response = await axios.get(`/invoices/${contract}`)
        if(response.status === 200){
            invoices.value = response.data
            console.log(response.data)
        }else{
            invoices.value = []
        }
    }
    const setDefaultDate = ()=> {
        const today = moment()
        invDate.value = today.format('YYYY-MM-DD')
    }
    const setTotal = ()=> {
        if(invFrom.value&&invTo.value){
            const f = moment(invFrom.value)
            const t = moment(invTo.value)
            if(props.pricing === 'fixed'){
                total.value = props.amount
            }else if(props.pricing === 'monthly'){
                const difference = t.diff(f,"months")
                
                if(difference === 0) months.value = 1
                else months.value = difference
                
                total.value = props.amount * months.value
            }else if(props.pricing === 'daily'){
                days.value = t.diff(f,"days")
                total.value = props.amount * days.value
            }
        humanize()
        }
    }
    
    const humanize = ()=> {
        humanFrom.value = moment(invFrom.value).format("MMM Do YYYY")
        humanTo.value = moment(invTo.value).format("MMM Do YYYY")

    }
    const checkInvoiceNum = async () => {
        const response = await axios.get(`invoice_exists/${invNum.value}`)
        invoiceExists.value = response.data.exists
    }
    const checkValidity = setInterval(() => {
            const allFilled = invNum.value&&invDate.value&&invFrom.value&&invTo.value
            const rangeCorrect = moment(invFrom.value) < moment(invTo.value)
            if(allFilled&&rangeCorrect&&!invoiceExists.value) isValid.value=true
            else isValid.value = false
        }, 1000);

    
    const createInvoice = async ()=> {
        const fd = new FormData()
        fd.append("advertiser",props.advertiser.id)
        fd.append("from_contract",props.contract)
        fd.append("account_executive",props.ae)
        fd.append("invoice_date",invDate.value)
        fd.append("invoice_no",invNum.value)
        fd.append("amount",total.value)
        fd.append("applicable_month_from",invFrom.value)
        fd.append("applicable_month_to",invTo.value)

        const response = await axios.post("/add_invoice",fd)
        if(response.status === 200){
            getInvoiceList(response.data.contract)
            invDate.value = ""
            invNum.value = ""
            invFrom.value = ""
            invTo.value = ""
        }
    }

    onMounted(() => {
        getInvoiceList(props.contract)
        setDefaultDate()
        checkValidity

    })
    onUnmounted(() => {
        clearInterval(checkValidity)
    })

</script>
