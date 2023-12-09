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

import React, { useContext, useEffect, useState } from "react";
import { TraceGraphContext } from "./TraceGraphContext";
import InputOutputWindow from "./InputOutputWindow";
import CloseIcon from "@mui/icons-material/CloseRounded";
import CodeWindow from "./CodeWindow";

const NodeWindows: React.FC = () => {
  const context = useContext(TraceGraphContext);

  // Local state to force re-render
  const [localWindows, setLocalWindows] = useState(context?.windows);
  const [visibleWindowId, setVisibleWindowId] = useState<
    string | null | undefined
  >(context?.visibleWindowId);
  useEffect(() => {
    if (context) {
      // Update local state when context changes
      setLocalWindows(context.windows);
      setVisibleWindowId(context.visibleWindowId || null);
    }
  }, [context?.windows, context?.visibleWindowId]); // Dependency on context's windows object

  if (!context) {
    throw new Error("NodeWindows must be used within a TraceGraphProvider");
  }

  const { hideWindow } = context;

  return (
    <>
      {localWindows &&
        Object.entries(localWindows).map(([key, windowData]) => {
          if (windowData.visible && key === visibleWindowId) {
            const [node, nodeNumber, windowType] = key.split("-");
            const nodeId = node + "-" + nodeNumber;
            const isInput = windowType === "Input";

            if (windowType === "Output" || windowType === "Input") {
              return (
                windowData.visible && (
                  <InputOutputWindow
                    key={key}
                    type={isInput ? "Input" : "Output"}
                    node={windowData.data}
                    icon={<CloseIcon />}
                    onClose={() =>
                      hideWindow(
                        nodeId.toString(),
                        isInput ? "Input" : "Output",
                        windowData.data
                      )
                    }
                  />
                )
              );
            } else {
              return (
                windowData.visible && (
                  <CodeWindow
                    key={key}
                    type="Code"
                    node={windowData.data}
                    icon={<CloseIcon />}
                    onClose={() =>
                      hideWindow(nodeId.toString(), "Code", windowData.data)
                    }
                  />
                )
              );
            }
          }
        })}
    </>
  );
};

export default NodeWindows;
