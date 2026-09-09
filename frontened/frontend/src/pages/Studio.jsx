import { useState } from "react";

import Navbar from "../components/studio/Navbar";
import ActivityBar from "../components/studio/ActivityBar";

import FileExplorer from "../components/studio/sidepanel/FileExplorer";
import SearchPanel from "../components/studio/sidepanel/SearchPanel";
import SettingsPanel from "../components/studio/sidepanel/SettingsPanel";
import HelpPanel from "../components/studio/sidepanel/HelpPanel";

import Editor from "../components/studio/Editor";
import ResearchPanel from "../components/studio/ResearchPanel";

import { apiFetch } from "../api";

const projectId = 1;

function Studio() {

  // =========================================================
  // ACTIVE ACTIVITY BAR PANEL
  // =========================================================

  const [activePanel, setActivePanel] = useState("explorer");
  const [sourceIds, setSourceIds] = useState({});


  // =========================================================
  // EDITOR TABS
  // =========================================================

  const [openTabs, setOpenTabs] = useState([
    "scene_07.tnp",
  ]);

  const [activeFile, setActiveFile] = useState(
    "scene_07.tnp"
  );

  const [fileContents, setFileContents] = useState({});


  // =========================================================
  // OPEN FILE
  // =========================================================

  const handleFileOpen = (file) => {
    const fileName =
      typeof file === "string"
        ? file
        : file?.name;

    if (!fileName) return;

    setOpenTabs((previousTabs) =>
      previousTabs.includes(fileName)
        ? previousTabs
        : [...previousTabs, fileName]
    );

    if (typeof file === "object") {

      if (file.content !== undefined) {
        setFileContents((previousContents) => ({
          ...previousContents,
          [fileName]: file.content,
        }));
      }

      if (file.sourceId !== undefined) {
        setSourceIds((previousIds) => ({
          ...previousIds,
          [fileName]: file.sourceId,
        }));
      }
    }

    setActiveFile(fileName);
  };


  // =========================================================
  // SAVE FILE TO CINEFORGE
  // =========================================================

  const handleFileSave = async (fileName, content) => {

    const sourceId = sourceIds[fileName];

    if (!sourceId) {
      alert(
        "This file has not been imported into CineForge yet."
      );
      return;
    }

    try {

      const response = await apiFetch(
        `/projects/${projectId}/sources/${sourceId}/content`,
        {
          method: "PUT",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            content,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to save file."
        );
      }

      setFileContents((previousContents) => ({
        ...previousContents,
        [fileName]: content,
      }));

      alert("Saved to CineForge.");

    } catch (error) {

      console.error("Save failed:", error);

      alert(
        `Unable to save "${fileName}".\n\n${error.message}`
      );
    }
  };


  // =========================================================
  // RENAME FILE / FOLDER
  // =========================================================

  const handleFileRename = (
    oldName,
    newName,
    type
  ) => {

    if (!oldName || !newName) return;

    // Folders do not change the names of the files
    // contained inside them.
    if (type !== "file") return;

    setOpenTabs((previousTabs) =>
      previousTabs.map((tab) =>
        tab === oldName
          ? newName
          : tab
      )
    );

    if (activeFile === oldName) {
      setActiveFile(newName);
    }
  };


  // =========================================================
  // DELETE FILE / FOLDER
  // =========================================================

  const handleFileDelete = (
    deletedFileNames = []
  ) => {

    if (!deletedFileNames.length) return;

    const remainingTabs =
      openTabs.filter(
        (tab) =>
          !deletedFileNames.includes(tab)
      );

    setOpenTabs(remainingTabs);

    if (
      deletedFileNames.includes(
        activeFile
      )
    ) {
      setActiveFile(
        remainingTabs[0] || null
      );
    }
  };


  // =========================================================
  // CLOSE TAB
  // =========================================================

  const handleTabClose = (fileName) => {

    const currentIndex =
      openTabs.indexOf(fileName);

    const remainingTabs =
      openTabs.filter(
        (tab) => tab !== fileName
      );

    setOpenTabs(remainingTabs);

    // If closing the active tab
    if (
      fileName === activeFile &&
      remainingTabs.length > 0
    ) {

      const nextTab =
        remainingTabs[currentIndex] ||
        remainingTabs[currentIndex - 1];

      setActiveFile(nextTab);
    }

    // No tabs remaining
    if (remainingTabs.length === 0) {
      setActiveFile(null);
    }
  };


  // =========================================================
  // RENDER ACTIVE SIDE PANEL
  // =========================================================

  const renderActivePanel = () => {

    switch (activePanel) {

      // -----------------------------------------------
      // FILE EXPLORER
      // -----------------------------------------------

      case "explorer":
        return (
          <FileExplorer
            projectId={projectId}
            activeFile={activeFile}
            onFileOpen={handleFileOpen}
            onFileRename={handleFileRename}
            onFileDelete={handleFileDelete}
          />
        );


      // -----------------------------------------------
      // SEARCH
      // -----------------------------------------------

      case "search":
        return <SearchPanel />;


      // -----------------------------------------------
      // SETTINGS
      // -----------------------------------------------

      case "settings":
        return <SettingsPanel />;


      // -----------------------------------------------
      // HELP
      // -----------------------------------------------

      case "help":
        return <HelpPanel />;


      // -----------------------------------------------
      // DEFAULT
      // -----------------------------------------------

      default:
        return (
          <FileExplorer
            projectId={projectId}
            activeFile={activeFile}
            onFileOpen={handleFileOpen}
            onFileRename={handleFileRename}
            onFileDelete={handleFileDelete}
          />
        );
    }
  };


  // =========================================================
  // PAGE
  // =========================================================

  return (
    <div className="h-screen bg-[#0d0f12] text-white overflow-hidden flex flex-col">

      {/* ===================================================
          NAVBAR
      ==================================================== */}

      <Navbar />


      {/* ===================================================
          MAIN STUDIO AREA
      ==================================================== */}

      <div className="flex flex-1 min-h-0">

        {/* =================================================
            ACTIVITY BAR
        ================================================== */}

        <ActivityBar
          activePanel={activePanel}
          onPanelChange={setActivePanel}
        />


        {/* =================================================
            SIDE PANEL
        ================================================== */}

        <div className="w-71.25 min-w-71.25 max-w-71.25 shrink-0 min-h-0 overflow-hidden border-r border-white/10">

          {renderActivePanel()}

        </div>


        {/* =================================================
            EDITOR
        ================================================== */}

        <Editor
          openTabs={openTabs}
          activeFile={activeFile}
          onTabSelect={setActiveFile}
          onTabClose={handleTabClose}
          fileContents={fileContents}
          onSave={handleFileSave}
        />


        {/* =================================================
            RESEARCH PANEL
        ================================================== */}

        <ResearchPanel />

      </div>

    </div>
  );
}

export default Studio;