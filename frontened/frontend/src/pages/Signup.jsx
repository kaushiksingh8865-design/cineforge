import { useState } from "react";

function Signup({ onSignup, onLogin }) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/auth/register",
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
          data.detail || "Registration failed."
        );
      }

      alert("Account created successfully.");

      onSignup();

    } catch (error) {
      console.error("Signup failed:", error);
      alert(error.message);
    }
  };

  return (
    <div className="min-h-screen bg-[#090a0d] text-white flex items-center justify-center px-5 py-10">

      <div className="w-full max-w-md">

        {/* Logo */}
        <div className="flex items-center justify-center gap-3 mb-10">
          <div className="w-10 h-10 rounded-xl bg-linear-to-br from-purple-500 to-violet-700 flex items-center justify-center font-bold">
            CF
          </div>

          <span className="text-2xl font-semibold">
            Cine<span className="text-purple-400">Forge</span>
          </span>
        </div>

        {/* Card */}
        <div className="bg-[#111316] border border-white/10 rounded-2xl p-7 sm:p-9">

          <div className="mb-7">
            <h1 className="text-3xl font-bold">
              Create your account
            </h1>

            <p className="text-gray-500 mt-2">
              Start creating your next film with AI.
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">

            {/* Name */}
            <div>
              <label className="block text-sm text-gray-300 mb-2">
                Full name
              </label>

              <input
                type="text"
                placeholder="Your name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                className="w-full h-12 px-4 rounded-lg bg-[#191c20] border border-white/10 outline-none focus:border-purple-500 placeholder:text-gray-600"
              />
            </div>

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
                className="w-full h-12 px-4 rounded-lg bg-[#191c20] border border-white/10 outline-none focus:border-purple-500 placeholder:text-gray-600"
              />
            </div>

            {/* Password */}
            <div>
              <label className="block text-sm text-gray-300 mb-2">
                Password
              </label>

              <input
                type="password"
                placeholder="Create a password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full h-12 px-4 rounded-lg bg-[#191c20] border border-white/10 outline-none focus:border-purple-500 placeholder:text-gray-600"
              />
            </div>

            <button
              type="submit"
              className="w-full h-12 rounded-lg bg-linear-to-r from-purple-600 to-violet-600 hover:from-purple-500 hover:to-violet-500 transition font-medium"
            >
              Create Account
            </button>

          </form>

          <p className="text-center text-sm text-gray-500 mt-7">
            Already have an account?{" "}

            <button
              type="button"
              onClick={onLogin}
              className="text-purple-400 hover:text-purple-300 font-medium"
            >
              Sign in
            </button>
          </p>

        </div>

      </div>
    </div>
  );
}

export default Signup;