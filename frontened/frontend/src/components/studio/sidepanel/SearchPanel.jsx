import { Search, FileText } from "lucide-react";

function SearchPanel() {
  return (
    <div className="h-full w-full bg-[#111316] text-white flex flex-col">

      {/* Header */}
      <div className="h-12 shrink-0 flex items-center px-4 border-b border-white/10">
        <h2 className="text-sm font-semibold">
          Search
        </h2>
      </div>

      {/* Search Input */}
      <div className="p-3">
        <div className="flex items-center gap-2 h-9 px-3 rounded-md bg-[#191b1f] border border-white/10 focus-within:border-purple-500/50">

          <Search
            size={16}
            className="text-gray-500 shrink-0"
          />

          <input
            type="text"
            placeholder="Search files..."
            className="w-full bg-transparent outline-none text-sm text-gray-200 placeholder:text-gray-600"
          />

        </div>
      </div>

      {/* Search Results */}
      <div className="flex-1 px-4">

        <div className="flex flex-col items-center justify-center h-full text-center">

          <FileText
            size={32}
            className="text-gray-700 mb-3"
          />

          <p className="text-sm text-gray-500">
            Search your project
          </p>

          <p className="text-xs text-gray-600 mt-1">
            Find scenes, scripts and project files
          </p>

        </div>

      </div>

    </div>
  );
}

export default SearchPanel;