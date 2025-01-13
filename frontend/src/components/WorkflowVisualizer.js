import React, { useState, useCallback } from 'react';
import ReactFlow, {
  Controls,
  Background,
  applyEdgeChanges,
  applyNodeChanges,
  addEdge,
} from 'reactflow';
import { useLocation } from 'react-router-dom';
import { Box, Typography, Paper, Container } from '@mui/material';
import 'reactflow/dist/style.css';

// Sample workflow data - replace with actual API calls
const workflowsData = {
  1: {
    name: 'Lead Nurturing',
    nodes: [
      {
        id: 'start',
        type: 'input',
        data: { label: 'New Lead' },
        position: { x: 250, y: 5 },
      },
      {
        id: 'email1',
        data: { label: 'Welcome Email' },
        position: { x: 250, y: 100 },
      },
      {
        id: 'wait1',
        data: { label: 'Wait 2 Days' },
        position: { x: 250, y: 200 },
      },
      {
        id: 'email2',
        data: { label: 'Follow-up Email' },
        position: { x: 250, y: 300 },
      },
      {
        id: 'condition1',
        data: { label: 'Opened?' },
        position: { x: 250, y: 400 },
      },
      {
        id: 'email3',
        data: { label: 'Engagement Email' },
        position: { x: 100, y: 500 },
      },
      {
        id: 'email4',
        data: { label: 'Re-engagement Email' },
        position: { x: 400, y: 500 },
      },
      {
        id: 'end',
        type: 'output',
        data: { label: 'End' },
        position: { x: 250, y: 600 },
      },
    ],
    edges: [
      { id: 'e1-2', source: 'start', target: 'email1', animated: true },
      { id: 'e2-3', source: 'email1', target: 'wait1', animated: true },
      { id: 'e3-4', source: 'wait1', target: 'email2', animated: true },
      { id: 'e4-5', source: 'email2', target: 'condition1', animated: true },
      { id: 'e5-6', source: 'condition1', target: 'email3', animated: true, label: 'Yes' },
      { id: 'e5-7', source: 'condition1', target: 'email4', animated: true, label: 'No' },
      { id: 'e6-8', source: 'email3', target: 'end', animated: true },
      { id: 'e7-8', source: 'email4', target: 'end', animated: true },
    ],
  },
  // Add more workflow templates as needed
};

const WorkflowVisualizer = () => {
  const location = useLocation();
  const workflowId = location.state?.workflowId || 1; // Default to workflow 1 if no ID provided
  const workflow = workflowsData[workflowId];

  const [nodes, setNodes] = useState(workflow.nodes);
  const [edges, setEdges] = useState(workflow.edges);

  const onNodesChange = useCallback(
    (changes) => setNodes((nds) => applyNodeChanges(changes, nds)),
    []
  );

  const onEdgesChange = useCallback(
    (changes) => setEdges((eds) => applyEdgeChanges(changes, eds)),
    []
  );

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    []
  );

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Paper sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          {workflow.name} - Workflow Visualizer
        </Typography>
        <Box sx={{ width: '100%', height: '70vh', mt: 3 }}>
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            fitView
            attributionPosition="bottom-right"
          >
            <Background />
            <Controls />
          </ReactFlow>
        </Box>
      </Paper>
    </Container>
  );
};

export default WorkflowVisualizer;