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

import React, { createContext, useState, ReactNode } from "react";
import { FunctionNode } from "./TraceGraph"; // Import your existing FunctionNode type
import { Argument, Return } from "../types"; // Import the types

interface WindowState {
  data: FunctionNode;
  visible: boolean;
}

interface TraceGraphContextProps {
  windows: Record<string, WindowState>;
  visibleWindowId: string | null; // The ID of the currently visible window, or null if none are visible
  showWindow: (
    nodeId: string,
    type: "Input" | "Output" | "Code",
    data: FunctionNode
  ) => void;
  hideWindow: (
    nodeId: string,
    type: "Input" | "Output" | "Code",
    data: FunctionNode
  ) => void;
}

export const TraceGraphContext = createContext<TraceGraphContextProps | null>(
  null
);

export const TraceGraphProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [windows, setWindows] = useState<Record<string, WindowState>>({});
  const [visibleWindowId, setVisibleWindowId] = useState<string | null>(null);

  const showWindow = (
    nodeId: string,
    type: "Input" | "Output" | "Code",
    data: FunctionNode
  ) => {
    const windowId = `${nodeId}-${type}`;
    setWindows((prev) => ({
      ...prev,
      [`${nodeId}-${type}`]: { data, visible: true },
    }));
    setVisibleWindowId(windowId); // Set this window as the visible one
  };

  const hideWindow = (
    nodeId: string,
    type: "Input" | "Output" | "Code",
    data: FunctionNode
  ) => {
    setVisibleWindowId(null); // No window is visible
    setWindows((prev) => ({
      ...prev,
      [`${nodeId}-${type}`]: { data, visible: false },
    }));
  };

  return (
    <TraceGraphContext.Provider
      value={{ windows, visibleWindowId, showWindow, hideWindow }}
    >
      {children}
    </TraceGraphContext.Provider>
  );
};
