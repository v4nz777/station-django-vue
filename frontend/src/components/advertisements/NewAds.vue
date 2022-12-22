<template>
    <div class="mx-auto my-3">
        <button @click="open = true" @mouseover="parentIsHovered = true" @mouseout=" parentIsHovered = false"
                class="w-32 rounded-md hover:shadow-md flex items-center justify-start px-2 h-9 hover:bg-primary hover:text-white">
        <i class="h-6 w-6" :class="parentIsHovered ? 'text-white':'text-primary'"><MegaphoneIcon/></i>
        <h3 class="text-sm font-light">{{buttonTitle}}</h3>
        </button>
        <teleport to='body'>

            <div class="bg-slate-800 bg-opacity-50 flex justify-center items-center absolute top-0 right-0 bottom-0 left-0"
                v-if="open"
                ref="outer"
                @click.self="open = false">
                <div class="w-max bg-white rounded-md text-start justify-center items-center flex flex-col">
                    <div class="flex flex-col justify-center text-center pt-4 w-full">
                        <h1 class="font-bold text-gray-500 text-xl">Add New Advertisement</h1>
                        <hr class="mt-4 w-full">
                    </div>
                    <div id="newads-scroll" class="w-full h-96 overflow-y-scroll"
                        v-if="display === 'composition'">
                        <!-- :Title: -->
                        <div class="my-3 w-96 text-right px-11">
                            <label for="adTitle" class="text-white px-2 py-1 w-full rounded-l-md
                                shadow-md text-sm mr-1"
                                :class="adTitle? 'bg-primary text-white':'bg-secondary text-primary'">Title: </label>
                            <input type="text" v-model="adTitle" class="bg-secondary focus-visible:outline-2 
                                focus-within:outline-primary font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                text-primary focus-within:bg-secondary"
                                @change="titleCheck">
                            <div class="inline-block ml-1" v-if="isTitleDecided">
                                <i class="inline-block w-4 h-4 text-primary" v-if="isTitleValid"><CheckCircleIcon/></i>
                                <i class="inline-block w-4 h-4 text-red-500" v-if="!isTitleValid"><XCircleIcon/></i>
                            </div>
                            <div class="text-xs text-red-500 text-left mx-5">
                                {{titleError}}
                            </div>
                        </div>
                        
                        
                        <!-- :Advertiser: -->
                        <div class="my-3 w-96 text-right px-11">
                            <label for="adAdvertiser" class="text-white px-2 py-1 w-full rounded-l-md
                                shadow-md text-sm mr-1"
                                :class="adAdvertiser? 'bg-primary text-white':'bg-secondary text-primary' ">Advertiser: </label>
                            <div class="inline-block relative">
                                <input type="text" v-model="adAdvertiser" class="bg-secondary focus-visible:outline-2 
                                    focus-within:outline-primary font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                    text-primary focus-within:bg-secondary"
                                    list="advertiserlist"
                                    @change="advertiserCheck"
                                    @keyup="advertiserSearch(adAdvertiser)"
                                    @emptied="isAdvertiserDecided = false">

                                <ul id="advertiserlist" class="bg-white absolute w-full h-max"
                                    v-if="searchedAdvertisers.length && !isAdvertiserDecided">
                                    <li v-for="i in searchedAdvertisers" class="text-sm text-left font-light
                                    hover:text-white hover:bg-primary w-full p-1 z-50"
                                    @click="selectAdvertiser(i.name)">
                                        {{i.name}}
                                    </li>
                                </ul>  
                            </div>
                            <div class="inline-block ml-1" v-if="isAdvertiserDecided">
                                <i class="inline-block w-4 h-4 text-primary" v-if="isAdvertiserValid"><CheckCircleIcon/></i>
                                <i class="inline-block w-4 h-4 text-red-500" v-if="!isAdvertiserValid"><XCircleIcon/></i>
                            </div>
                            <div class="text-xs text-red-500 text-left mx-5">
                                {{advertiserError}}
                            </div>
                        </div>
                        <!-- :Type: -->
                        <div class="my-3 w-96 text-right px-11">
                            <label for="adType" class="text-white px-2 py-1 w-full rounded-l-md
                                shadow-md text-sm mr-1"
                                :class="adType? 'bg-primary text-white':'bg-secondary text-primary' ">Type: </label>
                            <select name="" id="adType" v-model="adType" class="bg-secondary focus-visible:outline-2 
                                focus-within:outline-primary font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                text-primary focus-within:bg-secondary">
                                <option value="local">Local</option>
                                <option value="national">National</option>
                            </select>
                            <div class="inline-block ml-1" v-if="adType">
                                <i class="inline-block w-4 h-4 text-primary"><CheckCircleIcon/></i>
                            </div>
                        </div>
                        
                        <!-- :Contract: -->
                        <div class="my-3 w-96 text-right px-11">
                            <label for="adContract" class="text-white px-2 py-1 w-full rounded-l-md
                                shadow-md text-sm mr-1"
                                :class="adContract? 'bg-primary text-white':'bg-secondary text-primary' ">{{adType === 'local'?'Contract:':'IM:'}}</label>
                            <input type="text" v-model="adContract" class="bg-secondary focus-visible:outline-2 
                                focus-within:outline-primary font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                text-primary focus-within:bg-secondary"
                                @keyup="contractCheck">
                            <div class="inline-block ml-1" v-if="isContractDecided">
                                <i class="inline-block w-4 h-4 text-primary" v-if="isContractValid"><CheckCircleIcon/></i>
                                <i class="inline-block w-4 h-4 text-red-500" v-else><XCircleIcon/></i>
                            </div>
                            <div class="text-xs text-red-500 text-center mx-5">
                                {{contractError}}
                            </div>
                        <hr class="my-5" v-if="adType === 'local'">
                        </div>
                        <!-- :BO Number: -->
                        <div class="my-3 w-96 text-right px-11" v-if="adType == 'national'">
                            <label for="adBONum" class="text-white px-2 py-1 w-full rounded-l-md
                                shadow-md text-sm mr-1"
                                :class="adBONum? 'bg-primary text-white':'bg-secondary text-primary' ">B.O. Number: </label>
                            <input type="text" v-model="adBONum" class="bg-secondary focus-visible:outline-2 
                                focus-within:outline-primary font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                text-primary focus-within:bg-secondary"
                                @change="boCheck">
                            <div class="inline-block ml-1" v-if="isBODecided">
                                <i class="inline-block w-4 h-4 text-primary" v-if="isBOValid"><CheckCircleIcon/></i>
                                <i class="inline-block w-4 h-4 text-red-500" v-if="!isBOValid"><XCircleIcon/></i>
                            </div>
                            <div class="text-xs text-red-500 text-left mx-5">
                                {{boError}}
                            </div>
                            <hr class="my-5" v-if="adType === 'national'">
                        </div>
                        <!-- :Ex Deal: -->
                        <div class="my-3 w-96 text-right px-11">
                            <label for="exDeal" class="text-primary px-2 py-1 w-full text-sm mr-1">This is an ex-deal </label>
                            <input id="exDeal" type="checkbox" v-model="exDeal" class="w-4 h-4 border-primary align-bottom">
                        </div>
                        <!-- :Pricing: -->
                        <div class="my-3 w-96 text-right px-11">
                            <label for="adPricing" class="text-white px-2 py-1 w-full rounded-l-md
                                shadow-md text-sm mr-1"
                                :class="adPricing? 'bg-primary text-white':'bg-secondary text-primary' ">Pricing: </label>
                            <select name="" id="adPricing" v-model="adPricing" class="bg-secondary focus-visible:outline-2 
                                focus-within:outline-primary font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                text-primary focus-within:bg-secondary"
                                @change="summarizeBroadcast">
                                <option value="monthly">Monthly</option>
                                <option value="daily">Daily</option>
                                <option value="fixed">Fixed</option>
                            </select>
                            <div class="inline-block ml-1" v-if="adPricing">
                                <i class="inline-block w-4 h-4 text-primary"><CheckCircleIcon/></i>
                            </div>
                        </div>
                        <!-- :Amount: -->
                        <div class="my-3 w-96 text-right px-11" v-if="adPricing">
                            <label for="adAmount" class="text-white px-2 py-1 w-full rounded-l-md
                                shadow-md text-sm mr-1"
                                v-if="adPricing === 'monthly'"
                                :class="adAmount? 'bg-primary text-white':'bg-secondary text-primary' ">₱ per month: </label>
                            <label for="adAmount" class="text-white px-2 py-1 w-full rounded-l-md
                                shadow-md text-sm mr-1"
                                v-else-if="adPricing === 'daily'"
                                :class="adAmount? 'bg-primary text-white':'bg-secondary text-primary' ">₱ per day: </label>
                            <label for="adAmount" class="text-white px-2 py-1 w-full rounded-l-md
                                shadow-md text-sm mr-1"
                                v-else-if="adPricing === 'fixed'"
                                :class="adAmount? 'bg-primary text-white':'bg-secondary text-primary' ">₱ in total: </label>
                            <input type="text" v-model="adAmount" class="bg-secondary focus-visible:outline-2 
                                focus-within:outline-primary font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                text-primary focus-within:bg-secondary"
                                @keyup="summarizeBroadcast"
                                @change="amountCheck">
                            <div class="inline-block ml-1" v-if="isAmountDecided">
                                <i class="inline-block w-4 h-4 text-primary" v-if="isAmountValid"><CheckCircleIcon/></i>
                                <i class="inline-block w-4 h-4 text-red-500" v-if="!isAmountValid"><XCircleIcon/></i>
                            </div>
                            <div class="text-xs text-red-500 text-left mx-5">
                                {{amountError}}
                            </div>
                        </div>
                        <!-- :Broadcast Start: -->
                        <div class="my-3 w-96 text-right px-11">
                            <label for="adStart" class="text-white px-2 py-1 w-full rounded-l-md
                                shadow-md text-sm mr-1"
                                :class="adStart? 'bg-primary text-white':'bg-secondary text-primary' ">Broadcast Start: </label>
                            <input type="date" v-model="adStart" class="bg-secondary focus-visible:outline-2 
                                focus-within:outline-primary font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                text-primary focus-within:bg-secondary"
                                @change="startCheck">
                            <div class="inline-block ml-1" v-if="isStartDecided">
                                <i class="inline-block w-4 h-4 text-primary" v-if="isStartValid"><CheckCircleIcon/></i>
                                <i class="inline-block w-4 h-4 text-red-500" v-if="!isStartValid"><XCircleIcon/></i>
                            </div>
                            <div class="text-xs text-red-500 text-left mx-5">
                                {{startError}}
                            </div>
                        </div>
                        <!-- :Broadcast End: -->
                        <div class="my-3 w-96 text-right px-11">
                            <label for="adEnd" class="text-white px-2 py-1 w-full rounded-l-md
                                shadow-md text-sm mr-1"
                                :class="adEnd? 'bg-primary text-white':'bg-secondary text-primary' ">Broadcast End: </label>
                            <input type="date" v-model="adEnd" class="bg-secondary focus-visible:outline-2 
                                focus-within:outline-primary font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                text-primary focus-within:bg-secondary"
                                @change="endCheck">
                            <div class="inline-block ml-1" v-if="isEndDecided">
                                <i class="inline-block w-4 h-4 text-primary" v-if="isEndValid"><CheckCircleIcon/></i>
                                <i class="inline-block w-4 h-4 text-red-500" v-if="!isEndValid"><XCircleIcon/></i>
                            </div>
                            <div class="text-xs text-red-500 text-left mx-5">
                                {{endError}}
                            </div>
                        </div>
                        <div class="my-3 w-96 text-center px-11 text-primary font-light text-sm"
                            v-if="totalPrice">
                            <div><span class="font-bold">₱{{totalPrice}}.00</span> in total</div>
                            <div>will run for <span class="font-bold">{{totalBroadcastRange}}</span></div>
                        </div>
                        <hr class="my-5">
                        <!-- :Spots/day: -->
                        <div class="my-3 w-96 text-right px-11">
                            <label for="adSpot" class="text-white px-2 py-1 w-full rounded-l-md
                                shadow-md text-sm mr-1"
                                :class="adSpot? 'bg-primary text-white':'bg-secondary text-primary' ">Spots/day: </label>
                            <input type="number" v-model="adSpot" class="bg-secondary focus-visible:outline-2 
                                focus-within:outline-primary font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                text-primary focus-within:bg-secondary"
                                @change="spotCheck">
                            <div class="inline-block ml-1" v-if="isSpotDecided">
                                <i class="inline-block w-4 h-4 text-primary" v-if="isSpotValid"><CheckCircleIcon/></i>
                                <i class="inline-block w-4 h-4 text-red-500" v-if="!isSpotValid"><XCircleIcon/></i>
                            </div>
                            <div class="text-xs text-red-500 text-right mx-5"
                            v-if="spotError">
                                {{spotError}}
                            </div>
                        </div>
                        <!-- :Schedule: -->
                        <div class="my-3 w-96 text-right px-11">
                            <label for="adSchedule" class="text-white px-2 py-1 w-full rounded-l-md
                                shadow-md text-sm mr-1"
                                :class="adSchedule? 'bg-primary text-white':'bg-secondary text-primary' ">Schedule: </label>
                            <input type="text" v-model="adSchedule" class="bg-secondary focus-visible:outline-2 
                                focus-within:outline-primary font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                text-primary focus-within:bg-secondary"
                                placeholder="ex: 6:10am,7:40am"
                                @keyup="pushToScheduleList">
                            <div class="inline-block ml-1" v-if="adSchedule">
                                <i class="inline-block w-4 h-4 text-primary" v-if="adSpot === adScheduleList.length"><CheckCircleIcon/></i>
                                <i class="inline-block w-4 h-4 text-red-500" v-else><XCircleIcon/></i>
                            </div>
                            <div class="text-xs text-red-500 text-right mx-5"
                            v-if="adSpot !== adScheduleList.length && adSchedule">
                                {{adSpot}} is allowed, you provided {{adScheduleList.length}}
                            </div>
                            <div class="grid grid-cols-4 p-6 my-2 bg-secondary"
                                v-if="adSchedule">

                                <div v-for="i in adScheduleList"
                                class="bg-primary w-full shadow-sm border rounded-xl
                                text-xs text-center text-white font-extralight py-1">
                                    {{i}}
                                </div>
                            </div>
                        <hr class="my-5">
                        </div>
                        <!-- :AudioFile: -->
                        <div class="my-3 w-96 text-right px-11">
                            <div class="mb-5">
                                <label for="multiplVersions" class="text-primary px-2 py-1 w-full text-sm mr-1">
                                    Has multiple versions:
                                    <input type="checkbox" class="w-4 h-4 border-primary align-bottom" v-model="multiplVersions">
                                </label>
                            </div>
                            <label for="adAudioFile" class="text-white px-2 py-1 w-full rounded-l-md
                                shadow-md text-sm mr-1"
                                :class="uploadedFiles.length? 'bg-primary text-white':'bg-secondary text-primary' ">Audio FIle: </label>
                            <input type="file" ref="adAudioFile" accept="audio/*" class="hidden" @change="audioFileCheck" :multiple="multiplVersions">
                            <button class="bg-secondary focus-visible:outline-2 
                                focus-within:outline-primary font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                text-primary focus-within:bg-secondary"
                                @click="$refs.adAudioFile.click">Upload</button>
                            <div class="inline-block ml-1" v-if="isAudioFileDecided">
                                <i class="inline-block w-4 h-4 text-primary" v-if="isAudioFileValid"><CheckCircleIcon/></i>
                                <i class="inline-block w-4 h-4 text-red-500" v-if="!isAudioFileValid"><XCircleIcon/></i>
                            </div>
                            <ul class="text-xs text-primary text-right mx-1"
                            v-if="adAudioFile">
                                <li v-for="file,index in uploadedFiles">
                                    {{file.name.length > 25? `${file.name.substring(0,25)}...${file.name.substring(file.name.length-3,file.name.length)}`: file.name}}
                                    <button @click="removeFromFiles(file,index)"
                                    class="text-primary hover:bg-red-500 hover:text-white rounded-full w-4 h-4 font-bold text-center">x</button>
                                </li>
                            </ul>
                            <div class="text-xs text-red-500 text-right mx-5">
                                {{audioFileError}}
                            </div>
                        </div>
                        <!-- :MaterialDuration: -->
                        <div class="my-3 w-96 text-right px-10">
                            <label for="adMaterialDuration" class="text-white px-2 py-1 w-full rounded-l-md
                                shadow-md text-sm mr-1"
                                :class="adMaterialDuration? 'bg-primary text-white':'bg-secondary text-primary' ">Duration(seconds): </label>
                            <input type="text" v-model="adMaterialDuration" class="bg-secondary focus-visible:outline-2 
                                focus-within:outline-primary font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                text-primary focus-within:bg-secondary w-20"
                                @change="materialDurationCheck">
                            <div class="inline-block ml-1" v-if="isMaterialDurationDecided">
                                <i class="inline-block w-4 h-4 text-primary" v-if="isMaterialDurationValid"><CheckCircleIcon/></i>
                                <i class="inline-block w-4 h-4 text-red-500" v-if="!isMaterialDurationValid"><XCircleIcon/></i>
                            </div>
                            <div class="text-xs text-red-500 text-left mx-5">
                                {{materialDurationError}}
                            </div>
                        <hr class="my-5">
                        </div>
                        <!-- :Taglines: -->
                        <div class="my-3 w-96 text-right px-11">
                            <label for="adTaglines" class="text-primary px-2 py-1 w-full text-sm mr-1">This ad has taglines? (e.g: aob,ss,tc) </label>
                            <input id="adTaglines" type="checkbox" v-model="adTaglines" class="w-4 h-4 border-primary align-bottom">
                            <div v-if="adTaglines" class="my-2">
                                <!-- /AOB/ -->
                                <div class="mt-6">
                                    <label for="adTagAOBspot" class="text-white px-2 py-1 w-full rounded-l-md
                                    shadow-md text-sm mr-1"
                                    :class="adTagAOBspot? 'bg-primary text-white':'bg-secondary text-primary' ">AOB spots/day</label>
                                    <input type="number" v-model="adTagAOBspot" id="adTagAOBspot"
                                        class="bg-secondary focus-visible:outline-2 
                                        focus-within:outline-primary font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                        text-primary focus-within:bg-secondary w-20">
                                    <div class="text-xs text-primary text-right mx-5">
                                        leave blank if none
                                    </div>
                                </div>
                                <div v-if="adTagAOBspot" class="mt-2">
                                    <label for="adAOBsched" class="text-white px-2 py-1 w-full rounded-l-md
                                    shadow-md text-sm mr-1"
                                    :class="adAOBsched? 'bg-primary text-white':'bg-secondary text-primary' ">Schedule:</label>
                                    <input type="text" id="adAOBsched" v-model="adAOBsched"
                                        
                                        @keyup="pushToAOBschedList"
                                        class="bg-secondary focus-visible:outline-2 
                                        focus-within:outline-primary font-thin text-sm px-2 py-1 shadow-md 
                                        rounded-r-md text-primary focus-within:bg-secondary">
                                        <div class="inline-block ml-1" v-if="adAOBsched">
                                            <i class="inline-block w-4 h-4 text-primary" v-if="adTagAOBspot === adAOBschedList.length"><CheckCircleIcon/></i>
                                            <i class="inline-block w-4 h-4 text-red-500" v-else><XCircleIcon/></i>
                                        </div>
                                        <div class="text-xs text-red-500 text-right mx-5"
                                        v-if="adTagAOBspot !== adAOBschedList.length && adAOBsched">
                                            {{adTagAOBspot}} is allowed, you provided {{adAOBschedList.length}}
                                        </div>
                                    <div class="grid grid-cols-4 p-6 my-2 bg-secondary"
                                    v-if="adAOBsched">
                                        <div v-for="i in adAOBschedList"
                                            class="bg-primary w-full shadow-sm border rounded-xl
                                            text-xs text-center text-white font-extralight py-1">
                                            {{i}}
                                        </div>
                                    </div>
                                </div>
                                <!-- /TC/ -->
                                <div class="mt-6">
                                    <label for="adTagTCspot" class="text-white px-2 py-1 w-full rounded-l-md
                                    shadow-md text-sm mr-1"
                                    :class="adTagTCspot? 'bg-primary text-white':'bg-secondary text-primary' ">TC spots/day</label>
                                    <input type="number" v-model="adTagTCspot" id="adTagTCspot"
                                        class="bg-secondary focus-visible:outline-2 
                                        focus-within:outline-primary font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                        text-primary focus-within:bg-secondary w-20">
                                    <div class="text-xs text-primary text-right mx-5">
                                        leave blank if none
                                    </div>
                                </div>
                                <div v-if="adTagTCspot" class="mt-2">
                                    <label for="adTCsched" class="text-white px-2 py-1 w-full rounded-l-md
                                    shadow-md text-sm mr-1"
                                    :class="adTCsched? 'bg-primary text-white':'bg-secondary text-primary' ">Schedule:</label>
                                    <input type="text" id="adTCsched" v-model="adTCsched"
                                        placeholder="ex: 6:00am,7:00am"
                                        @keyup="pushToTCschedList"
                                        class="bg-secondary focus-visible:outline-2 
                                        focus-within:outline-primary font-thin text-sm px-2 py-1 shadow-md 
                                        rounded-r-md text-primary focus-within:bg-secondary">
                                    <div class="inline-block ml-1" v-if="adTCsched">
                                        <i class="inline-block w-4 h-4 text-primary" v-if="adTagTCspot === adTCschedList.length"><CheckCircleIcon/></i>
                                        <i class="inline-block w-4 h-4 text-red-500" v-else><XCircleIcon/></i>
                                    </div>
                                    <div class="text-xs text-red-500 text-right mx-5"
                                    v-if="adTagTCspot !== adTCschedList.length && adTCsched">
                                        {{adTagTCspot}} is allowed, you provided {{adTCschedList.length}}
                                    </div>
                                    <div class="grid grid-cols-4 p-6 my-2 bg-secondary"
                                    v-if="adTCsched">
                                        <div v-for="i in adTCschedList"
                                            class="bg-primary w-full shadow-sm border rounded-xl
                                            text-xs text-center text-white font-extralight py-1">
                                            {{i}}
                                        </div>
                                    </div>
                                </div>
                                <!-- /SS/ -->
                                <div class="mt-6">
                                    <label for="adTagSSspot" class="text-white px-2 py-1 w-full rounded-l-md
                                    shadow-md text-sm mr-1"
                                    :class="adTagSSspot? 'bg-primary text-white':'bg-secondary text-primary' ">SS spots/day</label>
                                    <input type="number" v-model="adTagSSspot" id="adTagSSspot"
                                        class="bg-secondary focus-visible:outline-2 
                                        focus-within:outline-primary font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                        text-primary focus-within:bg-secondary w-20">
                                    <div class="text-xs text-primary text-right mx-5">
                                        leave blank if none
                                    </div>
                                </div>
                                <div v-if="adTagSSspot" class="mt-2">
                                    <label for="adSSsched" class="text-white px-2 py-1 w-full rounded-l-md
                                    shadow-md text-sm mr-1"
                                    :class="adSSsched? 'bg-primary text-white':'bg-secondary text-primary' ">Schedule:</label>
                                    <input type="text" id="adSSsched" v-model="adSSsched"
                                        placeholder="ex: 6:30am,7:30am"
                                        @keyup="pushToSSschedList"
                                        class="bg-secondary focus-visible:outline-2 
                                        focus-within:outline-primary font-thin text-sm px-2 py-1 shadow-md 
                                        rounded-r-md text-primary focus-within:bg-secondary">
                                    <div class="inline-block ml-1" v-if="adSSsched">
                                        <i class="inline-block w-4 h-4 text-primary" v-if="adTagSSspot === adSSschedList.length"><CheckCircleIcon/></i>
                                        <i class="inline-block w-4 h-4 text-red-500" v-else><XCircleIcon/></i>
                                    </div>
                                    <div class="text-xs text-red-500 text-right mx-5"
                                    v-if="adTagSSspot !== adSSschedList.length && adSSsched">
                                        {{adTagSSspot}} is allowed, you provided {{adSSschedList.length}}
                                    </div>
                                    <div class="grid grid-cols-4 p-6 my-2 bg-secondary"
                                    v-if="adSSsched">
                                        <div v-for="i in adSSschedList"
                                            class="bg-primary w-full shadow-sm border rounded-xl
                                            text-xs text-center text-white font-extralight py-1">
                                            {{i}}
                                        </div>
                                    </div>
                                </div>
                                <!-- /// -->
                            </div>
                        <hr class="my-5">
                        </div>
                        <!-- :Account Executive: -->
                        <div class="my-3 w-96 text-right px-11">
                            <label for="adAE" class="text-white px-2 py-1 w-full rounded-l-md
                                shadow-md text-sm mr-1"
                                :class="adAE? 'bg-primary text-white':'bg-secondary text-primary' ">AE: </label>
                            <div class="inline-block">
                                <select name="" id="adAE" v-model="adAE" class="bg-secondary focus-visible:outline-2 
                                    focus-within:outline-primary font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                    text-primary focus-within:bg-secondary">
                                <option value="office">Office</option>
                                <option v-for="user in accountExecutives" :value="user.username">{{user.first_name}} {{user.last_name}}</option>
                                </select>
 
                            </div>
                            <div class="inline-block ml-1" v-if="adAE">
                                <i class="inline-block w-4 h-4 text-primary"><CheckCircleIcon/></i>
                            </div>

                        </div>
                        <!-- :: -->

                        <div class="mx-10 my-5">
                            <button class=" text-white w-full"
                            :class="submitEnabled? 'bg-primary':'bg-disabled'"
                            :disabled="!submitEnabled"
                            @click="display = 'preview'">Submit</button>
                        </div>

                    </div>
                    <div id="newads-scroll" class="w-full h-96 overflow-y-scroll"
                        v-else-if="display === 'preview'">
                        <div class="text-left font-normal flex flex-col px-10">

                            <span class="mb-5">Review before submission...</span>
                            <span>Title: <span class="font-light text-primary">{{adTitle}}</span></span>
                            <span>Advertiser: <span class="font-light text-primary">{{adAdvertiser}}</span></span>
                            <span>Type: <span class="font-light text-primary">{{adType}}</span></span>
                            <span>{{adType === 'local'?'Contract: ':'IM: '}}<span class="font-light text-primary">{{adContract}}</span></span>
                            <span v-if="adType === 'national'">B.O: <span class="font-light text-primary">{{adBONum}}</span></span>
                            <span>Ex-deal?: <span class="font-light text-primary">{{exDeal? 'yes':'no'}}</span></span>
                            <span>Pricing type: <span class="font-light text-primary">{{adPricing}}</span></span>
                            <span>Amount: <span class="font-light text-primary">₱ {{adAmount}}/month</span></span>
                            <span>Starts: <span class="font-light text-primary">{{adStart}}</span></span>
                            <span>Ends: <span class="font-light text-primary">{{adEnd}}</span></span>
                            <span>Spots: <span class="font-light text-primary">{{adSpot}}/day</span></span>
                            <span>Schedule: <span class="font-light text-primary">{{adSchedule}}</span></span>
                            <span>Duration: <span class="font-light text-primary">{{adMaterialDuration}}</span></span>
                            <span>Audio File: <span class="font-light text-primary text-xs">{{uploadedFiles[0].name}}</span></span>
                            <span>Has Taglines?: <span class="font-light text-primary">{{adTaglines? 'yes':'no'}}</span></span>
                            <div class="flex flex-col" v-if="adTaglines">
                                <span>AOB spots: <span class="font-light text-primary">{{adTagAOBspot}}</span></span>
                                <span>AOB schedule: <span class="font-light text-primary">{{adAOBsched}}</span></span>
                                <span>TC spots: <span class="font-light text-primary">{{adTagTCspot}}</span></span>
                                <span>TC schedule: <span class="font-light text-primary">{{adTCsched}}</span></span>
                                <span>SS spots: <span class="font-light text-primary">{{adTagSSspot}}</span></span>
                                <span>SS schedule: <span class="font-light text-primary">{{adSSsched}}</span></span>
                            </div>
                            
                        </div>
                        <hr>
                        <div class="grid grid-cols-2 space-x-5 px-5 py-5">
                            
                            <button @click="display = 'composition'"
                                class="text-primary hover:bg-secondary hover:shadow-md rounded-md">Edit</button>
                            <button @click="submitNewAds"
                                class="bg-primary shadow-md text-white hover:bg-primary rounded-md">Confirm</button>
                        </div>
                    </div>


                </div>
            </div>
        </teleport>
    </div>
</template>
<script setup>
    import MegaphoneIcon from "@/components/icons/MegaphoneIcon.vue"
    import { CheckCircleIcon, XCircleIcon } from "@heroicons/vue/solid";
    import { ref, onMounted } from "vue";
    import moment from 'moment';
    import axios from 'axios';
    import { userStore } from '@/stores/user';
    import router from "@/router";

    const props = defineProps({
        buttonTitle: String
    })
    
    const open = ref(false)
    const parentIsHovered = ref(false)
    const outer = ref("")

    const display = ref("composition")

    const adTitle = ref("")
    const isTitleValid = ref(false)
    const titleError = ref("")
    const isTitleDecided = ref(false)
    const titleCheck = () => {
        if (!adTitle.value) isTitleDecided.value = false
        else isTitleDecided.value = true
        isTitleValid.value = true
    }

    const adType = ref("")
    setTimeout(() => {
        adType.value = 'local'
    }, 1000);


    const adAdvertiser = ref("")
    const isAdvertiserValid = ref(false)
    const advertiserError = ref("")
    const isAdvertiserDecided = ref(false)
    const searchedAdvertisers = ref([])
 
    const advertiserCheck = () => {
        setTimeout(() => {
            if (adAdvertiser.value) isAdvertiserDecided.value = true
            else isAdvertiserDecided.value = false
            isAdvertiserValid.value = true
        }, 1000);
    }
    const advertiserSearch = async (keyword) => {
        if(!keyword)isAdvertiserDecided.value = false
        else{
            const response = await axios.get(`search_advertiser/${keyword}`)
            searchedAdvertisers.value = response.data
            isAdvertiserDecided.value = false
        }
    }
    const selectAdvertiser = (adv) => {
        adAdvertiser.value = adv
        isAdvertiserDecided.value = true
        isAdvertiserValid.value = true
    }



    const adContract = ref("")
    const isContractValid = ref(false)
    const contractError = ref("")
    const isContractDecided = ref(false)
    const contractCheck = async () => {
        if (adContract.value){
            const response = await axios.get('ads/all')
            const contracts = response.data.map(result => result.contract)
       
            if (contracts.includes(adContract.value)){
                isContractDecided.value = true
                isContractValid.value = false
                contractError.value = '#' + adContract.value + " already exists"
            }else{
                isContractDecided.value = true
                isContractValid.value = true
                contractError.value = ""

                
            }

        }
        else {
            isContractDecided.value = false
            isContractValid.value = false
            contractError.value = ""
        }
    }

    const adBONum = ref("")
    const isBOValid = ref(false)
    const boError = ref("")
    const isBODecided = ref(false)
    const boCheck = () => {
        if(!adBONum.value) isBODecided.value = false
        else isBODecided.value = true
        isBOValid.value = true
    }

    const adPricing = ref("")
    const exDeal = ref(false)


    const adAmount = ref(0)
    const isAmountValid = ref(false)
    const amountError = ref("")
    const isAmountDecided = ref(false)
    const amountCheck = () => {
        if(!adAmount.value) isAmountDecided.value = false
        else isAmountDecided.value = true
        
        isAmountValid.value = true
    }
    const totalPrice = ref("")
    const summarizeBroadcast = () => {
        // for pricing
        if (adAmount.value === "" || adAmount.value === "") amountCheck()
        if(adAmount.value&&adStart.value&&adEnd.value&&isStartValid.value&&isEndValid.value){
            const ad_start = moment(adStart.value)
            const ad_end = moment(adEnd.value)

            let price = 0
            if(adPricing.value === "monthly")price = ad_end.diff(ad_start,"months")
            else if(adPricing.value === "daily")price = ad_end.diff(ad_start,"days")
            else if(adPricing.value === "fixed")price = 1

            
            if (price === 0){
                totalPrice.value = 1 * adAmount.value
            } else totalPrice.value = price * adAmount.value


            // for duration/length of broadcast
            totalBroadcastRange.value = ad_start.to(ad_end,true)
        }

        

    }

    const adStart = ref("")
    const isStartValid = ref(false)
    const startError = ref("")
    const isStartDecided = ref(false)
    const startCheck = () => {
        
        if(!adStart.value)isStartDecided.value = false
        else isStartDecided.value = true

        if(adStart.value&&adEnd.value){
            const s = moment(adStart.value)
            const e = moment(adEnd.value)
            
            if(e.diff(s) > 0) {
                isEndValid.value = true
                isStartValid.value = true
            }
            else {
                isEndValid.value = false
                isStartValid.value = false
            }  
        } else isStartValid.value = true
        summarizeBroadcast()
    }

    const adEnd = ref("")
    const isEndValid = ref(false)
    const endError = ref("")
    const isEndDecided = ref(false)
    const endCheck = () => {
        if(!adEnd.value)isEndDecided.value = false
        else isEndDecided.value = true

        const s = moment(adStart.value)
        const e = moment(adEnd.value)
        
        if(e.diff(s) > 0) {
            isEndValid.value = true
            isStartValid.value = true
        }
        else {
            isEndValid.value = false
            isStartValid.value = false
        }
        summarizeBroadcast()
    }

    const totalBroadcastRange = ref("")

    const adSpot = ref(0)
    const isSpotValid = ref(false)
    const spotError = ref("")
    const isSpotDecided = ref(false)
    const spotCheck = () => {
        if(!adSpot.value)isSpotDecided.value = false
        else isSpotDecided.value = true

        if(adSchedule.value){
            if(adSpot.value === adScheduleList.value.length){
                isSpotValid.value = true
                spotError.value = ""
            }
            else{
                isSpotValid.value = false
                spotError.value = "no. of spots must be same no. of scheduled"
            }
        }else isSpotValid.value = true
    }

    const adSchedule = ref("")
    const adScheduleList = ref([])
    const pushToScheduleList = () => {
        adScheduleList.value = adSchedule.value.split(",") //(/[, ]+/)separate comma or space
        spotCheck()
    }


    const adMaterialDuration = ref("")
    const isMaterialDurationValid = ref(false)
    const materialDurationError = ref("")
    const isMaterialDurationDecided = ref(false)
    const materialDurationCheck = () => {
        if(!adMaterialDuration.value) isMaterialDurationDecided.value = false
        else isMaterialDurationDecided.value = true

        isMaterialDurationValid.value = true
    }


    const multiplVersions = ref(false)
    const adAudioFile = ref("")
    const uploadedFiles = ref([])
    const isAudioFileValid = ref(false)
    const audioFileError = ref("")
    const isAudioFileDecided = ref(false)
    const audioFileURL = ref("")
    const audioFileTemp = ref("")
    setInterval(() => {
        if(!multiplVersions.value && uploadedFiles.value.length > 1) {
            isAudioFileValid.value = false
            audioFileError.value = "only 1 upload is allowed"
        }
        else {
            isAudioFileValid.value = true
            audioFileError.value = ""
        }
    }, 1000);
    const removeFromFiles = (file,index) => {
        uploadedFiles.value.splice(index,1)
        if(!uploadedFiles.value.length){
            adAudioFile.value.value = ""
            adAudioFile.value = ""
            isAudioFileDecided.value = false
            isAudioFileValid.value = false
            uploadedFiles.value = []
            audioFileURL.value = ""
            audioFileTemp.value = ""
        }else if(index === uploadedFiles.value.length) adAudioFile.value.value = ""
      

    }
    const audioFileCheck = () => {
        audioFileURL.value = URL.createObjectURL(adAudioFile.value.files[0])
        audioFileTemp.value = new Audio(audioFileURL.value)
        audioFileTemp.value.onloadedmetadata = () => {
            // calculate duration
            if(!adMaterialDuration.value){
                adMaterialDuration.value = Math.round(audioFileTemp.value.duration)
                materialDurationCheck()
            }
        }
        
        if (uploadedFiles.value.length && multiplVersions.value){
            uploadedFiles.value = [...uploadedFiles.value,...adAudioFile.value.files]
        } else uploadedFiles.value = [...adAudioFile.value.files]
        
        isAudioFileDecided.value = true
        isAudioFileValid.value = true
    }

    const adTaglines = ref(false)

    const adTagAOBspot = ref(adSpot)
    const adAOBsched = ref(adSchedule)
    const adAOBschedList = ref(adScheduleList)
    const pushToAOBschedList = () => {
        adAOBschedList.value = adAOBsched.value.split(",") //(/[, ]+/)separate comma or space
    }

    const adTagTCspot = ref(0)
    const adTCsched = ref("")
    const adTCschedList = ref([])
    const pushToTCschedList = () => {
        adTCschedList.value = adTCsched.value.split(",") //(/[, ]+/)separate comma or space
    }

    const adTagSSspot = ref(0)
    const adSSsched = ref("")
    const adSSschedList = ref([])
    const pushToSSschedList = () => {
        adSSschedList.value = adSSsched.value.split(",") //(/[, ]+/)separate comma or space
    }


    const adAE = ref("")
    const accountExecutives = ref([])
    const getAccountExecutuves = async () => {
        const response = await axios.get("/users/")
        return accountExecutives.value = response.data
    }
 

    const submitEnabled = ref(false)
    setInterval(() => {
        if(
        isTitleValid.value &&
        isAdvertiserValid.value &&
        isContractValid.value &&
        isAmountValid.value &&
        isStartValid.value &&
        isEndValid.value &&
        isSpotValid.value &&
        isMaterialDurationValid.value&&
        adAE.value
        )submitEnabled.value = true
        else submitEnabled.value = false
    }, 1000);

    

    
    const setDefault = ()=> {
        display.value = "composition"
        adTitle.value = ""
        isTitleValid.value = false
        titleError.value = ""
        isTitleDecided.value = false
        adType.value = ""
        adAdvertiser.value = ""
        isAdvertiserValid.value = false
        advertiserError.value = ""
        isAdvertiserDecided.value = false
        searchedAdvertisers.value = []
        adContract.value = ""
        isContractValid.value = false
        contractError.value = ""
        isContractDecided.value = false
        adBONum.value = ""
        isBOValid.value = false
        boError.value = ""
        isBODecided.value = false
        adPricing.value = ""
        exDeal.value = false
        adAmount.value = 0
        isAmountValid.value = false
        amountError.value = ""
        isAmountDecided.value = false
        totalPrice.value = ""
        adStart.value = ""
        isStartValid.value = false
        startError.value = ""
        isStartDecided.value = false
        adEnd.value = ""
        isEndValid.value = false
        endError.value = ""
        isEndDecided.value = false
        totalBroadcastRange.value = ""
        adSpot.value = 0
        isSpotValid.value = false
        spotError.value = ""
        isSpotDecided.value = false
        adSchedule.value = ""
        adScheduleList.value = []
        adMaterialDuration.value = ""
        isMaterialDurationValid.value = false
        materialDurationError.value = ""
        isMaterialDurationDecided.value = false
        multiplVersions.value = false
        adAudioFile.value = ""
        uploadedFiles.value = []
        isAudioFileValid.value = false
        audioFileError.value = ""
        isAudioFileDecided.value = false
        audioFileURL.value = ""
        audioFileTemp.value = ""
        adTaglines.value = false

        adTagAOBspot.value = 0
        adAOBsched.value = ""
        adAOBschedList.value = []
        adTagTCspot.value = 0
        adTCsched.value = ""
        adTCschedList.value = []
        adTagSSspot.value = 0
        adSSsched.value = ""
        adSSschedList.value = []
        submitEnabled.value = false
        adAE.value = ""
        accountExecutives.value = []
    }


    const submitNewAds = async () => {
        const fd = new FormData()
        const userstore = userStore()
        fd.append("uploader",userstore.user)
        fd.append("duration",totalBroadcastRange.value)


        fd.append("title",adTitle.value)
        fd.append("contract",adContract.value)
        fd.append("type",adType.value)
        fd.append("ex_deal",exDeal.value)
        fd.append("pricing",adPricing.value)
        fd.append("amount",adAmount.value)
        fd.append("bo_number",adBONum.value)
        fd.append("advertiser",adAdvertiser.value)
        fd.append("broadcast_start",adStart.value)
        fd.append("broadcast_end",adEnd.value)
        fd.append("ad_spots",adSpot.value)
        fd.append("schedule",adSchedule.value)
        fd.append("has_tagline",adTaglines.value)
        fd.append("aob_spots",adTagAOBspot.value)
        fd.append("aob_sched",adAOBsched.value)
        fd.append("tc_spots",adTagTCspot.value)
        fd.append("tc_sched",adTCsched.value)
        fd.append("ss_spots",adTagSSspot.value)
        fd.append("ss_sched",adSSsched.value)
        fd.append("account_executive",adAE.value)
        fd.append("material_duration",adMaterialDuration.value )

  


        
        uploadedFiles.value.forEach(file => {
            fd.append("files",file,file.name)
        })

        const response = await axios.post("/new_ads", fd)
        if(response.status === 200){
            open.value = false
            setDefault()
        }
    }
    onMounted(() => {
        getAccountExecutuves()
    })
 
</script>



<style>
    .w-ads {
        width: 25rem;
    }
    #newads-scroll::-webkit-scrollbar {
        width: 4px;
        cursor: pointer;
        /*background-color: rgba(229, 231, 235, var(--bg-opacity));*/

    }
    #newads-scroll::-webkit-scrollbar-track {
        /* background-color: rgba(229, 231, 235, var(--bg-opacity)); */
        cursor: pointer;
        background: #c0b5a0;
    }
    #newads-scroll::-webkit-scrollbar-thumb {
        cursor: pointer;
        background-color: rgb(109, 79, 4);
        /*outline: 1px solid slategrey;*/
    }
  </style>