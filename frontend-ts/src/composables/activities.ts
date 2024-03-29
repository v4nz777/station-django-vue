
import { userStore } from "@/stores/user"
import { ref } from "vue"

/** Reactive data of activities instances */
export const activityData = ref(null)

/** Open WebSocket Connection for `sockets/activities` */
export const openActivitiesConnection = ()=> {
    const socket = new WebSocket(`${import.meta.env.VITE_DJANGO_SERVER_WEBSOCKET_URL}/sockets/activities`)
    socket.addEventListener('message',(e)=> {
        const response = JSON.parse(e.data)
        activityData.value = response.message
    })
    return socket
}


/** Send data to the WebSocket channel */
export const sendActivity = (socketInstance:WebSocket,subject:string)=> {
    console.log('sent')
    const userstore = userStore()
    socketInstance.send(JSON.stringify({
        'user': userstore.user,
        'subject': subject
    }))
}


