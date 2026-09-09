import {
  Files,
  Search,
  Settings,
  HelpCircle,
} from "lucide-react";

function ActivityBar({ activePanel, onPanelChange }) {
  const tools = [
    {
      id: "explorer",
      icon: Files,
      label: "File Explorer",
    },
    {
      id: "search",
      icon: Search,
      label: "Search",
    },
    {
      id: "settings",
      icon: Settings,
      label: "Settings",
    },
    {
      id: "help",
      icon: HelpCircle,
      label: "Help",
    },
  ];

  return (
    <aside className="w-13 shrink-0 bg-[#111316] border-r border-white/10 flex flex-col">

      {/* ================= TOP TOOLS ================= */}
      <div className="flex flex-col">

        {tools.map((tool) => {
          const Icon = tool.icon;
          const isActive = activePanel === tool.id;

          return (
            <button
              key={tool.id}
              type="button"
              onClick={() => onPanelChange(tool.id)}
              title={tool.label}
              aria-label={tool.label}
              className={`
                relative
                w-full
                h-12
                flex
                items-center
                justify-center
                transition-all
                duration-200
                ${
                  isActive
                    ? "text-white bg-purple-500/10"
                    : "text-gray-500 hover:text-gray-200 hover:bg-white/5"
                }
              `}
            >

              {/* Active Indicator */}
              {isActive && (
                <span className="absolute left-0 top-0 bottom-0 w-0.5 bg-purple-500" />
              )}

              {/* Icon */}
              <Icon
                size={21}
                strokeWidth={1.8}
              />

            </button>
          );
        })}

      </div>

    </aside>
  );
}

export default ActivityBar;