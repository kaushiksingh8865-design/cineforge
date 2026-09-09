import { useState } from "react";

import About from "./pages/About";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Studio from "./pages/Studio";

function App() {
  const [page, setPage] = useState(() => {
    const token = localStorage.getItem("access_token");

    if (token) {
      return "studio";
    }

    return "about";
  });

  // Login successful → Studio
  const handleLogin = () => {
    setPage("studio");
  };

  // Signup successful → Login
  const handleSignup = () => {
    setPage("login");
  };

  // Logout → remove JWT and return to About
  const handleLogout = () => {
    localStorage.removeItem("access_token");
    setPage("about");
  };

  // ABOUT PAGE
  if (page === "about") {
    return (
      <About
        onLogin={() => setPage("login")}
        onSignup={() => setPage("signup")}
      />
    );
  }

  // LOGIN PAGE
  if (page === "login") {
    return (
      <Login
        onLogin={handleLogin}
        onSignup={() => setPage("signup")}
      />
    );
  }

  // SIGNUP PAGE
  if (page === "signup") {
    return (
      <Signup
        onSignup={handleSignup}
        onLogin={() => setPage("login")}
      />
    );
  }

  // STUDIO PAGE
  if (page === "studio") {
    return (
      <Studio
        onLogout={handleLogout}
      />
    );
  }

  // Fallback
  return (
    <div className="flex min-h-screen items-center justify-center bg-[#08090c] text-white">
      <div className="text-center">
        <h1 className="text-2xl font-bold">
          Something Went Wrong
        </h1>

        <p className="mt-2 text-gray-400">
          Error - Website is Under Service
        </p>
      </div>
    </div>
  );
}

export default App;