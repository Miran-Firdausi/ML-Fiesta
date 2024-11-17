import React, { useState, useEffect, useRef } from "react";
import { Environment, OrbitControls } from "@react-three/drei";
import { Canvas } from "@react-three/fiber";
import { TalkingAvatar } from "../../components/TalkingAvatar";
import { IoSend, IoMic, IoMicOff } from "react-icons/io5";
import Header from "../../components/Header";
import "./Chatbot.css";

function Chatbot() {
  const [questionInput, setQuestionInput] = useState("");
  const [answer, setAnswer] = useState({});
  const [chatQuestion, setChatQuestion] = useState("ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಕೇಳಿ");
  const [isListening, setIsListening] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);

  // Initialize SpeechRecognition
  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = SpeechRecognition ? new SpeechRecognition() : null;

  // Handle speech recognition result
  useEffect(() => {
    if (recognition) {
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = "kn-IN";

      recognition.onresult = (event) => {
        const speechResult = event.results[0][0].transcript;
        setQuestionInput(speechResult); // Set recognized speech as input
      };

      recognition.onerror = (event) => {
        console.error("Speech Recognition Error:", event.error);
        setIsListening(false);
      };

      recognition.onend = () => setIsListening(false);
    }
  }, [recognition]);

  const fetchSpeech = async (answerText) => {
    try {
      const audioResponse = await fetch(`http://127.0.0.1:8000/tts/`, {
        body: JSON.stringify({
          text: answerText,
        }),
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });
      if (!audioResponse.ok) {
        throw new Error("Failed to fetch video");
      }
      const audio = await audioResponse.blob();
      const audioUrl = URL.createObjectURL(audio);
      const audioPlayer = new Audio(audioUrl);
      audioPlayer.onended = () => {
        setIsSpeaking(false);
      };

      var visemes = audioResponse.headers.get("visemes");
      visemes = JSON.parse(visemes);
      setAnswer((prev) => {
        return { ...prev, audioPlayer, visemes };
      });
      setIsSpeaking(true);

      audioPlayer.currentTime = 0;
      audioPlayer.play();
    } catch (err) {
      console.log("error" + err);
    }
  };

  const handleSend = async () => {
    if (!questionInput.trim()) return;
    setIsGenerating(true);
    try {
      const answerResponse = await fetch(`http://127.0.0.1:8000/answer/`, {
        body: JSON.stringify({
          question: questionInput,
        }),
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });
      if (!answerResponse.ok) {
        throw new Error("Failed to fetch an Answer");
      }
      setIsGenerating(false);
      const answerData = await answerResponse.json();
      console.log(answerData.answer);
      setAnswer((prev) => {
        return {
          ...prev,
          text: answerData.answer,
        };
      });
      setChatQuestion(questionInput);
      fetchSpeech(answerData.answer);
      setQuestionInput("");
    } catch (err) {
      console.log("error" + err);
    }
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
    <div className="chatbot-container">
      <Header />

      <div className="main-container">
        <div className="avatar-container">
          <Canvas
            camera={{
              zoom: 5,
            }}
          >
            <OrbitControls
              target={[0, 1.3, 0]}
              enableRotate={false}
              enablePan={false}
              enableZoom={false}
            />
            <Environment preset="sunset" />
            <ambientLight intensity={0.8} color="pink" />
            <TalkingAvatar answer={answer} isSpeaking={isSpeaking} />
          </Canvas>
        </div>
        <div className="input-container">
          <div className="input-area">
            <button
              onClick={handleMicClick}
              className={`mic-button ${isListening ? "listening" : ""}`}
              style={{ color: "#fff" }}
            >
              {isListening ? <IoMicOff /> : <IoMic />}
            </button>
            <div>
              <input
                type="text"
                value={questionInput}
                onChange={(e) => setQuestionInput(e.target.value)}
                placeholder="Type a message..."
                onKeyDown={(e) => e.key === "Enter" && handleSend()}
              />
              <button onClick={handleSend} className="send-button">
                <IoSend />
              </button>
            </div>
          </div>
        </div>
        <div className="chat-container">
          <h1>Chat</h1>
          <div className="chat">
            <p className="question">ಪ್ರಶ್ನೆ: {chatQuestion}</p>
            <p>
              ಉತ್ತರ: {isGenerating ? "ಉತ್ತರವನ್ನು ಉತ್ಪಾದಿಸುತ್ತದೆ" : answer.text}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Chatbot;
