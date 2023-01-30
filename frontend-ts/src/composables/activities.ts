
import { userStore } from "@/stores/user"
import { ref } from "vue"

/** Reactive data of activities instances */
export const activityData = ref(null)

/** Open WebSocket Connection for `sockets/activities` */
export const openActivitiesConnection = ()=> {
    const socket = new WebSocket(`ws://${location.hostname}:8000/sockets/activities`)
    socket.addEventListener('message',(e)=> {
        const response = JSON.parse(e.data)
        activityData.value = response.message
    })
    return socket
}

/** Send data to the WebSocket channel */
export const sendActivity = (socketInstance:WebSocket,subject:string)=> {
    const userstore = userStore()
    socketInstance.send(JSON.stringify({
        'user': userstore.user,
        'subject': subject
    }))
}


