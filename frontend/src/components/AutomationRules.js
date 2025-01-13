import React, { useState } from 'react';
import {
  Box,
  Typography,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Switch,
  FormControlLabel,
  IconButton,
  Paper,
  Grid
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  PlayArrow as PlayIcon,
  Pause as PauseIcon
} from '@mui/icons-material';

const AutomationRules = () => {
  const [rules, setRules] = useState([
    {
      id: 1,
      name: 'High Score Lead Follow-up',
      triggerType: 'LEAD_SCORE_CHANGED',
      conditions: 'Lead score > 80',
      actions: 'Send email template: High Value Lead',
      isActive: true
    },
    {
      id: 2,
      name: 'Welcome New Lead',
      triggerType: 'LEAD_CREATED',
      conditions: 'All new leads',
      actions: 'Send email template: Welcome Email',
      isActive: true
    }
  ]);
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedRule, setSelectedRule] = useState(null);

  const handleOpenDialog = (rule = null) => {
    setSelectedRule(rule);
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setSelectedRule(null);
    setOpenDialog(false);
  };

  const handleToggleActive = (ruleId) => {
    setRules(rules.map(rule => 
      rule.id === ruleId ? { ...rule, isActive: !rule.isActive } : rule
    ));
  };

  const handleDeleteRule = (ruleId) => {
    setRules(rules.filter(rule => rule.id !== ruleId));
  };

  return (
    <Box sx={{ p: 3, mt: 8 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">
          Automation Rules
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
        >
          Create Rule
        </Button>
      </Box>

      {rules.map(rule => (
        <Paper key={rule.id} sx={{ p: 2, mb: 2 }}>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} sm={3}>
              <Typography variant="h6">{rule.name}</Typography>
              <Typography variant="body2" color="textSecondary">
                Trigger: {rule.triggerType}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={3}>
              <Typography variant="body2">
                <strong>Conditions:</strong><br />
                {rule.conditions}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={3}>
              <Typography variant="body2">
                <strong>Actions:</strong><br />
                {rule.actions}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={3}>
              <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 1 }}>
                <IconButton 
                  onClick={() => handleToggleActive(rule.id)}
                  color={rule.isActive ? "primary" : "default"}
                >
                  {rule.isActive ? <PauseIcon /> : <PlayIcon />}
                </IconButton>
                <IconButton 
                  onClick={() => handleOpenDialog(rule)}
                  color="primary"
                >
                  <EditIcon />
                </IconButton>
                <IconButton 
                  onClick={() => handleDeleteRule(rule.id)}
                  color="error"
                >
                  <DeleteIcon />
                </IconButton>
              </Box>
            </Grid>
          </Grid>
        </Paper>
      ))}

      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        <DialogTitle>
          {selectedRule ? 'Edit Automation Rule' : 'Create Automation Rule'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
              label="Rule Name"
              fullWidth
              defaultValue={selectedRule?.name}
            />
            <FormControl fullWidth>
              <InputLabel>Trigger Type</InputLabel>
              <Select
                label="Trigger Type"
                defaultValue={selectedRule?.triggerType || 'LEAD_CREATED'}
              >
                <MenuItem value="LEAD_CREATED">Lead Created</MenuItem>
                <MenuItem value="LEAD_SCORE_CHANGED">Lead Score Changed</MenuItem>
                <MenuItem value="CAMPAIGN_JOINED">Campaign Joined</MenuItem>
              </Select>
            </FormControl>
            <TextField
              label="Conditions"
              fullWidth
              multiline
              rows={2}
              defaultValue={selectedRule?.conditions}
              helperText="Define conditions that must be met to trigger this rule"
            />
            <TextField
              label="Actions"
              fullWidth
              multiline
              rows={2}
              defaultValue={selectedRule?.actions}
              helperText="Define actions to take when conditions are met"
            />
            <FormControlLabel
              control={
                <Switch 
                  defaultChecked={selectedRule?.isActive ?? true}
                />
              }
              label="Active"
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button variant="contained" onClick={handleCloseDialog}>
            {selectedRule ? 'Save Changes' : 'Create Rule'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default AutomationRules; 