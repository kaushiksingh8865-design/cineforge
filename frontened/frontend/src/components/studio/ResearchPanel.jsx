import { useState } from "react";
import { apiFetch } from "../../api";

const projectId = 1;

function ResearchPanel() {
  const [question, setQuestion] = useState("");
  const [research, setResearch] = useState(null);
  const [loading, setLoading] = useState(false);

  const [ideas, setIdeas] = useState([]);
  const [ideasLoading, setIdeasLoading] = useState(false);

  const handleResearch = async () => {
    if (!question.trim()) return;

    try {
      setLoading(true);

      const response = await apiFetch(
        `/projects/${projectId}/research?question=${encodeURIComponent(
          question
        )}`,
        {
          method: "POST",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Research failed."
        );
      }

      setResearch(data);
    } catch (error) {
      console.error("Research failed:", error);
      alert(error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateIdeas = async () => {
    try {
      setIdeasLoading(true);

      const response = await apiFetch(
        `/projects/${projectId}/ideas?request=${encodeURIComponent(
          "Generate creative ideas for Scene 07 in the laboratory. Focus on atmosphere, tension, character actions, and interesting story developments."
        )}`,
        {
          method: "POST",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Idea generation failed."
        );
      }

      setIdeas(data.beats || []);
    } catch (error) {
      console.error(
        "Idea generation failed:",
        error
      );
      alert(error.message);
    } finally {
      setIdeasLoading(false);
    }
  };

  return (
    <aside className="w-82.5 h-full bg-[#111316] border-l border-[#292c32] flex flex-col text-gray-200">
      {/* Header */}
      <div className="h-13 px-4 flex items-center justify-between border-b border-[#292c32]">
        <div>
          <h2 className="text-sm font-semibold text-gray-100">
            Research & Ideas
          </h2>

          <p className="text-[11px] text-gray-500 mt-0.5">
            Scene 07 · Laboratory
          </p>
        </div>

        <button
          type="button"
          className="w-7 h-7 rounded-md flex items-center justify-center text-gray-400 hover:text-white hover:bg-[#1d2025] transition"
          title="More"
        >
          ⋯
        </button>
      </div>

      {/* Scrollable Content */}
      <div className="flex-1 overflow-y-auto">
        {/* Research Section */}
        <section className="p-4 border-b border-[#292c32]">
          <h3 className="text-xs font-semibold uppercase tracking-wide text-gray-400 mb-3">
            Research
          </h3>

          <div className="space-y-3">
            {/* Research Input */}
            <div className="flex gap-2">
              <input
                type="text"
                value={question}
                onChange={(event) =>
                  setQuestion(event.target.value)
                }
                onKeyDown={(event) => {
                  if (event.key === "Enter") {
                    handleResearch();
                  }
                }}
                placeholder="Ask a research question..."
                className="flex-1 min-w-0 h-9 px-3 rounded-md bg-[#181a1e] border border-[#292c32] text-xs text-gray-200 placeholder:text-gray-600 outline-none focus:border-purple-500"
              />

              <button
                type="button"
                onClick={handleResearch}
                disabled={loading}
                className="px-3 h-9 rounded-md bg-purple-600 text-xs text-white hover:bg-purple-500 disabled:opacity-50 transition"
              >
                {loading ? "..." : "Search"}
              </button>
            </div>

            {/* Research Results */}
            {research && (
              <div className="space-y-3">
                {/* Summary */}
                <div className="p-3 rounded-lg bg-[#181a1e] border border-[#292c32]">
                  <p className="text-[10px] uppercase tracking-wide text-gray-500 mb-1">
                    Summary
                  </p>

                  <p className="text-sm leading-relaxed text-gray-200">
                    {research.summary}
                  </p>
                </div>

                {/* Findings */}
                {research.findings.map(
                  (finding, index) => (
                    <div
                      key={index}
                      className="p-3 rounded-lg bg-[#181a1e] border border-[#292c32] hover:border-[#3b3f48] transition"
                    >
                      {/* Claim */}
                      <p className="text-sm leading-relaxed text-gray-200">
                        {finding.claim}
                      </p>

                      {/* Evidence */}
                      <p className="text-[11px] leading-relaxed text-gray-400 mt-2">
                        {finding.evidence}
                      </p>

                      {/* Source + Confidence */}
                      <div className="flex items-start justify-between gap-3 mt-3">
                        <p className="text-[10px] leading-relaxed text-gray-500 break-all">
                          {finding.source}
                        </p>

                        <span className="shrink-0 text-[10px] text-purple-400 uppercase">
                          {finding.confidence}
                        </span>
                      </div>
                    </div>
                  )
                )}
              </div>
            )}
          </div>
        </section>

        {/* Ideas Section */}
        <section className="p-4 border-b border-[#292c32]">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-xs font-semibold uppercase tracking-wide text-gray-400">
              Ideas
            </h3>

            <button
              type="button"
              onClick={handleGenerateIdeas}
              disabled={ideasLoading}
              className="text-purple-400 text-xs hover:text-purple-300 disabled:opacity-50 transition"
            >
              {ideasLoading
                ? "Generating..."
                : "+ Add"}
            </button>
          </div>

          {/* Generated Ideas */}
          {ideas.length > 0 ? (
            ideas.map((idea, index) => (
              <div
                key={index}
                className="p-3 mt-2 rounded-lg bg-[#181a1e] border border-[#292c32]"
              >
                <p className="text-sm leading-relaxed text-gray-300">
                  {idea.description}
                </p>

                <p className="text-[10px] text-gray-500 mt-2">
                  Purpose: {idea.purpose}
                </p>
              </div>
            ))
          ) : (
            <p className="text-[11px] text-gray-500">
              Generate ideas for this scene.
            </p>
          )}
        </section>

        {/* Scene Visual Section */}
        <section className="p-4">
          <div className="mb-3">
            <h3 className="text-xs font-semibold uppercase tracking-wide text-gray-400">
              Scene Visual
            </h3>
          </div>

          <div className="p-3 rounded-lg bg-[#181a1e] border border-[#292c32]">
            <p className="text-sm text-gray-300 mb-3">
              Scene 07 - Laboratory
            </p>

            {/* Visual Placeholder */}
            <div className="h-45 rounded-xl border border-[#292c32] bg-[#202329] flex flex-col items-center justify-center text-center">
              <div className="w-12 h-12 rounded-xl bg-[#292d34] flex items-center justify-center text-2xl mb-3">
                🎬
              </div>

              <p className="text-sm text-gray-300">
                Scene visual
              </p>

              <p className="text-[11px] text-gray-500 mt-1 px-8">
                Generate a visual reference for this
                scene
              </p>
            </div>

            {/* Scene Visual Actions */}
            <div className="flex gap-2 mt-3">
              <button
                type="button"
                className="flex-1 h-9 rounded-md bg-[#202329] border border-[#353941] text-xs text-gray-300 hover:bg-[#292d34] hover:text-white transition flex items-center justify-center gap-2"
              >
                ↻
                Regenerate
              </button>

              <button
                type="button"
                className="flex-1 h-9 rounded-md bg-purple-600 text-xs text-white hover:bg-purple-500 transition flex items-center justify-center gap-2"
              >
                ☆
                Save to Storyboard
              </button>
            </div>
          </div>
        </section>
      </div>
    </aside>
  );
}

export default ResearchPanel;