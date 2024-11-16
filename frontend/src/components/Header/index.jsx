import React from "react";
import "./Header.css";

const Header = () => {
  return (
    <header className="header">
      <div className="header-logo">ML-Fiesta</div>
      <div className="header-title">Sandalwood Cultivation Chatbot</div>
      <button className="header-button">Login</button>
    </header>
  );
};

export default Header;
