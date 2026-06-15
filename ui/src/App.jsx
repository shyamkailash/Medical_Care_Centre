import { useState } from "react";
import axios from "axios";
import "./App.css";

import logo from "./assets/medfliq-logo.png";
import icon from "./assets/icon.png";

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Hello! I am your AI Medical Assistant. Tell me your symptoms.",
    },
  ]);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userText = input.trim();

    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text: userText,
      },
    ]);

    setHistory((prev) => {
      const updatedHistory = [
        userText,
        ...prev.filter((item) => item !== userText),
      ];

      return updatedHistory.slice(0, 8);
    });

    setInput("");
    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:8000/chat", {
        message: userText,
      });

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: res.data.response || "No response received.",
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "Backend connection failed. Please start FastAPI server.",
        },
      ]);
    }

    setLoading(false);
  };

  const startNewChat = () => {
    setMessages([
      {
        sender: "bot",
        text: "Hello! I am your AI Medical Assistant. Tell me your symptoms.",
      },
    ]);
  };

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="logo-section">
          <div className="brand-row">
            <img src={icon} alt="icon" className="brand-icon" />
            <img src={logo} alt="MEDFLIQ" className="logo-img" />
          </div>

          <p>
            <b>Healthcare Assistant</b>
          </p>
        </div>

        <div className="status">● Backend Connected</div>

        <button className="new-chat-btn" onClick={startNewChat}>
          + New Chat
        </button>

        <div className="history-section">
          <h3>Recent Searches</h3>

          {history.length === 0 ? (
            <p className="empty-history">No searches yet</p>
          ) : (
            history.map((item, index) => (
              <div
                key={index}
                className="history-item"
                onClick={() => setInput(item)}
              >
                {item}
              </div>
            ))
          )}
        </div>
      </aside>

      <main className="chat-section">
        <div className="header">
          <h2>AI Medical Chatbot</h2>
          <p>Powered by Qwen2.5 + FastAPI</p>
        </div>

        <div className="chat-box">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={msg.sender === "user" ? "user-msg" : "bot-msg"}
            >
              {msg.text}
            </div>
          ))}

          {loading && <div className="bot-msg">Thinking...</div>}
        </div>

        <div className="input-area">
          <textarea
            placeholder="Describe your symptoms..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
              }
            }}
          />

          <button onClick={sendMessage}>Send</button>
        </div>
      </main>
    </div>
  );
}

export default App;