import { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Chatbot from "./pages/Chatbot";

function App() {
  const [count, setCount] = useState(0);

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Chatbot />} />
      </Routes>
    </Router>
  );
}

export default App;
