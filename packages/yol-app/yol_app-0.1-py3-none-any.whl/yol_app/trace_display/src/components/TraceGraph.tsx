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

/**
 * TraceGraph Component
 *
 * This component visualizes a function trace in a graphical format. The data representation
 * utilizes nodes to depict function calls and edges to show relationships between calls.
 * Each node contains information about a function call like its name, arguments, return value, and latency.
 * Edges establish parent-child relationships between function calls.
 *
 * The data is processed from a structured JSON, which gets converted into nodes and edges compatible with the ReactFlow library.
 *
 * Components:
 * - TraceGraph: The primary component which integrates the processed data into ReactFlow for visualization.
 * - TraceGraphNode: A custom node visualization for the graph.
 *
 * Dependencies:
 * - react-flow-renderer: Provides the graphical flow visualization.
 */

import React, { useState, useEffect } from "react";
import ReactFlow, { Background, BezierEdge } from "react-flow-renderer";
import TraceGraphNode from "./TraceGraphNode";
import dagre from "dagre";

// Interfaces and Types

// Represents a structured data about a function call.
export interface FunctionNode {
  id: string;
  position: { x: number; y: number };
  function_name: string; // Name of the function.
  args: Record<string, any>; // Arguments passed to the function.
  kwargs: Record<string, any>; // Keyword arguments passed to the function.
  thread_id: number; // ID of the thread where the function was executed.
  children: FunctionNode[]; // Child function calls made from within this function.
  return: any; // Return value of the function.
  latency: number; // Time taken for function execution.
  source_code: string; // Source code of the function.
  execution_order: number;
  return_type: string; // Type of return value of the function.
}

// Holds the formatted data for a node.
interface NodeData {
  position: { x: number; y: number };
  id: string;
  function_name: string;
  args: any;
  return: any;
  source_code: string;
  thread_id: number;
  latency: string;
  return_type: string;
}

// Represents a visual node in the graph.
interface Node {
  id: string; // Unique ID for the node.
  type: string; // Type of the node, used for custom visualization.
  data: NodeData; // Formatted data displayed on the node.
  position: { x: number; y: number }; // Position of the node in the graph.
}

// Represents a visual edge/connection between nodes in the graph.
interface Edge {
  id: string; // Unique ID for the edge.
  source: string; // ID of the source node.
  target: string; // ID of the target node.
  animated: boolean; // Animation for the edge.
  label?: string;
  style?: { strokeWidth: number };
  labelStyle?: { fontSize: string };
}

// Represents the state of elements (both nodes and edges).
interface ElementState {
  nodes: Node[];
  edges: Edge[];
}

const nodeTypes = {
  traceGraphNode: TraceGraphNode, // Custom node visualization.
};

const edgeTypes = {
  customEdge: BezierEdge,
};

/**
 * Formats the raw function node data into a structured label for display.
 *
 * @param nodeData - Raw function data that needs to be formatted.
 * @returns The formatted data suitable for the graph node.
 */
const formatFunctionNodeLabel = (nodeData: FunctionNode): NodeData => {
  const formattedLatency = nodeData.latency
    ? `${nodeData.latency.toFixed(3)}ms`
    : "";

  return {
    position: nodeData.position,
    id: nodeData.id,
    function_name: nodeData.function_name,
    args: nodeData.args,
    return: nodeData.return,
    source_code: nodeData.source_code,
    thread_id: nodeData.thread_id,
    latency: formattedLatency,
    return_type: nodeData.return_type,
  };
};

/**
 * Converts the provided JSON data into nodes and edges for the graph.
 *
 * @param jsonData - The raw function trace data.
 * @returns Nodes and edges structured for ReactFlow.
 */

// Define a type for the layout direction as a union of possible string literals
type LayoutDirection = "TB" | "BT" | "LR" | "RL";

const applyGraphLayout = (
  nodes: Node[],
  edges: Edge[],
  direction: LayoutDirection = "TB"
) => {
  const g = new dagre.graphlib.Graph();
  g.setGraph({ rankdir: direction });
  g.setDefaultEdgeLabel(() => ({}));

  nodes.forEach((node) => {
    // Assuming each node has a fixed width and height for simplicity
    g.setNode(node.id, { width: 300, height: 450 });
  });

  edges.forEach((edge) => {
    g.setEdge(edge.source, edge.target);
  });

  dagre.layout(g);

  const layoutedNodes: Node[] = nodes.map((node) => {
    const nodeWithLayout = g.node(node.id);
    return {
      ...node,
      position: {
        x: nodeWithLayout.x - nodeWithLayout.width / 2,
        y: nodeWithLayout.y - nodeWithLayout.height / 2,
      },
    };
  });

  // No changes needed for the edges, but they are returned to keep the function signature consistent
  return { nodes: layoutedNodes, edges };
};
const convertToNodeStructure = (jsonData: FunctionNode): ElementState => {
  const nodes: Node[] = [];
  const edges: Edge[] = [];
  const queue: {
    node: FunctionNode;
    parentId?: string;
    depth: number;
    xOffset: number;
  }[] = [{ node: jsonData, depth: 0, xOffset: 0 }];

  let idCounter = 1;
  let xSpacing = 700; // horizontal space between nodes

  while (queue.length) {
    const { node, parentId, depth, xOffset } = queue.shift()!;
    const nodeId = `node-${idCounter++}`;
    node.id = nodeId;
    node.position = { x: xOffset, y: depth * 500 };
    nodes.push({
      id: nodeId,
      type: "traceGraphNode",
      data: formatFunctionNodeLabel(node),
      position: { x: xOffset, y: depth * 500 },
    });
    if (parentId) {
      edges.push({
        id: `edge-${parentId}-${nodeId}`,
        source: parentId,
        target: nodeId,
        animated: true,
        label: `${node.execution_order}`,
        style: { strokeWidth: 8 },
        labelStyle: { fontSize: "1.7em" },
      });
    }

    node.children.forEach((child, index) =>
      queue.push({
        node: child,
        parentId: nodeId,
        depth: depth + 1,
        xOffset: xOffset + (index - (node.children.length - 1) / 2) * xSpacing,
      })
    );
  }
  return { nodes, edges };
};

const TraceGraph: React.FC<{ jsonData: FunctionNode }> = ({ jsonData }) => {
  const [elements, setElements] = useState<ElementState>({
    nodes: [],
    edges: [],
  });
  useEffect(() => {
    const { nodes, edges } = convertToNodeStructure(jsonData);
    const { nodes: layoutedNodes, edges: layoutedEdges } = applyGraphLayout(
      nodes,
      edges
    );
    setElements({ nodes: layoutedNodes, edges: layoutedEdges });
  }, [jsonData]);

  return (
    <div style={{ height: "90vh" }}>
      <ReactFlow
        nodes={elements.nodes}
        edges={elements.edges}
        fitView={true}
        attributionPosition="bottom-right"
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
      >
        <Background color="#aaa" gap={16} />
      </ReactFlow>
    </div>
  );
};

export default TraceGraph;
