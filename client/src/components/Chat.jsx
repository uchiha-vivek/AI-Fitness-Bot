import React, { useState } from "react";
import axios from 'axios';

const Chat = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const API_URL = 'http://localhost:5000/chat'; // Ensure your backend is running and CORS is properly configured

  // Function to send a message to the backend
  const sendMessage = async (message) => {
    try {
      // Sending the message to the backend using Axios
      const response = await axios.post(API_URL, { message });
      // Return the response from the backend
      return response.data.response; // Adjust this if your backend structure is different
    } catch (error) {
      console.error("Error connecting with Backend:", error);
      // Returning a default error message if the request fails
      return "Sorry, could not process your request.";
    }
  };

  // Logic for handling the send action
  const handleSend = async () => {
    if (!input) return; // Prevent sending if the input is empty

    // Add the user's message to the state
    setMessages((prevMessages) => [...prevMessages, { role: 'user', content: input }]);

    // Send the message to the backend and get the response
    const response = await sendMessage(input);

    // Add the assistant's response to the state
    setMessages((prevMessages) => [...prevMessages, { role: 'assistant', content: response }]);

    // Clear the input field
    setInput('');
  };

  return (
    <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto' }}>
      <div style={{ marginBottom: '20px', border: '1px solid #ccc', padding: '10px', borderRadius: '5px', height: '300px', overflowY: 'scroll' }}>
        {/* Render messages */}
        {messages.map((msg, index) => (
          <div key={index} style={{ marginBottom: '10px' }}>
            <strong>{msg.role === 'user' ? 'You' : 'Assistant'}:</strong> {msg.content}
          </div>
        ))}
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={(e) => e.key === "Enter" ? handleSend() : null}
        placeholder="Type your message..."
        style={{ width: '80%', padding: '10px', marginRight: '5px', borderRadius: '5px', border: '1px solid #ccc' }}
      />
      <button onClick={handleSend} style={{ padding: '10px', borderRadius: '5px', border: '1px solid #ccc', cursor: 'pointer' }}>Send</button>
    </div>
  );
};

export default Chat;
