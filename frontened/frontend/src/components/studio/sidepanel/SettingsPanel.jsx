import { Settings, LogOut } from "lucide-react";

function SettingsPanel() {

  const handleLogout = () => {
    // Remove logged-in user
    localStorage.removeItem("user");

    // Go back to the landing/login page
    window.location.href = "/";
  };

  return (
    <div className="h-full w-full bg-[#111316] text-white flex flex-col">

      {/* ================= HEADER ================= */}

      <div className="h-12 shrink-0 flex items-center px-4 border-b border-white/10">

        <div className="flex items-center gap-2">

          <Settings
            size={17}
            className="text-purple-400"
          />

          <h2 className="text-sm font-semibold">
            Settings
          </h2>

        </div>

      </div>


      {/* ================= CONTENT ================= */}

      <div className="flex-1 p-4">

        {/* Account */}
        <div>

          <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">
            Account
          </h3>


          {/* Logout Button */}
          <button
            type="button"
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-3 py-3 rounded-lg border border-white/10 bg-[#191b1f] text-gray-300 hover:bg-red-500/10 hover:border-red-500/20 hover:text-red-400 transition-all duration-200"
          >

            <LogOut size={17} />

            <span className="text-sm font-medium">
              Logout
            </span>

          </button>

        </div>

      </div>

    </div>
  );
}

export default SettingsPanel;