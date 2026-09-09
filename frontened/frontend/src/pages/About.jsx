function About({ onLogin, onSignup }) {
  return (
    <div className="min-h-screen bg-[#08090c] text-white">

      {/* Navbar */}
      <nav className="border-b border-white/10">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">

          {/* Logo */}
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-purple-500 to-violet-700 font-bold">
              CF
            </div>

            <span className="text-xl font-bold">
              Cine<span className="text-purple-400">Forge</span>
            </span>
          </div>

          {/* Buttons */}
          <div className="flex items-center gap-3">
            <button
              onClick={onLogin}
              className="rounded-lg border border-white/15 px-5 py-2.5 text-sm font-semibold text-gray-200 transition hover:border-purple-500 hover:text-white"
            >
              Sign In
            </button>

            <button
              onClick={onSignup}
              className="rounded-lg bg-gradient-to-r from-purple-600 to-violet-600 px-5 py-2.5 text-sm font-semibold transition hover:opacity-90"
            >
              Get Started
            </button>
          </div>

        </div>
      </nav>


      {/* Hero Section */}
      <main>

        <section className="mx-auto flex min-h-[calc(100vh-80px)] max-w-7xl items-center px-6 py-16">

          <div className="grid w-full items-center gap-16 lg:grid-cols-2">

            {/* Left Content */}
            <div>

              <div className="mb-6 inline-flex rounded-full border border-purple-500/30 bg-purple-500/10 px-4 py-2 text-sm font-medium text-purple-300">
                ✨ AI FILMMAKING STUDIO
              </div>

              <h1 className="max-w-3xl text-5xl font-bold leading-tight md:text-6xl lg:text-7xl">
                Turn your ideas
                <br />
                into{" "}
                <span className="bg-gradient-to-r from-purple-400 to-violet-500 bg-clip-text text-transparent">
                  cinema.
                </span>
              </h1>

              <p className="mt-7 max-w-xl text-lg leading-8 text-gray-400">
                CineForge is an AI-powered filmmaking workspace where you
                can create stories, develop scenes, organize your screenplay
                and bring your cinematic ideas to life.
              </p>

              {/* CTA Buttons */}
              <div className="mt-9 flex flex-wrap gap-4">

                <button
                  onClick={onSignup}
                  className="rounded-xl bg-gradient-to-r from-purple-600 to-violet-600 px-7 py-3.5 font-semibold shadow-lg shadow-purple-900/20 transition hover:scale-[1.02]"
                >
                  Start Creating
                  <span className="ml-2">→</span>
                </button>

                <button
                  onClick={onLogin}
                  className="rounded-xl border border-white/15 px-7 py-3.5 font-semibold text-gray-200 transition hover:border-purple-500 hover:bg-white/5"
                >
                  Sign In
                </button>

              </div>

              {/* Small text */}
              <p className="mt-6 text-sm text-gray-500">
                Create your account and start building your next film.
              </p>

            </div>


            {/* Right Side - Product Preview */}
            <div className="relative">

              {/* Glow */}
              <div className="absolute inset-0 rounded-3xl bg-purple-600/10 blur-3xl" />

              <div className="relative overflow-hidden rounded-2xl border border-white/10 bg-[#101116] shadow-2xl">

                {/* Fake browser header */}
                <div className="flex items-center gap-2 border-b border-white/10 px-5 py-4">
                  <div className="h-3 w-3 rounded-full bg-red-400/70" />
                  <div className="h-3 w-3 rounded-full bg-yellow-400/70" />
                  <div className="h-3 w-3 rounded-full bg-green-400/70" />

                  <div className="ml-4 flex-1 rounded-md bg-white/5 px-4 py-1.5 text-xs text-gray-500">
                    CineForge Studio
                  </div>
                </div>

                {/* Studio preview */}
                <div className="grid min-h-[400px] grid-cols-[150px_1fr_170px]">

                  {/* Sidebar */}
                  <div className="border-r border-white/10 bg-[#0d0e12] p-4">
                    <div className="mb-6 text-xs font-semibold text-gray-500">
                      PROJECT
                    </div>

                    <div className="rounded-lg bg-purple-500/15 px-3 py-2 text-sm text-purple-300">
                      📄 Screenplay
                    </div>

                    <div className="mt-2 rounded-lg px-3 py-2 text-sm text-gray-500">
                      🎬 Characters
                    </div>

                    <div className="mt-2 rounded-lg px-3 py-2 text-sm text-gray-500">
                      📝 Notes
                    </div>

                    <div className="mt-2 rounded-lg px-3 py-2 text-sm text-gray-500">
                      🖼 Storyboard
                    </div>
                  </div>

                  {/* Editor */}
                  <div className="p-6">

                    <div className="mb-6 flex items-center justify-between">
                      <div className="h-3 w-28 rounded bg-white/10" />
                      <div className="h-7 w-20 rounded-md bg-purple-600/30" />
                    </div>

                    <div className="space-y-5">
                      <div className="h-3 w-40 rounded bg-white/10" />

                      <div className="h-2 w-full rounded bg-white/5" />
                      <div className="h-2 w-11/12 rounded bg-white/5" />
                      <div className="h-2 w-9/12 rounded bg-white/5" />

                      <div className="pt-5">
                        <div className="h-3 w-24 rounded bg-purple-400/30" />

                        <div className="mt-5 h-2 w-full rounded bg-white/5" />
                        <div className="mt-3 h-2 w-10/12 rounded bg-white/5" />
                        <div className="mt-3 h-2 w-8/12 rounded bg-white/5" />
                      </div>

                      <div className="pt-5">
                        <div className="h-2 w-full rounded bg-white/5" />
                        <div className="mt-3 h-2 w-9/12 rounded bg-white/5" />
                      </div>
                    </div>

                  </div>

                  {/* Research Panel */}
                  <div className="border-l border-white/10 bg-[#0d0e12] p-4">

                    <div className="mb-5 text-sm font-semibold">
                      Research & Ideas
                    </div>

                    <div className="rounded-xl border border-white/10 bg-white/[0.03] p-4">
                      <div className="h-3 w-28 rounded bg-white/10" />
                      <div className="mt-4 h-2 w-full rounded bg-white/5" />
                      <div className="mt-2 h-2 w-10/12 rounded bg-white/5" />
                    </div>

                    <div className="mt-4 rounded-xl border border-white/10 bg-white/[0.03] p-4">
                      <div className="h-3 w-24 rounded bg-purple-400/20" />
                      <div className="mt-4 h-2 w-full rounded bg-white/5" />
                      <div className="mt-2 h-2 w-8/12 rounded bg-white/5" />
                    </div>

                  </div>

                </div>
              </div>

            </div>

          </div>

        </section>


        {/* Features */}
        <section className="border-t border-white/10 bg-[#0b0c10] px-6 py-20">

          <div className="mx-auto max-w-7xl">

            <div className="text-center">
              <p className="text-sm font-semibold tracking-widest text-purple-400">
                EVERYTHING YOU NEED
              </p>

              <h2 className="mt-3 text-3xl font-bold md:text-4xl">
                Your complete filmmaking workspace
              </h2>

              <p className="mx-auto mt-4 max-w-2xl text-gray-400">
                Create, organize and develop your film from one powerful
                workspace.
              </p>
            </div>


            <div className="mt-12 grid gap-5 md:grid-cols-3">

              <Feature
                icon="✍️"
                title="Write"
                text="Build screenplays and scenes in a focused cinematic editor."
              />

              <Feature
                icon="🔎"
                title="Research"
                text="Collect references, ideas and research while developing your story."
              />

              <Feature
                icon="🎬"
                title="Create"
                text="Turn your ideas into organized scenes and visual storyboards."
              />

            </div>

          </div>

        </section>

      </main>


      {/* Footer */}
      <footer className="border-t border-white/10 px-6 py-8">

        <div className="mx-auto flex max-w-7xl flex-col justify-between gap-4 text-sm text-gray-500 md:flex-row">

          <p>
            © 2026 CineForge. AI Filmmaking Workspace.
          </p>

          <p>
            Create. Imagine. Forge.
          </p>

        </div>

      </footer>

    </div>
  );
}


function Feature({ icon, title, text }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-[#101116] p-6 transition hover:border-purple-500/30">

      <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-xl bg-purple-500/10 text-xl">
        {icon}
      </div>

      <h3 className="text-xl font-semibold">
        {title}
      </h3>

      <p className="mt-3 leading-7 text-gray-400">
        {text}
      </p>

    </div>
  );
}


export default About;