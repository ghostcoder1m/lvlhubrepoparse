import React, { useState } from 'react';
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  Box,
  Chip,
  IconButton,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions
} from '@mui/material';
import {
  PlayArrow as PlayArrowIcon,
  Pause as PauseIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Visibility as VisibilityIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

// Sample data - replace with actual API calls
const sampleWorkflows = [
  {
    id: 1,
    name: 'Lead Nurturing',
    description: 'Automated email sequence for new leads',
    status: 'active',
    steps: 5,
    leadsProcessed: 250,
    conversionRate: '15%',
    lastModified: '2024-01-15'
  },
  {
    id: 2,
    name: 'Welcome Series',
    description: 'Onboarding workflow for new customers',
    status: 'draft',
    steps: 3,
    leadsProcessed: 0,
    conversionRate: '0%',
    lastModified: '2024-01-14'
  },
  {
    id: 3,
    name: 'Re-engagement',
    description: 'Re-engage inactive customers',
    status: 'paused',
    steps: 4,
    leadsProcessed: 150,
    conversionRate: '8%',
    lastModified: '2024-01-13'
  }
];

const Workflows = () => {
  const navigate = useNavigate();
  const [workflows] = useState(sampleWorkflows);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [selectedWorkflow, setSelectedWorkflow] = useState(null);

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'success';
      case 'draft':
        return 'default';
      case 'paused':
        return 'warning';
      default:
        return 'default';
    }
  };

  const handleToggleStatus = (id) => {
    // TODO: Implement status toggle functionality
    console.log('Toggle status:', id);
  };

  const handleEdit = (id) => {
    // TODO: Implement edit functionality
    console.log('Edit workflow:', id);
  };

  const handleDelete = (workflow) => {
    setSelectedWorkflow(workflow);
    setDeleteDialogOpen(true);
  };

  const confirmDelete = () => {
    // TODO: Implement delete functionality
    console.log('Delete workflow:', selectedWorkflow.id);
    setDeleteDialogOpen(false);
    setSelectedWorkflow(null);
  };

  const handleVisualize = (id) => {
    navigate('/workflow-visualizer', { state: { workflowId: id } });
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" gutterBottom>
          Workflows
        </Typography>
        <Button variant="contained" color="primary">
          Create Workflow
        </Button>
      </Box>

      <Grid container spacing={3}>
        {workflows.map((workflow) => (
          <Grid item xs={12} md={6} lg={4} key={workflow.id}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h6" component="h2">
                    {workflow.name}
                  </Typography>
                  <Chip
                    label={workflow.status}
                    color={getStatusColor(workflow.status)}
                    size="small"
                  />
                </Box>
                <Typography color="text.secondary" sx={{ mb: 1.5 }}>
                  {workflow.description}
                </Typography>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Steps:</Typography>
                  <Typography variant="body2">{workflow.steps}</Typography>
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Leads Processed:</Typography>
                  <Typography variant="body2">{workflow.leadsProcessed}</Typography>
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Conversion Rate:</Typography>
                  <Typography variant="body2">{workflow.conversionRate}</Typography>
                </Box>
                <Typography variant="body2" color="text.secondary">
                  Last Modified: {workflow.lastModified}
                </Typography>
              </CardContent>
              <CardActions sx={{ justifyContent: 'flex-end' }}>
                <Tooltip title={workflow.status === 'active' ? 'Pause' : 'Activate'}>
                  <IconButton
                    size="small"
                    onClick={() => handleToggleStatus(workflow.id)}
                  >
                    {workflow.status === 'active' ? (
                      <PauseIcon fontSize="small" />
                    ) : (
                      <PlayArrowIcon fontSize="small" />
                    )}
                  </IconButton>
                </Tooltip>
                <Tooltip title="Visualize">
                  <IconButton
                    size="small"
                    onClick={() => handleVisualize(workflow.id)}
                  >
                    <VisibilityIcon fontSize="small" />
                  </IconButton>
                </Tooltip>
                <Tooltip title="Edit">
                  <IconButton
                    size="small"
                    onClick={() => handleEdit(workflow.id)}
                  >
                    <EditIcon fontSize="small" />
                  </IconButton>
                </Tooltip>
                <Tooltip title="Delete">
                  <IconButton
                    size="small"
                    onClick={() => handleDelete(workflow)}
                  >
                    <DeleteIcon fontSize="small" />
                  </IconButton>
                </Tooltip>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Dialog
        open={deleteDialogOpen}
        onClose={() => setDeleteDialogOpen(false)}
      >
        <DialogTitle>Confirm Delete</DialogTitle>
        <DialogContent>
          Are you sure you want to delete the workflow "{selectedWorkflow?.name}"?
          This action cannot be undone.
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>Cancel</Button>
          <Button onClick={confirmDelete} color="error">Delete</Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default Workflows;