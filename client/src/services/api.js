import axios from 'axios'

const API_URL = 'http://localhost:5000/chat'

export const sendMessage = async(message)  => {
    try {
        const response = await axios.post(API_URL,{message})
        return response.data.response
    } catch(error){
        console.error("Error connecting with Backend", error)
        return "Sorry , could  not process your request. "
    }
}