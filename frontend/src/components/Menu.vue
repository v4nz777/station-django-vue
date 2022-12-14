<template>
    <div class="relative flex items-center justify-center">
        <button @click="toggle()" id="menu-opener">
            <i class="block h-9 w-9">
                <MenuIcon />
            </i>
        </button>
    <div class="absolute left-0 top-0 bg-white w-max h-max z-10 mt-12 b-border shadow-lg
                flex flex-col"
            v-if="open"
            v-click-away="toggle">
            <SideBar />
            <!-- <div class="flex flex-col justify-between">
            <SidebarItem title="Activities" location="/">
                <template #icon><HashtagIcon/></template>
            </SidebarItem>

            <SidebarItem title="Worktab">
                <template #icon><HashtagIcon/></template>
            </SidebarItem>

            <SidebarItem title="About" location="/about/">
                <template #icon><HashtagIcon/></template>
            </SidebarItem>
            </div> -->
            <hr>
            <div class="flex flex-col pt-12 m-4 justify-center items-center">
                <RouterLink v-if="userstore.user" to="/profile/">
                    <div class="flex flex-col justify-center items-center">
                        <div class="m-1 rounded-full overflow-hidden mx-auto
                                    h-9 w-9 flex justify-center items-center
                                    border-solid border-yellow-500 border-x-2 border-y-2 shadow-sm shadow-black">
                            <img :src="userstore.avatar" class="object-cover w-full h-full">
                        </div>
                        <span class="text-gray-900 text-sm font-light">{{userstore.userDetails.first_name}} {{userstore.userDetails.last_name}}</span>
                        <DTRTimer />
                    </div>
                </RouterLink>
                <hr>
                <Logout />
            </div>

    </div>
    </div>
</template>
<script setup>
    import { MenuIcon } from '@heroicons/vue/outline';
    import Logout from "@/components/Logout.vue";
    import DTRTimer from "@/components/DTRTimer.vue";
    import { userStore } from '../stores/user';
    import { ref } from 'vue';
    import SideBar from "@/components/Sidebar.vue"


    const userstore = userStore()
    const open = ref(false)

    const toggle = () => {
        // open if closed -> close if opened
        open.value ? open.value=false : open.value=true
    }

</script>