import { useEffect, useRef, useState } from "react";

function Editor({
  openTabs,
  activeFile,
  onTabSelect,
  onTabClose,
  fileContents,
  onSave,
}) {
  const editorRef = useRef(null);
  const savedRangeRef = useRef(null);

  const [files, setFiles] = useState({
    "scene_01.tnp": `<div>EXT. CITY STREET - NIGHT</div>
<div><br></div>
<div>Rain falls heavily across the empty street.</div>
<div><br></div>
<div>A car moves slowly through the darkness.</div>
<div><br></div>
<div>                    ARJUN</div>
<div>           We need to leave. Now.</div>`,

    "scene_02.tnp": `<div>INT. APARTMENT - MORNING</div>
<div><br></div>
<div>Sunlight enters through the window.</div>
<div><br></div>
<div>ARJUN sits quietly at the table.</div>
<div><br></div>
<div>His phone suddenly rings.</div>`,

    "scene_03.tnp": `<div>EXT. FOREST - EVENING</div>
<div><br></div>
<div>The forest is silent.</div>
<div><br></div>
<div>ARJUN walks between the trees.</div>
<div><br></div>
<div>Something moves behind him.</div>`,

    "scene_04.tnp": `<div>INT. OFFICE - DAY</div>
<div><br></div>
<div>Several files are scattered across the desk.</div>
<div><br></div>
<div>ARJUN picks up a photograph.</div>
<div><br></div>
<div>His expression changes.</div>`,

    "scene_05.tnp": `<div>INT. LABORATORY - EVENING</div>
<div><br></div>
<div>Machines hum in the background.</div>
<div><br></div>
<div>A monitor displays a strange pattern.</div>`,

    "scene_06.tnp": `<div>EXT. ROOFTOP - NIGHT</div>
<div><br></div>
<div>The city glows below.</div>
<div><br></div>
<div>ARJUN looks toward the horizon.</div>`,

    "scene_07.tnp": `<div>INT. LABORATORY - NIGHT</div>
<div><br></div>
<div>The laboratory is almost completely dark.</div>
<div><br></div>
<div>A single fluorescent light flickers above the long steel table.</div>
<div><br></div>
<div>ARJUN enters the room slowly.</div>
<div><br></div>
<div>He looks around.</div>
<div><br></div>
<div>                    ARJUN</div>
<div>           Is anyone here?</div>
<div><br></div>
<div>A strange sound comes from the other side of the laboratory.</div>
<div><br></div>
<div>Arjun moves toward the sound.</div>
<div><br></div>
<div>The light suddenly goes out.</div>`,

    "scene_08.tnp": `<div>INT. HOSPITAL - NIGHT</div>
<div><br></div>
<div>The corridor is empty.</div>
<br>
<div>A nurse walks toward the emergency room.</div>`,

    "scene_09.tnp": `<div>EXT. LABORATORY - MORNING</div>
<div><br></div>
<div>Police vehicles surround the building.</div>
<br>
<div>ARJUN stands behind the barrier.</div>`,
  });

  const continuityIssues = {
    "scene_07.tnp": {
      line: 1,
      message:
        "Scene 07 takes place at night, while the previous scene takes place during the evening. Check the timeline continuity.",
    },

    "scene_09.tnp": {
      line: 1,
      message:
        "The laboratory was shown at night in Scene 07, but this scene changes to morning. Verify the intended timeline.",
    },
  };

  const [currentLine, setCurrentLine] = useState(1);

  const [lineCount, setLineCount] = useState(1);

  const [activeFormats, setActiveFormats] = useState({
    bold: false,
    italic: false,
    underline: false,
    highlight: false,
    heading: null,
  });

  const escapeHtml = (text) =>
    text
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;");

  const saveSelection = () => {
    const editor = editorRef.current;
    const selection = window.getSelection();

    if (!editor || !selection || selection.rangeCount === 0) return;

    const range = selection.getRangeAt(0);

    if (!editor.contains(range.commonAncestorContainer)) return;

    savedRangeRef.current = range.cloneRange();
  };

  const restoreSelection = () => {
    const selection = window.getSelection();
    const range = savedRangeRef.current;

    if (!selection || !range) return false;

    try {
      selection.removeAllRanges();
      selection.addRange(range);
      return true;
    } catch {
      return false;
    }
  };

  const getSelection = () => {
    const selection = window.getSelection();

    if (!selection || selection.rangeCount === 0) {
      return null;
    }

    return selection;
  };

  const hasSelection = () => {
    const selection = getSelection();

    return Boolean(
      selection &&
        !selection.isCollapsed &&
        selection.toString().trim().length > 0
    );
  };

  const saveEditor = () => {
    if (!activeFile || !editorRef.current) return;

    setFiles((previous) => ({
      ...previous,
      [activeFile]: editorRef.current.innerHTML,
    }));
  };
  const handleSave = () => {
  if (!activeFile || !editorRef.current) return;

  const content = editorRef.current.innerHTML;

  saveEditor();

  if (onSave) {
    onSave(activeFile, content);
  }
};

  const runCommand = (command, value = null) => {
    if (!editorRef.current) return;

    if (!restoreSelection()) return;

    if (!hasSelection()) return;

    editorRef.current.focus();

    try {
      document.execCommand("styleWithCSS", false, true);
    } catch {
    }

    try {
      document.execCommand(command, false, value);
    } catch {
      return;
    }

    saveSelection();

    saveEditor();
    updateToolbarState();
    updateCurrentLine();
  };

  const toggleBold = () => {
    runCommand("bold");
  };

  const toggleItalic = () => {
    runCommand("italic");
  };

  const toggleUnderline = () => {
    runCommand("underline");
  };

  const toggleHighlight = () => {
    if (!editorRef.current) return;

    if (!restoreSelection()) return;
    if (!hasSelection()) return;

    editorRef.current.focus();

    try {
      document.execCommand("styleWithCSS", false, true);
    } catch {
    }

    const shouldRemove = activeFormats.highlight;

    const color = shouldRemove
      ? "transparent"
      : "rgba(180, 150, 40, 0.22)";

    try {
      document.execCommand("hiliteColor", false, color);
    } catch {
      try {
        document.execCommand("backColor", false, color);
      } catch {
        return;
      }
    }

    saveSelection();
    saveEditor();
    updateToolbarState();
    updateCurrentLine();
  };

  const getBlockElement = (node) => {
    let current =
      node?.nodeType === Node.TEXT_NODE ? node.parentElement : node;

    while (current && current !== editorRef.current) {
      if (
        ["DIV", "P", "H1", "H2", "H3"].includes(current.tagName)
      ) {
        return current;
      }

      current = current.parentElement;
    }

    return null;
  };

  const getSelectedBlocks = () => {
    const editor = editorRef.current;
    const selection = getSelection();

    if (!editor || !selection) return [];

    const range = selection.getRangeAt(0);

    if (!editor.contains(range.commonAncestorContainer)) {
      return [];
    }

    const blocks = Array.from(editor.children).filter((element) =>
      ["DIV", "P", "H1", "H2", "H3"].includes(element.tagName)
    );

    const selectedBlocks = blocks.filter((block) => {
      try {
        return range.intersectsNode(block);
      } catch {
        return false;
      }
    });

    if (selectedBlocks.length === 0) {
      const block = getBlockElement(range.startContainer);

      return block ? [block] : [];
    }

    return selectedBlocks;
  };

  const applyHeading = (heading) => {
    if (!editorRef.current) return;

    if (!restoreSelection()) return;
    if (!hasSelection()) return;

    editorRef.current.focus();

    const blocks = getSelectedBlocks();

    if (blocks.length === 0) return;

    const allSameHeading = blocks.every(
      (block) => block.tagName.toLowerCase() === heading
    );

    const newTag = allSameHeading ? "div" : heading;

    blocks.forEach((block) => {
      if (block.tagName.toLowerCase() === newTag) return;

      const replacement = document.createElement(newTag);

      while (block.firstChild) {
        replacement.appendChild(block.firstChild);
      }

      if (!replacement.firstChild) {
        replacement.appendChild(document.createElement("br"));
      }

      replacement.style.textAlign = block.style.textAlign;

      block.replaceWith(replacement);
    });

    restoreSelection();

    saveSelection();
    saveEditor();
    updateToolbarState();
    updateCurrentLine();
  };

  const isInsideHighlightedText = () => {
    const selection = getSelection();

    if (!selection || selection.rangeCount === 0) return false;

    let node = selection.anchorNode;

    if (node?.nodeType === Node.TEXT_NODE) {
      node = node.parentElement;
    }

    while (node && node !== editorRef.current) {
      if (
        node instanceof HTMLElement &&
        node.style.backgroundColor &&
        node.style.backgroundColor !== "transparent"
      ) {
        return true;
      }

      node = node.parentElement;
    }

    return false;
  };

  const getHeadingState = () => {
    const selection = getSelection();

    if (!selection || selection.rangeCount === 0) {
      return null;
    }

    const block = getBlockElement(selection.anchorNode);

    if (!block) return null;

    const tag = block.tagName.toLowerCase();

    if (["h1", "h2", "h3"].includes(tag)) {
      return tag;
    }

    return null;
  };

  const updateToolbarState = () => {
    const selection = getSelection();

    if (!selection || selection.rangeCount === 0) return;

    let bold = false;
    let italic = false;
    let underline = false;

    try {
      bold = document.queryCommandState("bold");
    } catch {}

    try {
      italic = document.queryCommandState("italic");
    } catch {}

    try {
      underline = document.queryCommandState("underline");
    } catch {}

    setActiveFormats({
      bold,
      italic,
      underline,
      highlight: isInsideHighlightedText(),
      heading: getHeadingState(),
    });
  };

  const getEditorBlocks = () => {
    if (!editorRef.current) return [];

    return Array.from(editorRef.current.children).filter((element) =>
      ["DIV", "P", "H1", "H2", "H3"].includes(element.tagName)
    );
  };

  const updateLineCount = () => {
    const count = getEditorBlocks().length;
    setLineCount(Math.max(count, 1));
  };

  const updateCurrentLine = () => {
    const editor = editorRef.current;
    const selection = getSelection();

    if (!editor || !selection || selection.rangeCount === 0) return;

    const blocks = getEditorBlocks();

    if (blocks.length === 0) {
      setCurrentLine(1);
      return;
    }

    const focusNode = selection.focusNode;
    const focusOffset = selection.focusOffset;

    if (!focusNode || !editor.contains(focusNode)) return;

    let currentBlock = getBlockElement(focusNode);

    if (!currentBlock && focusNode === editor) {
      const childAtCaret = editor.childNodes[focusOffset];

      currentBlock = getBlockElement(childAtCaret);

      if (!currentBlock && focusOffset >= editor.childNodes.length) {
        currentBlock = blocks[blocks.length - 1];
      }
    }

    if (!currentBlock) return;

    const index = blocks.indexOf(currentBlock);

    if (index !== -1) {
      setCurrentLine(index + 1);
    }
  };

  const syncEditorPosition = () => {
    requestAnimationFrame(() => {
      updateLineCount();
      updateCurrentLine();
      updateToolbarState();
    });
  };

  const handleKeyDown = (event) => {
    if (
  (event.ctrlKey || event.metaKey) &&
  event.key.toLowerCase() === "s"
) {
  event.preventDefault();
  handleSave();
  return;
}
    if (!(event.ctrlKey || event.metaKey)) return;

    const key = event.key.toLowerCase();

    if (key === "b") {
      event.preventDefault();
      toggleBold();
    }

    if (key === "i") {
      event.preventDefault();
      toggleItalic();
    }

    if (key === "u") {
      event.preventDefault();
      toggleUnderline();
    }

    if (key === "enter") {
      setTimeout(() => {
        updateLineCount();
        updateCurrentLine();
      }, 0);
    }
  };

  const handleInput = () => {
    saveEditor();
    saveSelection();
    syncEditorPosition();
  };

  const handleSelectionChange = () => {
    const editor = editorRef.current;

    if (!editor) return;

    const selection = getSelection();

    if (!selection || selection.rangeCount === 0) return;

    if (!editor.contains(selection.anchorNode)) return;

    saveSelection();
    syncEditorPosition();
  };

  useEffect(() => {
    if (!activeFile || !editorRef.current) return;

    /*
     * Prefer real file content supplied by Studio.
     *
     * If the file came from the local File Explorer,
     * fileContents[activeFile] will contain its actual text.
     *
     * If it is one of the existing mock .tnp files,
     * we fall back to the old local files state.
     */
    const content =
      fileContents?.[activeFile] ??
      files[activeFile] ??
      "";

    editorRef.current.innerHTML = content;

    savedRangeRef.current = null;

    setCurrentLine(1);
    updateLineCount();

    setTimeout(() => {
      editorRef.current?.focus();
      updateLineCount();
    }, 0);
  }, [activeFile, fileContents, files]);

  useEffect(() => {
    const editor = editorRef.current;

    if (!editor) return;

    const observer = new MutationObserver(() => {
      syncEditorPosition();
    });

    observer.observe(editor, {
      childList: true,
      subtree: true,
      characterData: true,
    });

    updateLineCount();
    updateCurrentLine();

    return () => observer.disconnect();
  }, [activeFile]);

  useEffect(() => {
    document.addEventListener(
      "selectionchange",
      handleSelectionChange
    );

    return () => {
      document.removeEventListener(
        "selectionchange",
        handleSelectionChange
      );
    };
  });

  const issue = continuityIssues[activeFile];

  if (!activeFile) {
    return (
      <main className="flex-1 min-w-0 bg-[#0d0f12] flex items-center justify-center">
        <div className="text-center">
          <div className="text-gray-500 text-sm">
            No file open
          </div>

          <p className="text-gray-600 text-xs mt-2">
            Select a file from the Explorer
          </p>
        </div>
      </main>
    );
  }

  return (
    <main className="flex-1 min-w-0 bg-[#0d0f12] flex flex-col overflow-hidden">

      <div className="h-10 shrink-0 bg-[#15171a] border-b border-[#292c32] flex items-center overflow-x-auto">
        {openTabs.map((fileName) => (
          <div
            key={fileName}
            onClick={() => onTabSelect(fileName)}
            className={`
              h-full
              min-w-36
              max-w-50
              px-3
              flex
              items-center
              gap-2
              border-r border-[#292c32]
              cursor-pointer
              transition
              ${
                activeFile === fileName
                  ? "bg-[#0d0f12] text-gray-200"
                  : "bg-[#15171a] text-gray-500 hover:text-gray-300"
              }
            `}
          >
            <span className="text-purple-400 text-xs">
              ▤
            </span>

            <span className="text-xs truncate flex-1">
              {fileName}
            </span>

            <button
              type="button"
              onClick={(event) => {
                event.stopPropagation();
                onTabClose(fileName);
              }}
              className="
                w-5 h-5
                rounded
                flex items-center justify-center
                text-gray-500
                hover:text-gray-200
                hover:bg-[#292c32]
                transition
              "
              title="Close"
            >
              ×
            </button>
          </div>
        ))}
      </div>

      <div className="h-11 shrink-0 bg-[#111316] border-b border-[#292c32] flex items-center px-4 gap-1">

        <button
          type="button"
          onMouseDown={(event) => {
            event.preventDefault();
            toggleBold();
          }}
          className={`
            w-8 h-8 rounded
            flex items-center justify-center
            font-bold text-sm
            transition
            ${
              activeFormats.bold
                ? "bg-purple-500/20 text-purple-300 ring-1 ring-purple-500/30"
                : "text-gray-400 hover:bg-[#25282d] hover:text-white"
            }
          `}
          title="Bold"
        >
          B
        </button>

        <button
          type="button"
          onMouseDown={(event) => {
            event.preventDefault();
            toggleItalic();
          }}
          className={`
            w-8 h-8 rounded
            flex items-center justify-center
            italic text-sm
            transition
            ${
              activeFormats.italic
                ? "bg-purple-500/20 text-purple-300 ring-1 ring-purple-500/30"
                : "text-gray-400 hover:bg-[#25282d] hover:text-white"
            }
          `}
          title="Italic"
        >
          I
        </button>

        <button
          type="button"
          onMouseDown={(event) => {
            event.preventDefault();
            toggleUnderline();
          }}
          className={`
            w-8 h-8 rounded
            flex items-center justify-center
            underline text-sm
            transition
            ${
              activeFormats.underline
                ? "bg-purple-500/20 text-purple-300 ring-1 ring-purple-500/30"
                : "text-gray-400 hover:bg-[#25282d] hover:text-white"
            }
          `}
          title="Underline"
        >
          U
        </button>

        <div className="w-px h-5 bg-[#292c32] mx-1" />

        <button
          type="button"
          onMouseDown={(event) => {
            event.preventDefault();
            toggleHighlight();
          }}
          className={`
            w-8 h-8 rounded
            flex items-center justify-center
            text-sm font-bold
            transition
            ${
              activeFormats.highlight
                ? "bg-[#b49a28]/15 text-[#e2d37d] ring-1 ring-[#b49a28]/25"
                : "text-[#c9bb70] hover:bg-[#25282d] hover:text-[#e2d37d]"
            }
          `}
          title="Highlight / Remove Highlight"
        >
          <span className="relative">
            H
            <span className="absolute left-0 right-0 bottom-0.5 h-0.5 bg-[#b49a28]/60" />
          </span>
        </button>

        <div className="w-px h-5 bg-[#292c32] mx-1" />

        <button
          type="button"
          onMouseDown={(event) => {
            event.preventDefault();
            applyHeading("h1");
          }}
          className={`
            px-2 h-8 rounded
            flex items-center justify-center
            text-xs font-bold
            transition
            ${
              activeFormats.heading === "h1"
                ? "bg-purple-500/20 text-purple-300 ring-1 ring-purple-500/30"
                : "text-gray-400 hover:bg-[#25282d] hover:text-white"
            }
          `}
          title="Heading 1 / Remove Heading"
        >
          H1
        </button>

        <button
          type="button"
          onMouseDown={(event) => {
            event.preventDefault();
            applyHeading("h2");
          }}
          className={`
            px-2 h-8 rounded
            flex items-center justify-center
            text-xs font-bold
            transition
            ${
              activeFormats.heading === "h2"
                ? "bg-purple-500/20 text-purple-300 ring-1 ring-purple-500/30"
                : "text-gray-400 hover:bg-[#25282d] hover:text-white"
            }
          `}
          title="Heading 2 / Remove Heading"
        >
          H2
        </button>

        <button
          type="button"
          onMouseDown={(event) => {
            event.preventDefault();
            applyHeading("h3");
          }}
          className={`
            px-2 h-8 rounded
            flex items-center justify-center
            text-xs font-bold
            transition
            ${
              activeFormats.heading === "h3"
                ? "bg-purple-500/20 text-purple-300 ring-1 ring-purple-500/30"
                : "text-gray-400 hover:bg-[#25282d] hover:text-white"
            }
          `}
          title="Heading 3 / Remove Heading"
        >
          H3
        </button>
      </div>

      <div className="flex-1 min-h-0 overflow-auto">
        <div className="min-w-162.5 flex">

          <div
            className="
              w-14
              shrink-0
              pt-6
              pr-3
              text-right
              select-none
              border-r border-[#1d2025]
              bg-[#101215]
            "
          >
            {Array.from({ length: lineCount }, (_, index) => {
              const lineNumber = index + 1;

              return (
                <div
                  key={lineNumber}
                  className={`
                    min-h-6
                    text-[12px]
                    leading-6
                    ${
                      issue?.line === lineNumber
                        ? "text-yellow-400 font-semibold"
                        : currentLine === lineNumber
                        ? "text-gray-400"
                        : "text-gray-600"
                    }
                  `}
                >
                  {lineNumber}
                </div>
              );
            })}
          </div>

          <div className="flex-1 bg-[#0d0f12]">
            <div
              ref={editorRef}
              contentEditable
              suppressContentEditableWarning
              spellCheck={false}
              onInput={handleInput}
              onKeyDown={handleKeyDown}
              onMouseUp={() => {
                saveSelection();
                syncEditorPosition();
              }}
              onKeyUp={() => {
                saveSelection();
                syncEditorPosition();
              }}
              onBlur={saveSelection}
              className="
                min-h-162.5
                p-6
                outline-none
                text-[14px]
                leading-6
                text-gray-300
                font-mono
                whitespace-pre-wrap
                wrap-break-word

                [&_div]:min-h-6
                [&_div]:leading-6

                [&_h1]:text-2xl
                [&_h1]:font-bold
                [&_h1]:leading-8
                [&_h1]:my-3
                [&_h1]:text-gray-100

                [&_h2]:text-xl
                [&_h2]:font-bold
                [&_h2]:leading-7
                [&_h2]:my-2
                [&_h2]:text-gray-100

                [&_h3]:text-lg
                [&_h3]:font-semibold
                [&_h3]:leading-6
                [&_h3]:my-2
                [&_h3]:text-gray-100

                [&_b]:text-gray-100
                [&_strong]:text-gray-100
                [&_i]:text-gray-200
                [&_em]:text-gray-200
                [&_u]:decoration-gray-300
              "
            />
          </div>
        </div>
      </div>

      {issue && (
        <div className="shrink-0 border-t border-[#292c32] bg-[#15171a]">
          <div className="px-4 py-3 flex items-start gap-3">

            <div
              className="
                w-7 h-7
                rounded-md
                bg-yellow-500/10
                border border-yellow-500/20
                flex items-center justify-center
                text-yellow-400
                shrink-0
              "
            >
              !
            </div>

            <div className="min-w-0">
              <div className="flex items-center gap-2 flex-wrap">

                <h3 className="text-xs font-semibold text-gray-200">
                  Continuity Issue
                </h3>

                <span
                  className="
                    px-2 py-0.5
                    rounded-full
                    text-[10px]
                    bg-yellow-500/10
                    text-yellow-400
                    border border-yellow-500/20
                  "
                >
                  Warning
                </span>

                <span
                  className="
                    px-2 py-0.5
                    rounded-full
                    text-[10px]
                    bg-[#24262b]
                    text-gray-400
                  "
                >
                  Line {issue.line}
                </span>
              </div>

              <p className="text-xs text-gray-500 mt-1 leading-5">
                {issue.message}
              </p>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}

export default Editor;