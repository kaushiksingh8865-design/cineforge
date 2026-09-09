import { useEffect, useState } from "react";
import {
  FolderOpen,
  Folder,
  File,
  ChevronRight,
  ChevronDown,
  FilePlus,
  FolderPlus,
  RefreshCw,
  Pencil,
  Trash2,
} from "lucide-react";

import { apiFetch } from "../../api";

function FileExplorer({
  projectId,
  activeFile,
  onFileOpen,
  onFileRename,
  onFileDelete,
}) {
  const [rootHandle, setRootHandle] = useState(null);
  const [fileTree, setFileTree] = useState([]);
  const [loading, setLoading] = useState(false);
  const [importingFile, setImportingFile] = useState(null);

  // Currently selected folder.
  // New File/New Folder will be created inside this folder.
  const [selectedFolder, setSelectedFolder] = useState(null);

  // Right-click context menu
  const [contextMenu, setContextMenu] = useState(null);

  useEffect(() => {
    const closeMenu = () => setContextMenu(null);

    window.addEventListener("click", closeMenu);
    window.addEventListener("scroll", closeMenu);
    window.addEventListener("resize", closeMenu);

    return () => {
      window.removeEventListener("click", closeMenu);
      window.removeEventListener("scroll", closeMenu);
      window.removeEventListener("resize", closeMenu);
    };
  }, []);

  // =========================================================
  // OPEN FOLDER
  // =========================================================

  const handleOpenFolder = async () => {
    try {
      if (!window.showDirectoryPicker) {
        alert(
          "Folder access is not supported in this browser. Please use Chrome or Edge."
        );
        return;
      }

      const directoryHandle = await window.showDirectoryPicker({
        mode: "readwrite",
      });

      setLoading(true);

      const tree = await readDirectory(directoryHandle);

      setRootHandle(directoryHandle);
      setSelectedFolder(directoryHandle);
      setFileTree(tree);
    } catch (error) {
      if (error.name !== "AbortError") {
        console.error("Error opening folder:", error);
        alert("Unable to open the selected folder.");
      }
    } finally {
      setLoading(false);
    }
  };

  // =========================================================
  // READ DIRECTORY RECURSIVELY
  // =========================================================

  const readDirectory = async (directoryHandle) => {
    const items = [];

    for await (const [name, handle] of directoryHandle.entries()) {
      if (handle.kind === "directory") {
        const children = await readDirectory(handle);

        items.push({
          name,
          type: "folder",
          handle,
          parentHandle: directoryHandle,
          children,
          isOpen: true,
        });
      } else {
        items.push({
          name,
          type: "file",
          handle,
          parentHandle: directoryHandle,
        });
      }
    }

    // Folders first, then files
    items.sort((a, b) => {
      if (a.type === "folder" && b.type === "file") {
        return -1;
      }

      if (a.type === "file" && b.type === "folder") {
        return 1;
      }

      return a.name.localeCompare(b.name);
    });

    return items;
  };

  // =========================================================
  // REFRESH
  // =========================================================

  const handleRefresh = async () => {
    if (!rootHandle) return;

    try {
      setLoading(true);

      const tree = await readDirectory(rootHandle);

      setFileTree(tree);
    } catch (error) {
      console.error("Error refreshing explorer:", error);

      alert("Unable to refresh the project explorer.");
    } finally {
      setLoading(false);
    }
  };

  // =========================================================
  // CREATE NEW FILE
  // =========================================================

  const handleNewFile = async () => {
    if (!rootHandle) {
      alert("Please open a folder first.");
      return;
    }

    const fileName = window.prompt("Enter file name:");

    if (!fileName || !fileName.trim()) {
      return;
    }

    try {
      const targetFolder = selectedFolder || rootHandle;

      await targetFolder.getFileHandle(fileName.trim(), {
        create: true,
      });

      await handleRefresh();
    } catch (error) {
      console.error("Error creating file:", error);

      alert(
        "Unable to create the file. A file with this name may already exist."
      );
    }
  };

  // =========================================================
  // CREATE NEW FOLDER
  // =========================================================

  const handleNewFolder = async () => {
    if (!rootHandle) {
      alert("Please open a folder first.");
      return;
    }

    const folderName = window.prompt("Enter folder name:");

    if (!folderName || !folderName.trim()) {
      return;
    }

    try {
      const targetFolder = selectedFolder || rootHandle;

      await targetFolder.getDirectoryHandle(folderName.trim(), {
        create: true,
      });

      await handleRefresh();
    } catch (error) {
      console.error("Error creating folder:", error);

      alert(
        "Unable to create the folder. A folder with this name may already exist."
      );
    }
  };

  // =========================================================
  // TOGGLE FOLDER
  // =========================================================

  const toggleFolder = (folderHandle) => {
    const updateTree = (items) => {
      return items.map((item) => {
        if (item.type !== "folder") {
          return item;
        }

        if (item.handle === folderHandle) {
          return {
            ...item,
            isOpen: !item.isOpen,
          };
        }

        return {
          ...item,
          children: updateTree(item.children),
        };
      });
    };

    setFileTree((previousTree) => updateTree(previousTree));
  };

  // =========================================================
  // SELECT FOLDER
  // =========================================================

  const handleFolderSelect = (folderHandle) => {
    setSelectedFolder(folderHandle);
  };

  // =========================================================
  // OPEN FILE
  // =========================================================

  const handleFileClick = async (file) => {
    if (!file || file.type !== "file") return;

    try {
      const fileObject = await file.handle.getFile();
      const content = await fileObject.text();

      if (onFileOpen) {
        onFileOpen({
          name: file.name,
          content,
        });
      }
    } catch (error) {
      console.error("Failed to read file:", error);

      alert(`Unable to open "${file.name}".`);
    }
  };

  // =========================================================
  // IMPORT FILE TO CINEFORGE
  // =========================================================

  const handleImportToCineForge = async (item) => {
    setContextMenu(null);

    if (item.type !== "file") {
      alert("Only files can be imported.");
      return;
    }

    if (!projectId) {
      alert("No CineForge project is selected.");
      return;
    }

    if (!item.name.toLowerCase().endsWith(".txt")) {
      alert(
        "This source importer currently supports .txt files only."
      );
      return;
    }

    try {
      setImportingFile(item.name);

      // Read the actual local file.
      const file = await item.handle.getFile();

      // Prepare multipart upload.
      const formData = new FormData();
      formData.append("file", file, item.name);

      // 1. Upload source to CineForge.
      // apiFetch automatically adds the JWT.
      const uploadResponse = await apiFetch(
        `/projects/${projectId}/sources/upload`,
        {
          method: "POST",
          body: formData,
        }
      );

      const uploadData = await uploadResponse.json();

      if (!uploadResponse.ok) {
        throw new Error(
          uploadData.detail || "Failed to upload source."
        );
      }

      // 2. Ingest source through ETL + AI.
      // apiFetch automatically adds the JWT.
      const ingestResponse = await apiFetch(
        `/projects/${projectId}/sources/${uploadData.id}/ingest`,
        {
          method: "POST",
        }
      );

      const ingestData = await ingestResponse.json();

      if (!ingestResponse.ok) {
        throw new Error(
          ingestData.detail || "Failed to ingest source."
        );
      }

      if (onFileOpen) {
        const fileObject = await item.handle.getFile();
        const content = await fileObject.text();

        onFileOpen({
          name: item.name,
          content,
          sourceId: uploadData.id,
        });
      }

      alert(
        `Imported successfully.\nScene ${ingestData.scene.scene_number} was created.`
      );
    } catch (error) {
      console.error(
        "Error importing source:",
        error
      );

      alert(
        `Unable to import "${item.name}".\n\n${error.message}`
      );
    } finally {
      setImportingFile(null);
    }
  };

  // =========================================================
  // RIGHT-CLICK MENU
  // =========================================================

  const handleContextMenu = (event, item) => {
    event.preventDefault();
    event.stopPropagation();

    setContextMenu({
      x: event.clientX,
      y: event.clientY,
      item,
    });
  };

  // =========================================================
  // RENAME
  // =========================================================

  const handleRename = async (item) => {
    setContextMenu(null);

    if (!item.parentHandle) {
      alert("This item cannot be renamed.");
      return;
    }

    const newName = window.prompt(
      "Enter new name:",
      item.name
    );

    if (
      !newName ||
      !newName.trim() ||
      newName.trim() === item.name
    ) {
      return;
    }

    const trimmedName = newName.trim();

    try {
      // FileSystemHandle.move() is supported in some Chromium versions.
      if (typeof item.handle.move === "function") {
        await item.handle.move(trimmedName);
      } else if (item.type === "file") {
        // Fallback: create the renamed file,
        // copy its bytes, then delete old file.
        const sourceFile = await item.handle.getFile();

        const newFile =
          await item.parentHandle.getFileHandle(
            trimmedName,
            {
              create: true,
            }
          );

        const writable =
          await newFile.createWritable();

        await writable.write(
          await sourceFile.arrayBuffer()
        );

        await writable.close();

        await item.parentHandle.removeEntry(
          item.name
        );
      } else {
        // Fallback for folders:
        // recursively copy the folder, then remove old folder.
        const copyDirectory = async (
          source,
          target
        ) => {
          for await (const [
            name,
            child,
          ] of source.entries()) {
            if (child.kind === "file") {
              const file = await child.getFile();

              const newFile =
                await target.getFileHandle(name, {
                  create: true,
                });

              const writable =
                await newFile.createWritable();

              await writable.write(
                await file.arrayBuffer()
              );

              await writable.close();
            } else if (
              child.kind === "directory"
            ) {
              const newDirectory =
                await target.getDirectoryHandle(
                  name,
                  {
                    create: true,
                  }
                );

              await copyDirectory(
                child,
                newDirectory
              );
            }
          }
        };

        const newFolder =
          await item.parentHandle.getDirectoryHandle(
            trimmedName,
            {
              create: true,
            }
          );

        await copyDirectory(
          item.handle,
          newFolder
        );

        await item.parentHandle.removeEntry(
          item.name,
          {
            recursive: true,
          }
        );
      }

      await handleRefresh();

      // Tell Studio that the item was renamed.
      if (onFileRename) {
        onFileRename(
          item.name,
          trimmedName,
          item.type
        );
      }

      // Keep the renamed file open if it was the active file.
      if (
        item.type === "file" &&
        activeFile === item.name &&
        onFileOpen
      ) {
        onFileOpen(trimmedName);
      }
    } catch (error) {
      console.error("Error renaming item:", error);

      alert(
        `Unable to rename ${
          item.type === "folder"
            ? "folder"
            : "file"
        }. The new name may already exist.`
      );
    }
  };

  // =========================================================
  // DELETE
  // =========================================================

  const handleDelete = async (item) => {
    setContextMenu(null);

    if (!item.parentHandle) {
      alert("This item cannot be deleted.");
      return;
    }

    const message =
      item.type === "folder"
        ? `Delete folder "${item.name}" and everything inside it?`
        : `Delete file "${item.name}"?`;

    if (!window.confirm(message)) {
      return;
    }

    try {
      await item.parentHandle.removeEntry(
        item.name,
        {
          recursive: item.type === "folder",
        }
      );

      await handleRefresh();

      // Tell Studio which file/folder was deleted.
      if (onFileDelete) {
        onFileDelete([item.name]);
      }
    } catch (error) {
      console.error("Error deleting item:", error);

      alert(
        `Unable to delete ${
          item.type === "folder"
            ? "folder"
            : "file"
        } "${item.name}".`
      );
    }
  };

  // =========================================================
  // RENDER TREE
  // =========================================================

  const renderTree = (items, level = 0) => {
    return items.map((item) => {
      // =====================================================
      // FOLDER
      // =====================================================

      if (item.type === "folder") {
        const isSelected =
          selectedFolder === item.handle;

        return (
          <div key={item.name + level}>
            <button
              type="button"
              onClick={() => {
                handleFolderSelect(item.handle);
                toggleFolder(item.handle);
              }}
              onContextMenu={(event) =>
                handleContextMenu(event, item)
              }
              className={`
                w-full
                flex
                items-center
                gap-1
                py-1.5
                rounded-md
                text-left
                text-[13px]
                transition
                ${
                  isSelected
                    ? "bg-purple-500/10 text-white"
                    : "text-gray-300 hover:bg-white/5 hover:text-white"
                }
              `}
              style={{
                paddingLeft: `${8 + level * 16}px`,
              }}
              title="Select folder"
            >
              <span className="w-4 shrink-0 text-gray-500">
                {item.isOpen ? (
                  <ChevronDown size={14} />
                ) : (
                  <ChevronRight size={14} />
                )}
              </span>

              {item.isOpen ? (
                <FolderOpen
                  size={16}
                  className="shrink-0 text-purple-400"
                />
              ) : (
                <Folder
                  size={16}
                  className="shrink-0 text-purple-400"
                />
              )}

              <span className="truncate">
                {item.name}
              </span>
            </button>

            {item.isOpen &&
              item.children.length > 0 && (
                <div>
                  {renderTree(
                    item.children,
                    level + 1
                  )}
                </div>
              )}
          </div>
        );
      }

      // =====================================================
      // FILE
      // =====================================================

      return (
        <button
          key={item.name + level}
          type="button"
          onClick={() =>
            handleFileClick(item)
          }
          onContextMenu={(event) =>
            handleContextMenu(event, item)
          }
          className={`
            w-full
            flex
            items-center
            gap-2
            py-1.5
            rounded-md
            text-left
            text-[13px]
            transition
            ${
              activeFile === item.name
                ? "bg-purple-500/10 text-purple-300"
                : "text-gray-400 hover:bg-white/5 hover:text-gray-200"
            }
          `}
          style={{
            paddingLeft: `${28 + level * 16}px`,
          }}
        >
          <File
            size={15}
            className="shrink-0 text-gray-500"
          />

          <span className="truncate">
            {item.name}
          </span>
        </button>
      );
    });
  };

  // =========================================================
  // UI
  // =========================================================

  return (
    <aside className="w-71.25 shrink-0 h-full bg-[#111316] border-r border-white/10 flex flex-col">

      {/* =====================================================
          HEADER
      ===================================================== */}

      <div className="h-12 shrink-0 px-3 flex items-center justify-between border-b border-white/10">
        <span className="text-[11px] font-semibold tracking-[0.08em] text-gray-300">
          PROJECT EXPLORER
        </span>

        <div className="flex items-center gap-0.5">

          {/* Open Folder */}
          <button
            type="button"
            onClick={handleOpenFolder}
            title="Open Folder"
            className="w-7 h-7 flex items-center justify-center rounded-md text-gray-500 hover:text-white hover:bg-white/5 transition"
          >
            <FolderOpen size={16} />
          </button>

          {/* New File */}
          <button
            type="button"
            onClick={handleNewFile}
            disabled={!rootHandle}
            title="New File"
            className={`
              w-7 h-7
              flex
              items-center
              justify-center
              rounded-md
              transition
              ${
                rootHandle
                  ? "text-gray-500 hover:text-white hover:bg-white/5"
                  : "text-gray-700 cursor-not-allowed"
              }
            `}
          >
            <FilePlus size={16} />
          </button>

          {/* New Folder */}
          <button
            type="button"
            onClick={handleNewFolder}
            disabled={!rootHandle}
            title="New Folder"
            className={`
              w-7 h-7
              flex
              items-center
              justify-center
              rounded-md
              transition
              ${
                rootHandle
                  ? "text-gray-500 hover:text-white hover:bg-white/5"
                  : "text-gray-700 cursor-not-allowed"
              }
            `}
          >
            <FolderPlus size={16} />
          </button>

          {/* Refresh */}
          <button
            type="button"
            onClick={handleRefresh}
            disabled={!rootHandle || loading}
            title="Refresh"
            className={`
              w-7 h-7
              flex
              items-center
              justify-center
              rounded-md
              transition
              ${
                rootHandle
                  ? "text-gray-500 hover:text-white hover:bg-white/5"
                  : "text-gray-700 cursor-not-allowed"
              }
            `}
          >
            <RefreshCw
              size={15}
              className={
                loading
                  ? "animate-spin"
                  : ""
              }
            />
          </button>

        </div>
      </div>

      {/* =====================================================
          CONTENT
      ===================================================== */}

      <div className="flex-1 min-h-0 overflow-y-auto py-3 px-2">

        {/* NO FOLDER */}

        {!rootHandle && !loading && (
          <div className="h-full flex flex-col items-center justify-center px-5 text-center">

            <div className="w-12 h-12 rounded-xl bg-purple-500/10 flex items-center justify-center mb-4">
              <FolderOpen
                size={24}
                className="text-purple-400"
              />
            </div>

            <p className="text-sm text-gray-300">
              No folder opened
            </p>

            <p className="text-xs text-gray-600 mt-2 leading-5">
              Open a project folder to view its
              files and folders.
            </p>

            <button
              type="button"
              onClick={handleOpenFolder}
              className="mt-4 px-4 py-2 rounded-md bg-purple-600 hover:bg-purple-500 text-xs font-medium text-white transition"
            >
              Open Folder
            </button>

          </div>
        )}

        {/* LOADING */}

        {loading && (
          <div className="h-full flex items-center justify-center">
            <p className="text-xs text-gray-500">
              Reading project files...
            </p>
          </div>
        )}

        {/* OPENED PROJECT */}

        {rootHandle && !loading && (
          <>
            {/* Root Folder */}

            <button
              type="button"
              onClick={() =>
                setSelectedFolder(rootHandle)
              }
              className={`
                w-full
                flex
                items-center
                gap-2
                px-2
                py-2
                mb-1
                rounded-md
                text-left
                transition
                ${
                  selectedFolder === rootHandle
                    ? "bg-purple-500/10"
                    : "hover:bg-white/5"
                }
              `}
              title="Select project root"
            >
              <FolderOpen
                size={17}
                className="text-purple-400"
              />

              <span className="text-sm font-medium text-gray-200 truncate">
                {rootHandle.name}
              </span>
            </button>

            {/* Complete Tree */}

            <div>
              {fileTree.length > 0 ? (
                renderTree(fileTree)
              ) : (
                <div className="px-8 py-6 text-center">
                  <p className="text-xs text-gray-600">
                    This folder is empty
                  </p>
                </div>
              )}
            </div>
          </>
        )}

        {/* RIGHT-CLICK CONTEXT MENU */}

        {contextMenu && (
          <div
            className="fixed z-9999 min-w-40 rounded-lg border border-white/10 bg-[#1b1d21] py-1 shadow-2xl"
            style={{
              left: `${Math.min(
                contextMenu.x,
                window.innerWidth - 180
              )}px`,
              top: `${Math.min(
                contextMenu.y,
                window.innerHeight - 100
              )}px`,
            }}
            onClick={(event) =>
              event.stopPropagation()
            }
            onContextMenu={(event) =>
              event.preventDefault()
            }
          >
            <button
              type="button"
              onClick={() =>
                handleRename(contextMenu.item)
              }
              className="w-full flex items-center gap-3 px-3 py-2 text-left text-[13px] text-gray-300 hover:bg-white/5 hover:text-white transition"
            >
              <Pencil
                size={14}
                className="text-gray-400"
              />

              <span>Rename</span>
            </button>

            {/* IMPORT BUTTON */}

            <button
              type="button"
              disabled={
                contextMenu.item.type !== "file" ||
                importingFile ===
                  contextMenu.item.name
              }
              onClick={() =>
                handleImportToCineForge(
                  contextMenu.item
                )
              }
              className="w-full flex items-center gap-3 px-3 py-2 text-left text-[13px] text-purple-400 hover:bg-purple-500/10 hover:text-purple-300 transition disabled:opacity-40 disabled:cursor-not-allowed"
            >
              <FolderOpen size={14} />

              <span>
                {importingFile ===
                contextMenu.item.name
                  ? "Importing..."
                  : "Import to CineForge"}
              </span>
            </button>

            <button
              type="button"
              onClick={() =>
                handleDelete(contextMenu.item)
              }
              className="w-full flex items-center gap-3 px-3 py-2 text-left text-[13px] text-red-400 hover:bg-red-500/10 hover:text-red-300 transition"
            >
              <Trash2 size={14} />

              <span>Delete</span>
            </button>
          </div>
        )}

      </div>
    </aside>
  );
}

export default FileExplorer;