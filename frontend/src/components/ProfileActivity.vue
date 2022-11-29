<template>
    <div class="flex flex-col w-96 py-8 bg-white justify-center shadow-md rounded-3xl mx-auto mt-8 mb-16 px-4"
        v-if="activitystore.userActivities">
            <span class="text-gray-900 font-black text-center text-lg">Your Activities</span>
        <hr class="my-2">
        <div class="flex flex-col">
            <div v-for="i in activitystore.userActivities"
            class="text-gray-500 font-sans my-4 flex items-center">
                <div class="w-10 h-10 border-2 border-gray-300 rounded-full flex item-center justify-center overflow-hidden mr-2 shadow-sm shadow-black">
                    <img :src="activitystore.setAvatar(i.userpic)" alt="" class="object-cover w-full h-full">
                </div>
                <div>
                    <div>
                        <span class="font-bold">{{activitystore.humanizeUser(i.username)}}</span> 
                        {{i.other.type === "profile_modify" && i.username === userstore.user? "changed your avatar" : i.subject }} 
                        {{activitystore.humanizeDate(i.created)}}
                    </div>
                    <div class="text-blue-200 text-sm"
                        v-if="i.other.type==='login'">
                        was recorded in daily time records
                    </div>
                    <div class="text-blue-200 text-sm"
                        v-else-if="i.other.type==='relogin'">
                        not recorded in daily time records
                    </div>
                    <div class="text-blue-200 text-sm"
                        v-else-if="i.other.type==='logout'">
                        recorded in daily time records
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup>
    import { activityStore } from '@/stores/activity';
    import { userStore } from '@/stores/user';

    const userstore = userStore()
    const activitystore = activityStore()
    
    activitystore.getUserActivity()

</script>