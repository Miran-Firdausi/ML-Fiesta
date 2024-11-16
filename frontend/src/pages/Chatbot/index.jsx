import React, { useState, useEffect, useRef } from "react";
import { IoSend, IoMic, IoMicOff } from "react-icons/io5";
import Header from "../../components/Header";
import "./Chatbot.css";

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isListening, setIsListening] = useState(false);
  const chatContainerRef = useRef(null);

  // Initialize SpeechRecognition
  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = SpeechRecognition ? new SpeechRecognition() : null;

  // Automatically scroll to the latest message
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  // Handle speech recognition result
  useEffect(() => {
    if (recognition) {
      recognition.continuous = false;
      recognition.interimResults = false;

      recognition.onresult = (event) => {
        const speechResult = event.results[0][0].transcript;
        setInput(speechResult); // Set recognized speech as input
      };

      recognition.onerror = (event) => {
        console.error("Speech Recognition Error:", event.error);
        setIsListening(false);
      };

      recognition.onend = () => setIsListening(false);
    }
  }, [recognition]);

  const handleSend = () => {
    if (!input.trim()) return;

    // Add user's message to chat history
    const newMessages = [...messages, { text: input, sender: "user" }];
    setMessages(newMessages);
    setInput("");

    // Simulate bot response
    setTimeout(() => {
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: `Echo: ${input}`, sender: "bot" },
      ]);
    }, 1000);
  };

  const handleMicClick = () => {
    if (recognition) {
      if (isListening) {
        recognition.stop();
      } else {
        recognition.start();
      }
      setIsListening((prevState) => !prevState);
    } else {
      alert("Speech recognition is not supported in this browser.");
    }
  };

  return (
    <div className="chatbot-fullscreen">
      <Header />
      <div className="chat-container" ref={chatContainerRef}>
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            {msg.text}
          </div>
        ))}
      </div>
      <div className="input-container">
        <div className="input-area">
          <button
            onClick={handleMicClick}
            className={`mic-button ${isListening ? "listening" : ""}`}
          >
            {isListening ? <IoMicOff /> : <IoMic />}
          </button>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message..."
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <button onClick={handleSend} className="send-button">
            <IoSend />
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;
