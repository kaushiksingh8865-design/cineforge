import { useState } from "react";
import {
  HelpCircle,
  BookOpen,
  Mail,
  ArrowLeft,
} from "lucide-react";

function HelpPanel() {
  const [activeSection, setActiveSection] = useState(null);

  // Go back to Help main menu
  const handleBack = () => {
    setActiveSection(null);
  };

  return (
    <div className="h-full w-full bg-[#111316] text-white flex flex-col ">

      {/* ================= HEADER ================= */}

      <div className="h-12 shrink-0 flex items-center px-4 border-b border-white/10">

        <div className="flex items-center gap-2">

          <HelpCircle
            size={17}
            className="text-purple-400"
          />

          <h2 className="text-sm font-semibold">
            Help
          </h2>

        </div>

      </div>


      {/* =================================================
          MAIN HELP MENU
      ================================================== */}

      {activeSection === null && (

        <div className="flex-1 p-4">

          <p className="text-sm text-gray-400 mb-5">
            How can we help you?
          </p>


          {/* ================= DOCUMENTATION ================= */}

          <button
            type="button"
            onClick={() => setActiveSection("documentation")}
            className="w-full flex items-center gap-3 p-3 mb-2 rounded-lg border border-white/10 bg-[#191b1f] hover:bg-white/5 transition text-left"
          >

            <div className="w-9 h-9 rounded-md bg-purple-500/10 flex items-center justify-center shrink-0">

              <BookOpen
                size={17}
                className="text-purple-400"
              />

            </div>

            <div>

              <p className="text-sm text-gray-300">
                Documentation
              </p>

              <p className="text-xs text-gray-600 mt-1">
                Learn how to use CineForge
              </p>

            </div>

          </button>


          {/* ================= CONTACT INFORMATION ================= */}

          <button
            type="button"
            onClick={() => setActiveSection("contact")}
            className="w-full flex items-center gap-3 p-3 rounded-lg border border-white/10 bg-[#191b1f] hover:bg-white/5 transition text-left"
          >

            <div className="w-9 h-9 rounded-md bg-purple-500/10 flex items-center justify-center shrink-0">

              <Mail
                size={17}
                className="text-purple-400"
              />

            </div>

            <div>

              <p className="text-sm text-gray-300">
                Contact Information
              </p>

              <p className="text-xs text-gray-600 mt-1">
                Get in touch with the CineForge team
              </p>

            </div>

          </button>

        </div>

      )}


      {/* =================================================
          DOCUMENTATION
      ================================================== */}

      {activeSection === "documentation" && (

        <div className="flex-1 overflow-y-auto">

          {/* Back */}
          <div className="p-3 border-b border-white/10">

            <button
              type="button"
              onClick={handleBack}
              className="flex items-center gap-2 text-xs text-gray-400 hover:text-white transition"
            >

              <ArrowLeft size={15} />

              Back

            </button>

          </div>


          <div className="p-4">

            <div className="flex items-center gap-3 mb-5">

              <div className="w-10 h-10 rounded-lg bg-purple-500/10 flex items-center justify-center">

                <BookOpen
                  size={19}
                  className="text-purple-400"
                />

              </div>

              <div>

                <h2 className="text-sm font-semibold text-white">
                  CineForge Documentation
                </h2>

                <p className="text-xs text-gray-500 mt-1">
                  Getting started with CineForge
                </p>

              </div>

            </div>


            {/* Getting Started */}
            <div className="mb-5">

              <h3 className="text-xs font-semibold text-gray-300 uppercase tracking-wider mb-2">
                Getting Started
              </h3>

              <p className="text-xs leading-5 text-gray-500">
                CineForge is a creative filmmaking workspace designed
                to help you organize your film project, write scenes,
                research ideas and work with your screenplay.
              </p>

            </div>


            {/* File Explorer */}
            <div className="mb-5">

              <h3 className="text-xs font-semibold text-gray-300 uppercase tracking-wider mb-2">
                File Explorer
              </h3>

              <p className="text-xs leading-5 text-gray-500">
                Use the File Explorer to browse and organize your
                project files. Select a file to open it in the editor.
              </p>

            </div>


            {/* Editor */}
            <div className="mb-5">

              <h3 className="text-xs font-semibold text-gray-300 uppercase tracking-wider mb-2">
                Editor
              </h3>

              <p className="text-xs leading-5 text-gray-500">
                Open your screenplay or project files in the editor.
                Multiple files can be opened using tabs.
              </p>

            </div>


            {/* AI Assistant */}
            <div>

              <h3 className="text-xs font-semibold text-gray-300 uppercase tracking-wider mb-2">
                AI Assistant
              </h3>

              <p className="text-xs leading-5 text-gray-500">
                Use the AI Assistant from the top navigation bar to
                get creative help with scenes, dialogue and filmmaking
                ideas.
              </p>

            </div>

          </div>

        </div>

      )}


      {/* =================================================
          CONTACT INFORMATION
      ================================================== */}

      {activeSection === "contact" && (

        <div className="flex-1 overflow-y-auto">

          {/* Back */}
          <div className="p-3 border-b border-white/10">

            <button
              type="button"
              onClick={handleBack}
              className="flex items-center gap-2 text-xs text-gray-400 hover:text-white transition"
            >

              <ArrowLeft size={15} />

              Back

            </button>

          </div>


          <div className="p-4">

            {/* Header */}
            <div className="flex items-center gap-3 mb-6">

              <div className="w-10 h-10 rounded-lg bg-purple-500/10 flex items-center justify-center">

                <Mail
                  size={19}
                  className="text-purple-400"
                />

              </div>

              <div>

                <h2 className="text-sm font-semibold text-white">
                  Contact Information
                </h2>

                <p className="text-xs text-gray-500 mt-1">
                  We're here to help
                </p>

              </div>

            </div>


            {/* Email */}
            <div className="mb-4 p-3 rounded-lg border border-white/10 bg-[#191b1f]">

              <p className="text-xs text-gray-500 mb-1">
                Support Email
              </p>

              <p className="text-sm text-gray-300">
                support.cineforge@gmail.com
              </p>

            </div>


            {/* General Email */}
            <div className="mb-4 p-3 rounded-lg border border-white/10 bg-[#191b1f]">

              <p className="text-xs text-gray-500 mb-1">
                General Enquiries
              </p>

              <p className="text-sm text-gray-300">
                ankitgangwar0012@gmail.com
              </p>

            </div>


            {/* Support */}
            <div className="p-3 rounded-lg border border-white/10 bg-[#191b1f]">

              <p className="text-xs text-gray-500 mb-1">
                Support Hours
              </p>

              <p className="text-sm text-gray-300">
                Monday – Friday
              </p>

              <p className="text-xs text-gray-500 mt-1">
                9:00 AM – 6:00 PM
              </p>

            </div>


            {/* Footer Message */}
            <p className="text-xs leading-5 text-gray-600 mt-6 text-center">
              Have a question or found an issue?
              Contact our team and we'll be happy to help.
            </p>

          </div>

        </div>

      )}

    </div>
  );
}

export default HelpPanel;