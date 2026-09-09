import { useState } from "react";
import { Mail, LogOut, X, Send, Sparkles } from "lucide-react";

function Navbar() {
  const [showUserCard, setShowUserCard] = useState(false);
  const [showAIAssistant, setShowAIAssistant] = useState(false);
  const [message, setMessage] = useState("");

  // Get logged-in user from localStorage
  const getUser = () => {
    try {
      const savedUser = localStorage.getItem("user");

      if (savedUser) {
        return JSON.parse(savedUser);
      }
    } catch (error) {
      console.error("Error reading user data:", error);
    }

    // Default user
    return {
      name: "Admin",
      email: "admin@gmail.com",
    };
  };

  const user = getUser();

  const userInitial =
    user?.name?.charAt(0)?.toUpperCase() || "U";

  // Logout
  const handleLogout = () => {
    localStorage.removeItem("user");
    setShowUserCard(false);

    window.location.href = "/";
  };

  // Open AI Assistant
  const handleAIButton = () => {
    setShowAIAssistant(true);
    setShowUserCard(false);
  };

  // Close AI Assistant
  const closeAIAssistant = () => {
    setShowAIAssistant(false);
  };

  // Send AI message
  const handleSendMessage = (e) => {
    e.preventDefault();

    if (!message.trim()) return;

    console.log("AI Message:", message);

    setMessage("");
  };

  return (
    <header className="h-17.5 shrink-0 bg-[#101214] border-b border-white/10 flex items-center justify-between px-5 relative">

      {/* =====================================================
          LEFT — LOGO
      ====================================================== */}
      <div className="flex items-center">
        <div className="flex items-center gap-3">

          {/* Logo */}
          <div className="w-8 h-8 rounded-md bg-linear-to-br from-purple-500 to-violet-700 flex items-center justify-center text-sm font-bold shadow-lg shadow-purple-900/20">
            CF
          </div>

          {/* Brand Name */}
          <span className="text-lg font-semibold tracking-tight">
            Cine<span className="text-purple-400">Forge</span>
          </span>

        </div>
      </div>


      {/* =====================================================
          CENTER — WORKSPACE STATUS
      ====================================================== */}
      <div className="flex-1 flex items-center justify-center">

        <div className="flex items-center gap-2 text-sm">

          {/* Status Dot */}
          <span className="text-green-400 text-base leading-none">
            ●
          </span>

          {/* Workspace Text */}
          <span className="text-gray-300 font-medium">
            Studio Workspace
          </span>

        </div>

      </div>


      {/* =====================================================
          RIGHT — AI ASSISTANT + USER
      ====================================================== */}
      <div className="flex items-center gap-3">

        {/* AI Assistant Button */}
        <button
          type="button"
          onClick={handleAIButton}
          className="px-4 py-2 rounded-md bg-linear-to-r from-purple-600 to-violet-600 text-sm font-medium text-white hover:from-purple-500 hover:to-violet-500 transition shadow-lg shadow-purple-900/20"
        >
          ✨ AI Assistant
        </button>


        {/* =================================================
            USER PROFILE
        ================================================== */}
        <div className="relative ml-2">

          {/* User Avatar */}
          <button
            type="button"
            onClick={() => {
              setShowUserCard((prev) => !prev);
              setShowAIAssistant(false);
            }}
            aria-label="Open user profile"
            className="w-9 h-9 rounded-full p-0.5 bg-linear-to-br from-purple-400 via-violet-500 to-indigo-500 hover:from-purple-300 hover:via-violet-400 hover:to-indigo-400 transition-all duration-200 shadow-lg shadow-purple-900/20"
          >
            <div className="w-full h-full rounded-full bg-[#181a1e] flex items-center justify-center">

              <span className="text-xs font-semibold text-gray-200">
                {userInitial}
              </span>

            </div>
          </button>


          {/* =================================================
              USER PROFILE CARD
          ================================================== */}
          {showUserCard && (
            <div className="absolute right-0 top-12 z-50 w-72 overflow-hidden rounded-xl border border-white/10 bg-[#15171b] shadow-2xl shadow-black/50">

              {/* User Information */}
              <div className="p-4">

                <div className="flex items-center gap-3">

                  {/* Large Avatar */}
                  <div className="w-12 h-12 shrink-0 rounded-full bg-linear-to-br from-purple-500 to-violet-700 flex items-center justify-center shadow-lg shadow-purple-900/20">

                    <span className="text-lg font-bold text-white">
                      {userInitial}
                    </span>

                  </div>


                  {/* Name + Email */}
                  <div className="min-w-0">

                    <h3 className="text-sm font-semibold text-white">
                      Hello, {user.name}
                    </h3>

                    <div className="mt-1 flex items-center gap-1.5 text-xs text-gray-400">

                      <Mail size={13} />

                      <span className="truncate">
                        {user.email}
                      </span>

                    </div>

                  </div>

                </div>

              </div>


              {/* Divider */}
              <div className="border-t border-white/10"></div>


              {/* Logout */}
              <button
                type="button"
                onClick={handleLogout}
                className="flex w-full items-center gap-3 px-4 py-3 text-sm font-medium text-gray-300 transition hover:bg-red-500/10 hover:text-red-400"
              >

                <LogOut size={17} />

                <span>
                  Logout
                </span>

              </button>

            </div>
          )}

        </div>

      </div>


      {/* =====================================================
          AI ASSISTANT PANEL
      ====================================================== */}
      {showAIAssistant && (
        <div className="absolute right-5 top-[70px] z-50 w-[380px] overflow-hidden rounded-2xl border border-white/10 bg-[#111318] shadow-2xl shadow-black/60">

          {/* =================================================
              AI HEADER
          ================================================== */}
          <div className="flex items-center justify-between border-b border-white/10 px-5 py-4">

            <div className="flex items-center gap-3">

              {/* AI Icon */}
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-linear-to-br from-purple-500 to-violet-700 shadow-lg shadow-purple-900/30">

                <Sparkles
                  size={17}
                  className="text-white"
                />

              </div>


              {/* AI Title */}
              <div>

                <h2 className="text-sm font-semibold text-white">
                  AI Assistant
                </h2>

                <p className="text-xs text-gray-500">
                  Your filmmaking companion
                </p>

              </div>

            </div>


            {/* Close Button */}
            <button
              type="button"
              onClick={closeAIAssistant}
              aria-label="Close AI Assistant"
              className="flex h-8 w-8 items-center justify-center rounded-md text-gray-400 transition hover:bg-white/10 hover:text-white"
            >
              <X size={18} />
            </button>

          </div>


          {/* =================================================
              AI CHAT CONTENT
          ================================================== */}
          <div className="h-[330px] overflow-y-auto p-5">

            {/* AI Welcome Message */}
            <div className="flex gap-3">

              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-purple-500/15">

                <Sparkles
                  size={15}
                  className="text-purple-400"
                />

              </div>


              <div className="max-w-[270px] rounded-xl rounded-tl-none border border-white/10 bg-[#191b20] px-4 py-3">

                <p className="text-sm leading-6 text-gray-300">
                  Hello! I'm your AI filmmaking assistant.
                  How can I help you with your film?
                </p>

              </div>

            </div>


            {/* Suggested Prompts */}
            <div className="mt-6">

              <p className="mb-3 text-xs font-medium uppercase tracking-wider text-gray-500">
                Try asking
              </p>


              <div className="space-y-2">

                {/* Prompt 1 */}
                <button
                  type="button"
                  onClick={() =>
                    setMessage("Improve this scene")
                  }
                  className="w-full rounded-lg border border-white/10 bg-white/[0.02] px-4 py-3 text-left text-sm text-gray-400 transition hover:border-purple-500/30 hover:bg-purple-500/5 hover:text-gray-200"
                >
                  Improve this scene
                </button>


                {/* Prompt 2 */}
                <button
                  type="button"
                  onClick={() =>
                    setMessage(
                      "Generate ideas for this scene"
                    )
                  }
                  className="w-full rounded-lg border border-white/10 bg-white/[0.02] px-4 py-3 text-left text-sm text-gray-400 transition hover:border-purple-500/30 hover:bg-purple-500/5 hover:text-gray-200"
                >
                  Generate ideas for this scene
                </button>


                {/* Prompt 3 */}
                <button
                  type="button"
                  onClick={() =>
                    setMessage(
                      "Make this dialogue more cinematic"
                    )
                  }
                  className="w-full rounded-lg border border-white/10 bg-white/[0.02] px-4 py-3 text-left text-sm text-gray-400 transition hover:border-purple-500/30 hover:bg-purple-500/5 hover:text-gray-200"
                >
                  Make this dialogue more cinematic
                </button>

              </div>

            </div>

          </div>


          {/* =================================================
              AI INPUT
          ================================================== */}
          <div className="border-t border-white/10 p-4">

            <form
              onSubmit={handleSendMessage}
              className="flex items-center gap-2"
            >

              {/* Input */}
              <input
                type="text"
                value={message}
                onChange={(e) =>
                  setMessage(e.target.value)
                }
                placeholder="Ask your AI assistant..."
                className="min-w-0 flex-1 rounded-lg border border-white/10 bg-[#191b20] px-3 py-2.5 text-sm text-white outline-none placeholder:text-gray-600 focus:border-purple-500/50"
              />


              {/* Send Button */}
              <button
                type="submit"
                className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-gradient-to-r from-purple-600 to-violet-600 text-white transition hover:opacity-90"
              >
                <Send size={16} />
              </button>

            </form>

          </div>

        </div>
      )}

    </header>
  );
}

export default Navbar;