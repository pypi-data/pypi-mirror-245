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
import "./InputOutputButton.css";
import { Argument, Return } from "../types";
import MoreHoriz from "@mui/icons-material/MoreHoriz";

interface InputOutputButtonProps {
  type: "Input" | "Output";
  data: Argument[] | Return[];
  icon?: React.ReactElement;
  onClick: () => void;
}

const InputOutputButton: React.FC<InputOutputButtonProps> = ({
  type,
  data,
  icon,
  onClick,
}) => {
  const maxVisibleItems = 1; // Set the maximum number of visible items

  if (!Array.isArray(data)) {
    console.error(`Expected 'data' to be an array, but got:`, data);
    return null;
  }

  return (
    <div className="input-output-button" onClick={onClick}>
      <div className="input-output-button__header">
        {icon && (
          <div className="input-output-button__header--icon">{icon}</div>
        )}
        <strong className="input-output-button__header--text">{type}</strong>
      </div>
      <ul className="input-output-button__list">
        {data.slice(0, maxVisibleItems).map((item, index) => (
          <li
            key={index}
            className="input-output-button__item input-output-button__text--truncate"
          >
            {type === "Input" ? (
              <>
                <span className="input-output-button__name">
                  {(item as Argument).name} ({(item as Argument).type})
                </span>
                : {(item as Argument).value}
              </>
            ) : (
              <>
                <span className="input-output-button__name">
                  ({(item as Return).type})
                </span>
                : {(item as Return).value}
              </>
            )}
          </li>
        ))}
        <li className="input-output-button__overflow">
          {data.length > maxVisibleItems && (
            <span className="input-output-button__overflow-icon">
              <MoreHoriz />
            </span>
          )}
        </li>
      </ul>
    </div>
  );
};

export default InputOutputButton;
