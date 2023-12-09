/*
Copyright 2023 NeuralBridge AI

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
 */

import React, { useState } from "react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { FunctionNode } from "./TraceGraph"; // Import your existing FunctionNode type
import { Rnd } from "react-rnd";
import "./CodeWindow.css";

interface CodeWindowProps {
  type: "Code";
  node: FunctionNode;
  icon?: React.ReactElement;
  onClose: () => void;
}

const CodeWindow: React.FC<CodeWindowProps> = ({ node, icon, onClose }) => {
  return (
    <Rnd
      className="code-window"
      dragHandleClassName="code-window__draghandle"
      default={{
        x: window.innerWidth / 2 - 300,
        y: window.innerHeight / 2 - 200,
        width: window.innerWidth / 2,
        height: window.innerHeight / 2,
      }}
      style={{ display: "grid" }}
    >
      <div className="code-window__draghandle">
        <button onClick={onClose} className="code-window__clearbutton">
          {icon && <div className="code-window__icon">{icon}</div>}
        </button>
        <strong className="code-window__header">Code</strong>
      </div>
      <div className="code-window__content">
        <SyntaxHighlighter language="python">
          {node.source_code.trim()}
        </SyntaxHighlighter>
      </div>
    </Rnd>
  );
};

export default CodeWindow;
