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

import React from "react";
import "./InputOutputWindow.css";
import { FunctionNode } from "./TraceGraph"; // Assuming this is the correct path
import { Argument, Return } from "../types"; // Import the types
import { Rnd } from "react-rnd";

interface InputOutputWindowProps {
  type: "Input" | "Output";
  node: FunctionNode;
  icon: React.ReactElement;
  onClose: () => void;
}

// Extending the Argument type with an additional 'isJson' property for internal use within the function
type ArgumentWithJson = Argument & { isJson: boolean };

// Extending the Argument type with an additional 'isJson' property for internal use within the function
type ReturnWithJson = Return & { isJson: boolean };

const argumentFormatter = (object: {
  [key: string]: any;
}): ArgumentWithJson[] => {
  return Object.entries(object).map(([key, value]): ArgumentWithJson => {
    let isJson = false;
    let formattedValue = " ";
    if (value === null) {
      formattedValue = "null";
    } else if (Array.isArray(value)) {
      formattedValue = `[${value
        .map(
          (v) => (
            typeof v === "object" ? (isJson = true) : (isJson = isJson),
            JSON.stringify(v, null, 2)
          )
        )
        .join(", ")}]`;
    } else if (typeof value === "object") {
      formattedValue = JSON.stringify(value, null, 2);
      isJson = true;
    } else {
      formattedValue = value.toString();
    }

    return {
      name: key,
      value: formattedValue.replace(/["]/g, ""),
      type: "",
      isJson: isJson,
    };
  });
};

const returnFormatter = (
  object: { [key: string]: any },
  return_type: string
): ReturnWithJson[] => {
  let isJson = false;
  return Object.entries(object).map(([key, value]): ReturnWithJson => {
    let formattedValue = " ";
    if (value === null) {
      formattedValue = "null";
    } else if (Array.isArray(value)) {
      formattedValue = `[${value
        .map(
          (v) => (
            typeof v === "object" ? (isJson = true) : (isJson = isJson),
            JSON.stringify(v, null, 2)
          )
        )
        .join(", ")}]`;
    } else if (typeof value === "object") {
      formattedValue = JSON.stringify(value, null, 2);
      isJson = true;
    } else {
      formattedValue = value.toString();
    }

    return {
      value:
        return_type === "dict" && key
          ? `${key}: ${formattedValue.replace(/["]/g, "")}`
          : formattedValue.replace(/["]/g, ""),
      type: "",
      isJson: isJson,
    };
  });
};

const InputOutputWindow: React.FC<InputOutputWindowProps> = ({
  type,
  node,
  icon,
  onClose,
}) => {
  // Determine content based on the type
  const content = type == "Input" ? node.args : node.return;
  let inputArguments: ArgumentWithJson[] = [];

  // data.args is converted to the format compatible with argumentFormatter function
  // {name: {value, type}} to {name: value}
  const compatibleFormat = Object.entries(node.args).reduce(
    (acc, [name, { value }]) => {
      acc[name] = value;
      return acc;
    },
    {} as Record<string, any>
  );

  if (
    compatibleFormat &&
    typeof compatibleFormat === "object" &&
    !Array.isArray(compatibleFormat)
  ) {
    inputArguments = argumentFormatter(compatibleFormat);
  }

  inputArguments.forEach((argument) => {
    argument.type = node.args[argument.name].type;
  });

  let outputReturns: ReturnWithJson[] = [];
  if (
    node.return &&
    typeof node.return === "object" &&
    !Array.isArray(node.return)
  ) {
    outputReturns = returnFormatter({ "": node.return }, node.return_type);
  } else if (node.return) {
    outputReturns = returnFormatter([node.return], node.return_type);
  }
  outputReturns.forEach((output, index) => {
    output.type = node.return_type;
  });

  const rndPosition = {
    x: node.position.x + 0, // offsetX is the horizontal offset you want to apply
    y: node.position.y + 0, // offsetY is the vertical offset
  };

  return (
    <Rnd
      className="input-output-window"
      dragHandleClassName="input-output-window__draghandle"
      default={{
        x: window.innerWidth / 2 - 300,
        y: window.innerHeight / 2 - 200,
        width: window.innerWidth / 2,
        height: window.innerHeight / 2,
      }}
      enableResizing={{
        bottom: true,
        bottomLeft: true,
        bottomRight: true,
        left: true,
        right: true,
        top: true,
        topLeft: true,
        topRight: true,
      }}
      style={{ display: "grid" }}
    >
      <div className="input-output-window__draghandle">
        <div className="input-output-window__header">
          <button
            onClick={onClose}
            className="input-output-window__clearbutton"
          >
            {icon}
          </button>
          <strong className="input-output-window__title">
            {type} of {node.function_name}
          </strong>
        </div>
      </div>
      <div className="input-output-window__content">
        <ul className="input-output-window__list">
          {type == "Input"
            ? inputArguments.map((item, index) => (
                <li key={index} className="input-output-window__item">
                  <>
                    <span className="input-output-window__name">
                      {(item as ArgumentWithJson).name} (
                      {(item as ArgumentWithJson).type}):
                    </span>
                    {item.isJson ? (
                      <pre>{item.value}</pre> // Wrap with <pre> if isObject is true
                    ) : (
                      " " + item.value // Render as is if not an object
                    )}
                  </>
                </li>
              ))
            : outputReturns.map((item, index) => (
                <li key={index} className="input-output-window__item">
                  <span className="input-output-button__name">
                    ({(item as ReturnWithJson).type}):
                  </span>
                  {item.isJson ? (
                    <pre>{item.value}</pre> // Wrap with <pre> if isObject is true
                  ) : (
                    " " + item.value // Render as is if not an object
                  )}
                </li>
              ))}
        </ul>
      </div>
    </Rnd>
  );
};

export default InputOutputWindow;
