import { useState } from "react";

function Login({ onLogin, onSignup }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/auth/login",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: email,
            password: password,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Login failed."
        );
      }

      // Save JWT
      localStorage.setItem(
        "access_token",
        data.access_token
      );

      // Login successful
      onLogin();

    } catch (error) {
      console.error("Login failed:", error);
      alert(error.message);
    }
  };

  return (
    <div className="min-h-screen bg-[#090a0d] text-white flex items-center justify-center px-5 py-10">

      <div className="w-full max-w-5xl min-h-150 grid md:grid-cols-2 rounded-2xl overflow-hidden border border-white/10 bg-[#111316] shadow-2xl">

        {/* LEFT SIDE */}
        <div className="hidden md:flex relative flex-col justify-between p-10 bg-linear-to-br from-[#17121f] via-[#111318] to-[#090a0d]">

          <div className="absolute -top-32 -left-32 w-80 h-80 bg-purple-600/20 blur-[100px] rounded-full"></div>

          <div className="relative z-10">

            {/* Logo */}
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-linear-to-br from-purple-500 to-violet-700 flex items-center justify-center font-bold text-lg">
                CF
              </div>

              <span className="text-2xl font-semibold">
                Cine<span className="text-purple-400">Forge</span>
              </span>
            </div>

            <div className="mt-28">
              <p className="text-purple-400 text-sm font-medium mb-4">
                AI FILMMAKING STUDIO
              </p>

              <h1 className="text-4xl lg:text-5xl font-bold leading-tight">
                Turn your ideas
                <br />
                into <span className="text-purple-400">cinema.</span>
              </h1>

              <p className="mt-6 text-gray-400 max-w-md leading-relaxed">
                Create stories, develop scenes and bring your imagination
                to life with AI-powered filmmaking.
              </p>
            </div>
          </div>

          <p className="relative z-10 text-xs text-gray-600">
            © 2026 CineForge. AI Filmmaking Workspace.
          </p>
        </div>

        {/* RIGHT SIDE */}
        <div className="flex items-center justify-center p-7 sm:p-12">

          <div className="w-full max-w-md">

            {/* Mobile logo */}
            <div className="flex md:hidden items-center gap-3 mb-12">
              <div className="w-10 h-10 rounded-xl bg-linear-to-br from-purple-500 to-violet-700 flex items-center justify-center font-bold">
                CF
              </div>

              <span className="text-2xl font-semibold">
                Cine<span className="text-purple-400">Forge</span>
              </span>
            </div>

            <div className="mb-8">
              <h2 className="text-3xl font-bold">
                Welcome back
              </h2>

              <p className="text-gray-500 mt-2">
                Sign in to continue creating your film.
              </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-5">

              {/* Email */}
              <div>
                <label className="block text-sm text-gray-300 mb-2">
                  Email
                </label>

                <input
                  type="email"
                  placeholder="you@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="w-full h-12 px-4 rounded-lg bg-[#191c20] border border-white/10 outline-none text-white placeholder:text-gray-600 focus:border-purple-500 transition"
                />
              </div>

              {/* Password */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <label className="text-sm text-gray-300">
                    Password
                  </label>

                  <button
                    type="button"
                    className="text-xs text-purple-400 hover:text-purple-300"
                  >
                    Forgot password?
                  </button>
                </div>

                <input
                  type="password"
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  className="w-full h-12 px-4 rounded-lg bg-[#191c20] border border-white/10 outline-none text-white placeholder:text-gray-600 focus:border-purple-500 transition"
                />
              </div>

              {/* Login */}
              <button
                type="submit"
                className="w-full h-12 rounded-lg bg-linear-to-r from-purple-600 to-violet-600 hover:from-purple-500 hover:to-violet-500 transition font-medium shadow-lg shadow-purple-900/20"
              >
                Sign In
              </button>

            </form>

            {/* Signup */}
            <p className="text-center text-sm text-gray-500 mt-7">
              Don't have an account?{" "}

              <button
                type="button"
                onClick={onSignup}
                className="text-purple-400 hover:text-purple-300 font-medium"
              >
                Create account
              </button>
            </p>

          </div>
        </div>

      </div>
    </div>
  );
}

export default Login;