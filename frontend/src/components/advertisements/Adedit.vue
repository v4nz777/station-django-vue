<template>

    <div class="w-full h-5/6 overflow-y-scroll none-scroll pt-3">
                        <!-- :Title: -->
                        <div class="my-3 w-96 text-right px-11">
                            <label for="adTitle" class="text-white px-2 py-1 w-full rounded-l-md
                                shadow-md text-sm mr-1 bg-gray-500">Title: </label>
                            <input type="text" v-model="adTitle" class="bg-gray-300 focus-visible:outline-2 
                                focus-within:outline-gray-500 font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                text-gray-900 focus-within:bg-gray-100" disabled>
                        </div>
    
                        
                        
                        <!-- :Advertiser: -->
                        <div class="my-3 w-96 text-right px-11">
                            <label for="adAdvertiser" class="text-white px-2 py-1 w-full rounded-l-md
                                shadow-md text-sm mr-1 bg-gray-500">Advertiser: </label>
                            <div class="inline-block relative">
                                <input type="text" v-model="adAdvertiser" class="bg-gray-300 focus-visible:outline-2 
                                    focus-within:outline-gray-500 font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                    text-gray-900 focus-within:bg-gray-100" disabled>
                            </div>
                        </div>
            
                        <!-- :Type: -->
                        <div class="my-3 w-96 text-right px-11">
                            <label for="adType" class="text-white px-2 py-1 w-full rounded-l-md
                                shadow-md text-sm mr-1"
                                :class="adType? 'bg-gray-500':'bg-gray-300' ">Type: </label>
                            <select v-model="adType" class="bg-gray-300 focus-visible:outline-2 
                                focus-within:outline-gray-500 font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                text-gray-900 focus-within:bg-gray-100" disabled>
                                <option value="local">Local</option>
                                <option value="national">National</option>
                            </select>
                        </div>
                        
                        <!-- :Contract: -->
                        <div class="my-3 w-96 text-right px-11">
                            <label for="adContract" class="text-white px-2 py-1 w-full rounded-l-md
                                shadow-md text-sm mr-1"
                                :class="adContract? 'bg-gray-500':'bg-gray-300' ">{{adType === 'local'?'Contract:':'IM:'}}</label>
                            <input type="text" v-model="adContract" class="bg-gray-300 focus-visible:outline-2 
                                focus-within:outline-gray-500 font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                text-gray-900 focus-within:bg-gray-100" disabled>
                     
                        <hr class="my-5" v-if="adType === 'local'">
                        </div>
                        <!-- :BO Number: -->
                        <div class="my-3 w-96 text-right px-11" v-if="adType == 'national'">
                            <label for="adBONum" class="text-white px-2 py-1 w-full rounded-l-md
                                shadow-md text-sm mr-1 bg-gray-500">B.O. Number: </label>
                            <input type="text" v-model="adBONum" class="bg-gray-300 focus-visible:outline-2 
                                focus-within:outline-gray-500 font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                text-gray-900 focus-within:bg-gray-100" disabled>

                            <hr class="my-5" v-if="adType === 'national'">
                        </div>
                        <!-- :Ex Deal: -->
                        <div class="my-3 w-96 text-right px-11">
                            <label for="exDeal" class="text-blue-500 px-2 py-1 w-full text-sm mr-1">This is an ex-deal </label>
                            <input id="exDeal" type="checkbox" v-model="exDeal" class="w-4 h-4 border-blue align-bottom">
                        </div>
                        <!-- :Pricing: -->
                        <div class="my-3 w-96 text-right px-11">
                            <label for="adPricing" class="text-white px-2 py-1 w-full rounded-l-md
                                shadow-md text-sm mr-1"
                                :class="adPricing? 'bg-blue-500':'bg-blue-300' ">Pricing: </label>
                            <select name="" id="adPricing" v-model="adPricing" class="bg-blue-300 focus-visible:outline-2 
                                focus-within:outline-blue-500 font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                text-blue-900 focus-within:bg-blue-100"
                                @change="summarizeBroadcast">
                                <option value="monthly">Monthly</option>
                                <option value="daily">Daily</option>
                                <option value="fixed">Fixed</option>
                            </select>
                            <div class="inline-block ml-1" v-if="adPricing">
                                <i class="inline-block w-4 h-4 text-blue-500"><CheckCircleIcon/></i>
                            </div>
                        </div>
                        <!-- :Amount: -->
                        <div class="my-3 w-96 text-right px-11" v-if="adPricing">
                            <label for="adAmount" class="text-white px-2 py-1 w-full rounded-l-md
                                shadow-md text-sm mr-1"
                                v-if="adPricing === 'monthly'"
                                :class="adAmount? 'bg-blue-500':'bg-blue-300' ">₱ per month: </label>
                            <label for="adAmount" class="text-white px-2 py-1 w-full rounded-l-md
                                shadow-md text-sm mr-1"
                                v-else-if="adPricing === 'daily'"
                                :class="adAmount? 'bg-blue-500':'bg-blue-300' ">₱ per day: </label>
                            <label for="adAmount" class="text-white px-2 py-1 w-full rounded-l-md
                                shadow-md text-sm mr-1"
                                v-else-if="adPricing === 'fixed'"
                                :class="adAmount? 'bg-blue-500':'bg-blue-300' ">₱ in total: </label>
                            <input type="text" v-model="adAmount" class="bg-blue-300 focus-visible:outline-2 
                                focus-within:outline-blue-500 font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                text-blue-900 focus-within:bg-blue-100"
                                @keyup="summarizeBroadcast"
                                @change="amountCheck">
                            <div class="inline-block ml-1" v-if="isAmountDecided">
                                <i class="inline-block w-4 h-4 text-blue-500" v-if="isAmountValid"><CheckCircleIcon/></i>
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
                                :class="adStart? 'bg-blue-500':'bg-blue-300' ">Broadcast Start: </label>
                            <input type="date" v-model="adStart" class="bg-blue-300 focus-visible:outline-2 
                                focus-within:outline-blue-500 font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                text-blue-900 focus-within:bg-blue-100"
                                @change="startCheck">
                            <div class="inline-block ml-1" v-if="isStartDecided">
                                <i class="inline-block w-4 h-4 text-blue-500" v-if="isStartValid"><CheckCircleIcon/></i>
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
                                :class="adEnd? 'bg-blue-500':'bg-blue-300' ">Broadcast End: </label>
                            <input type="date" v-model="adEnd" class="bg-blue-300 focus-visible:outline-2 
                                focus-within:outline-blue-500 font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                text-blue-900 focus-within:bg-blue-100"
                                @change="endCheck">
                            <div class="inline-block ml-1" v-if="isEndDecided">
                                <i class="inline-block w-4 h-4 text-blue-500" v-if="isEndValid"><CheckCircleIcon/></i>
                                <i class="inline-block w-4 h-4 text-red-500" v-if="!isEndValid"><XCircleIcon/></i>
                            </div>
                            <div class="text-xs text-red-500 text-left mx-5">
                                {{endError}}
                            </div>
                        </div>
                        <div class="my-3 w-96 text-center px-11 text-blue-500 font-light text-sm"
                            v-if="totalPrice">
                            <div><span class="font-bold">₱{{totalPrice}}.00</span> in total</div>
                            <div>will run for <span class="font-bold">{{totalBroadcastRange}}</span></div>
                        </div>
                        <hr class="my-5">
                        <!-- :Spots/day: -->
                        <div class="my-3 w-96 text-right px-11">
                            <label for="adSpot" class="text-white px-2 py-1 w-full rounded-l-md
                                shadow-md text-sm mr-1"
                                :class="adSpot? 'bg-blue-500':'bg-blue-300' ">Spots/day: </label>
                            <input type="number" v-model="adSpot" class="bg-blue-300 focus-visible:outline-2 
                                focus-within:outline-blue-500 font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                text-blue-900 focus-within:bg-blue-100"
                                @change="spotCheck">
                            <div class="inline-block ml-1" v-if="isSpotDecided">
                                <i class="inline-block w-4 h-4 text-blue-500" v-if="isSpotValid"><CheckCircleIcon/></i>
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
                                :class="adSchedule? 'bg-blue-500':'bg-blue-300' ">Schedule: </label>
                            <input type="text" v-model="adSchedule" class="bg-blue-300 focus-visible:outline-2 
                                focus-within:outline-blue-500 font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                text-blue-900 focus-within:bg-blue-100"
                                placeholder="ex: 6:10am,7:40am"
                                @keyup="pushToScheduleList">
                            <div class="inline-block ml-1" v-if="adSchedule">
                                <i class="inline-block w-4 h-4 text-blue-500" v-if="adSpot === adScheduleList.length"><CheckCircleIcon/></i>
                                <i class="inline-block w-4 h-4 text-red-500" v-else><XCircleIcon/></i>
                            </div>
                            <div class="text-xs text-red-500 text-right mx-5"
                            v-if="adSpot !== adScheduleList.length && adSchedule">
                                {{adSpot}} is allowed, you provided {{adScheduleList.length}}
                            </div>
                            <div class="grid grid-cols-4 p-6 my-2 bg-blue-100"
                                v-if="adSchedule">

                                <div v-for="i in adScheduleList"
                                class="bg-blue-400 w-full shadow-sm border rounded-xl
                                text-xs text-center text-white font-extralight py-1">
                                    {{i}}
                                </div>
                            </div>
                        </div>
                        <hr class="my-5">

                       
                        <!-- :MaterialDuration: -->
                        <div class="my-3 w-96 text-right px-10">
                            <label for="adMaterialDuration" class="text-white px-2 py-1 w-full rounded-l-md
                                shadow-md text-sm mr-1"
                                :class="adMaterialDuration? 'bg-blue-500':'bg-blue-300' ">Duration(seconds): </label>
                            <input type="text" v-model="adMaterialDuration" class="bg-blue-300 focus-visible:outline-2 
                                focus-within:outline-blue-500 font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                text-blue-900 focus-within:bg-blue-100 w-20"
                                @change="materialDurationCheck">
                            <div class="inline-block ml-1" v-if="isMaterialDurationDecided">
                                <i class="inline-block w-4 h-4 text-blue-500" v-if="isMaterialDurationValid"><CheckCircleIcon/></i>
                                <i class="inline-block w-4 h-4 text-red-500" v-if="!isMaterialDurationValid"><XCircleIcon/></i>
                            </div>
                            <div class="text-xs text-red-500 text-left mx-5">
                                {{materialDurationError}}
                            </div>
                        </div>
                        <hr class="my-5">
                        <!-- AudioFiles -->
                        
                        <ul class="w-full h-max bg-blue-100 p-10">
                            <div class="flex" v-for="audio, index in audioMaterials">
                                <AudioItem :id="audio" :index="index"/>
                                <button @click="addToForDelete(audio,index)">
                                    <i class="inline-block align-middle w-6 h-6 text-red-500 hover:text-red-800">
                                        <TrashIcon/>
                                    </i>
                                </button>
                            </div>
                        </ul>

                        <div class="my-3 w-96 text-right px-11">
                            <label for="adAudioFile" class="text-white px-2 py-1 w-full rounded-l-md
                                shadow-md text-sm mr-1"
                                :class="uploadedFiles.length? 'bg-blue-500':'bg-blue-300' ">Add: </label>
                            <input type="file" ref="adAudioFile" accept="audio/*" class="hidden" @change="audioFileCheck" multiple>
                            <button class="bg-blue-300 focus-visible:outline-2 
                                focus-within:outline-blue-500 font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                text-blue-900 focus-within:bg-blue-100"
                                @click="$refs.adAudioFile.click">Upload</button>
                            <div class="inline-block ml-1" v-if="isAudioFileDecided">
                                <i class="inline-block w-4 h-4 text-blue-500" v-if="isAudioFileValid"><CheckCircleIcon/></i>
                                <i class="inline-block w-4 h-4 text-red-500" v-if="!isAudioFileValid"><XCircleIcon/></i>
                            </div>
                            <ul class="text-xs text-blue-500 text-right mx-1"
                            v-if="adAudioFile">
                                <li v-for="file,index in uploadedFiles">
                                    {{file.name.length > 25? `${file.name.substring(0,25)}...${file.name.substring(file.name.length-3,file.name.length)}`: file.name}}
                                    <button @click="removeFromFiles(file,index)"
                                    class="text-blue-500 hover:bg-red-500 hover:text-white rounded-full w-4 h-4 font-bold text-center">x</button>
                                </li>
                            </ul>
                            <div class="text-xs text-red-500 text-right mx-5">
                                {{audioFileError}}
                            </div>
                        </div>
                            
                        
                        <hr class="my-5">

                        <!-- :Taglines: -->
                        <div class="my-3 w-96 text-right px-11">
                            <label for="adTaglines" class="text-blue-500 px-2 py-1 w-full text-sm mr-1">This ad has taglines? (e.g: aob,ss,tc) </label>
                            <input id="adTaglines" type="checkbox" v-model="adTaglines" class="w-4 h-4 border-blue align-bottom">
                            <div v-if="adTaglines" class="my-2">
                                <!-- /AOB/ -->
                                <div class="mt-6">
                                    <label for="adTagAOBspot" class="text-white px-2 py-1 w-full rounded-l-md
                                    shadow-md text-sm mr-1"
                                    :class="adTagAOBspot? 'bg-blue-500':'bg-blue-300' ">AOB spots/day</label>
                                    <input type="number" v-model="adTagAOBspot" id="adTagAOBspot"
                                        class="bg-blue-300 focus-visible:outline-2 
                                        focus-within:outline-blue-500 font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                        text-blue-900 focus-within:bg-blue-100 w-20">
                                    <div class="text-xs text-blue-500 text-right mx-5">
                                        leave blank if none
                                    </div>
                                </div>
                                <div v-if="adTagAOBspot" class="mt-2">
                                    <label for="adAOBsched" class="text-white px-2 py-1 w-full rounded-l-md
                                    shadow-md text-sm mr-1"
                                    :class="adAOBsched? 'bg-blue-500':'bg-blue-300' ">Schedule:</label>
                                    <input type="text" id="adAOBsched" v-model="adAOBsched"
                                        
                                        @keyup="pushToAOBschedList"
                                        class="bg-blue-300 focus-visible:outline-2 
                                        focus-within:outline-blue-500 font-thin text-sm px-2 py-1 shadow-md 
                                        rounded-r-md text-blue-900 focus-within:bg-blue-100">
                                        <div class="inline-block ml-1" v-if="adAOBsched">
                                            <i class="inline-block w-4 h-4 text-blue-500" v-if="adTagAOBspot === adAOBschedList.length"><CheckCircleIcon/></i>
                                            <i class="inline-block w-4 h-4 text-red-500" v-else><XCircleIcon/></i>
                                        </div>
                                        <div class="text-xs text-red-500 text-right mx-5"
                                        v-if="adTagAOBspot !== adAOBschedList.length && adAOBsched">
                                            {{adTagAOBspot}} is allowed, you provided {{adAOBschedList.length}}
                                        </div>
                                    <div class="grid grid-cols-4 p-6 my-2 bg-blue-100"
                                    v-if="adAOBsched">
                                        <div v-for="i in adAOBschedList"
                                            class="bg-blue-400 w-full shadow-sm border rounded-xl
                                            text-xs text-center text-white font-extralight py-1">
                                            {{i}}
                                        </div>
                                    </div>
                                </div>
                                <!-- /TC/ -->
                                <div class="mt-6">
                                    <label for="adTagTCspot" class="text-white px-2 py-1 w-full rounded-l-md
                                    shadow-md text-sm mr-1"
                                    :class="adTagTCspot? 'bg-blue-500':'bg-blue-300' ">TC spots/day</label>
                                    <input type="number" v-model="adTagTCspot" id="adTagTCspot"
                                        class="bg-blue-300 focus-visible:outline-2 
                                        focus-within:outline-blue-500 font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                        text-blue-900 focus-within:bg-blue-100 w-20">
                                    <div class="text-xs text-blue-500 text-right mx-5">
                                        leave blank if none
                                    </div>
                                </div>
                                <div v-if="adTagTCspot" class="mt-2">
                                    <label for="adTCsched" class="text-white px-2 py-1 w-full rounded-l-md
                                    shadow-md text-sm mr-1"
                                    :class="adTCsched? 'bg-blue-500':'bg-blue-300' ">Schedule:</label>
                                    <input type="text" id="adTCsched" v-model="adTCsched"
                                        placeholder="ex: 6:00am,7:00am"
                                        @keyup="pushToTCschedList"
                                        class="bg-blue-300 focus-visible:outline-2 
                                        focus-within:outline-blue-500 font-thin text-sm px-2 py-1 shadow-md 
                                        rounded-r-md text-blue-900 focus-within:bg-blue-100">
                                    <div class="inline-block ml-1" v-if="adTCsched">
                                        <i class="inline-block w-4 h-4 text-blue-500" v-if="adTagTCspot === adTCschedList.length"><CheckCircleIcon/></i>
                                        <i class="inline-block w-4 h-4 text-red-500" v-else><XCircleIcon/></i>
                                    </div>
                                    <div class="text-xs text-red-500 text-right mx-5"
                                    v-if="adTagTCspot !== adTCschedList.length && adTCsched">
                                        {{adTagTCspot}} is allowed, you provided {{adTCschedList.length}}
                                    </div>
                                    <div class="grid grid-cols-4 p-6 my-2 bg-blue-100"
                                    v-if="adTCsched">
                                        <div v-for="i in adTCschedList"
                                            class="bg-blue-400 w-full shadow-sm border rounded-xl
                                            text-xs text-center text-white font-extralight py-1">
                                            {{i}}
                                        </div>
                                    </div>
                                </div>
                                <!-- /SS/ -->
                                <div class="mt-6">
                                    <label for="adTagSSspot" class="text-white px-2 py-1 w-full rounded-l-md
                                    shadow-md text-sm mr-1"
                                    :class="adTagSSspot? 'bg-blue-500':'bg-blue-300' ">SS spots/day</label>
                                    <input type="number" v-model="adTagSSspot" id="adTagSSspot"
                                        class="bg-blue-300 focus-visible:outline-2 
                                        focus-within:outline-blue-500 font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                        text-blue-900 focus-within:bg-blue-100 w-20">
                                    <div class="text-xs text-blue-500 text-right mx-5">
                                        leave blank if none
                                    </div>
                                </div>
                                <div v-if="adTagSSspot" class="mt-2">
                                    <label for="adSSsched" class="text-white px-2 py-1 w-full rounded-l-md
                                    shadow-md text-sm mr-1"
                                    :class="adSSsched? 'bg-blue-500':'bg-blue-300' ">Schedule:</label>
                                    <input type="text" id="adSSsched" v-model="adSSsched"
                                        placeholder="ex: 6:30am,7:30am"
                                        @keyup="pushToSSschedList"
                                        class="bg-blue-300 focus-visible:outline-2 
                                        focus-within:outline-blue-500 font-thin text-sm px-2 py-1 shadow-md 
                                        rounded-r-md text-blue-900 focus-within:bg-blue-100">
                                    <div class="inline-block ml-1" v-if="adSSsched">
                                        <i class="inline-block w-4 h-4 text-blue-500" v-if="adTagSSspot === adSSschedList.length"><CheckCircleIcon/></i>
                                        <i class="inline-block w-4 h-4 text-red-500" v-else><XCircleIcon/></i>
                                    </div>
                                    <div class="text-xs text-red-500 text-right mx-5"
                                    v-if="adTagSSspot !== adSSschedList.length && adSSsched">
                                        {{adTagSSspot}} is allowed, you provided {{adSSschedList.length}}
                                    </div>
                                    <div class="grid grid-cols-4 p-6 my-2 bg-blue-100"
                                    v-if="adSSsched">
                                        <div v-for="i in adSSschedList"
                                            class="bg-blue-400 w-full shadow-sm border rounded-xl
                                            text-xs text-center text-white font-extralight py-1">
                                            {{i}}
                                        </div>
                                    </div>
                                </div>
                                <!-- /// -->
                            </div>
                        </div>
                        <hr class="my-5">

                        <!-- :Account Executive: -->
                        <div class="my-3 w-96 text-right px-11">
                            <label for="adAE" class="text-white px-2 py-1 w-full rounded-l-md
                                shadow-md text-sm mr-1"
                                :class="adAE? 'bg-blue-500':'bg-blue-300' ">AE: </label>
                            <div class="inline-block">
                                <select name="" id="adAE" v-model="adAE" class="bg-blue-300 focus-visible:outline-2 
                                    focus-within:outline-blue-500 font-thin text-sm px-2 py-1 shadow-md rounded-r-md
                                    text-blue-900 focus-within:bg-blue-100">
                                <option value="office">Office</option>
                                <option v-for="user in accountExecutives" :value="user.username">{{user.first_name}} {{user.last_name}}</option>
                                </select>
 
                            </div>
                            <div class="inline-block ml-1" v-if="adAE">
                                <i class="inline-block w-4 h-4 text-blue-500"><CheckCircleIcon/></i>
                            </div>

                        </div>
                        <!-- :: -->

                        <div class="mx-10 my-5">
                            <div v-if="savingInProgress">
                                <div class="w-8 h-8 mx-auto border-4 border-blue-500 rounded-full" id="loader"></div>
                            </div>
                            <button v-else class=" text-white w-full bg-blue-500" @click="saveAd">
                                Save
                            </button>
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
    const props = defineProps({
        ad: Object,
        versionDetails: Object,
        advertiser: Object,
        ae: String,
    })

    const adTitle = ref(props.ad.title)
    const adType = ref(props.ad.type)

    const adAdvertiser = ref(props.advertiser.name)



    const adContract = ref(props.ad.contract)


    const adBONum = ref(props.ad.bo_number)

    const adPricing = ref(props.versionDetails.pricing)
    const exDeal = ref(props.versionDetails.ex_deal)


    const adAmount = ref(props.versionDetails.amount)
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

    const adStart = ref(props.versionDetails.broadcast_start)
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

    const adEnd = ref(props.versionDetails.broadcast_end)
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

    const adSpot = ref(props.versionDetails.ad_spots)
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

    const adSchedule = ref(props.versionDetails.schedule)
    const adScheduleList = ref([])
    const pushToScheduleList = () => {
        adScheduleList.value = adSchedule.value.split(",") //(/[, ]+/)separate comma or space
        spotCheck()
    }


    const adMaterialDuration = ref(props.versionDetails.material_duration)
    const isMaterialDurationValid = ref(false)
    const materialDurationError = ref("")
    const isMaterialDurationDecided = ref(false)
    const materialDurationCheck = () => {
        if(!adMaterialDuration.value) isMaterialDurationDecided.value = false
        else isMaterialDurationDecided.value = true

        isMaterialDurationValid.value = true
    }



    const adAudioFile = ref("")
    const uploadedFiles = ref([])
    const isAudioFileValid = ref(false)
    const audioFileError = ref("")
    const isAudioFileDecided = ref(false)
    const audioFileURL = ref("")
    const audioFileTemp = ref("")
    
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
        
        if (uploadedFiles.value.length && multiplVersions.value){
            uploadedFiles.value = [...uploadedFiles.value,...adAudioFile.value.files]
        } else uploadedFiles.value = [...adAudioFile.value.files]
        
        isAudioFileDecided.value = true
        isAudioFileValid.value = true
    }

    const audioMaterials = ref(props.versionDetails.files) // read only
    const audioForDelete = ref([])             // for write
    const addToForDelete = (id,index) => {
       
        audioForDelete.value.push(id)

        audioMaterials.value.splice(index,1)

       
    }

    const adTaglines = ref(props.versionDetails.has_tagline)

    const adTagAOBspot = ref(props.versionDetails.aob_spots)
    const adAOBsched = ref(props.versionDetails.aob_sched)
    const adAOBschedList = ref([])
    const pushToAOBschedList = () => {
        adAOBschedList.value = adAOBsched.value.split(",") //(/[, ]+/)separate comma or space
    }

    const adTagTCspot = ref(props.versionDetails.tc_spots)
    const adTCsched = ref(props.versionDetails.tc_sched)
    const adTCschedList = ref([])
    const pushToTCschedList = () => {
        if(adTCsched.value){
            adTCschedList.value = adTCsched.value.split(",") //(/[, ]+/)separate comma or space
        }
    }

    const adTagSSspot = ref(props.versionDetails.ss_spots)
    const adSSsched = ref(props.versionDetails.ss_sched)
    const adSSschedList = ref([])
    const pushToSSschedList = () => {
        if(adSSsched.value){
            adSSschedList.value = adSSsched.value.split(",") //(/[, ]+/)separate comma or space
        }
    }


    const adAE = ref(props.versionDetails.account_executive)
    const accountExecutives = ref([])
    const getAccountExecutuves = async () => {
        const response = await axios.get("/users/")
        return accountExecutives.value = response.data
    }
 

    onMounted(()=>{
        getAccountExecutuves(); // get list of AEs
        pushToScheduleList();   // initialize spots schedules
        pushToAOBschedList();   // initialize aob spots sched
        pushToTCschedList();    // initialize tc spots sched
        pushToSSschedList();    // initialize ss spots sched
        startCheck();           // 
        endCheck();             //

    })

    onUnmounted(() => {
        setDefault()
    })

    const setDefault = () => {
        adTitle.value = props.ad.title
        adType.value = props.ad.type
        adAdvertiser.value = props.advertiser.name
        adContract.value = props.ad.contract
        adBONum.value = props.ad.bo_number
        adPricing.value = props.versionDetails.pricing
        exDeal.value = props.versionDetails.ex_deal
        adAmount.value = props.versionDetails.amount
        isAmountValid.value = false
        amountError.value = ""
        isAmountDecided.value = false
        totalPrice.value = ""
        adStart.value = props.versionDetails.broadcast_start
        isStartValid.value = false
        startError.value = ""
        isStartDecided.value = false
        adEnd.value = props.versionDetails.broadcast_end
        isEndValid.value = false
        endError.value = ""
        isEndDecided.value = false
        totalBroadcastRange.value = ""
        adSpot.value = props.versionDetails.ad_spots
        isSpotValid.value = false
        spotError.value = ""
        isSpotDecided.value = false
        adSchedule.value = props.versionDetails.schedule
        adScheduleList.value = []
        adMaterialDuration.value = props.versionDetails.material_duration
        isMaterialDurationValid.value = false
        materialDurationError.value = ""
        isMaterialDurationDecided.value = false
        adAudioFile.value = ""
        uploadedFiles.value = []
        isAudioFileValid.value = false
        audioFileError.value = ""
        isAudioFileDecided.value = false
        audioFileURL.value = ""
        audioFileTemp.value = ""
        audioMaterials.value = props.versionDetails.files
        audioForDelete.value = [] 
        adTaglines.value = props.versionDetails.has_tagline
        adTagAOBspot.value = props.versionDetails.aob_spots
        adAOBsched.value = props.versionDetails.aob_sched
        adAOBschedList.value = []
        adTagTCspot.value = props.versionDetails.tc_spots
        adTCsched.value = props.versionDetails.tc_sched
        adTCschedList.value = []
        adTagSSspot.value = props.versionDetails.ss_spots
        adSSsched.value = props.versionDetails.ss_sched
        adSSschedList.value = []
        adAE.value = props.versionDetails.account_executive
        accountExecutives.value = []
    }

    const savingInProgress = ref(false) 
    const emits = defineEmits(["saved"])

    const saveAd = async ()=> {

        savingInProgress.value = true

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
        
        fd.append("existing_files", audioMaterials.value)
        fd.append("files_remove", audioForDelete.value)

        uploadedFiles.value.forEach(file => {
            fd.append("files",file,file.name)
        })

        const response = await axios.post("/new_ads", fd)
        if(response.status === 200) {
            setTimeout(() => {
                setDefault()
                emits("saved")
                savingInProgress.value = false
            }, 3000);
        }
        
        


    }

</script>