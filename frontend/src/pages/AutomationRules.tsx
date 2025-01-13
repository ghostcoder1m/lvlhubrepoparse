import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Typography,
  Paper,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  ListItemIcon,
  Switch,
  IconButton,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Grid,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { automationApi, type AutomationRule } from '../services/api';

export default function AutomationRules() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [openDialog, setOpenDialog] = React.useState(false);
  const [selectedRule, setSelectedRule] = React.useState<AutomationRule | null>(null);

  const { data: rules = [], isLoading } = useQuery({
    queryKey: ['automation-rules'],
    queryFn: async () => {
      const response = await automationApi.getRules();
      return response.data;
    },
  });

  const toggleMutation = useMutation({
    mutationFn: ({ id, isActive }: { id: number; isActive: boolean }) =>
      automationApi.toggleRule(id, isActive),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['automation-rules'] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: automationApi.deleteRule,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['automation-rules'] });
    },
  });

  const handleToggle = (rule: AutomationRule) => {
    toggleMutation.mutate({ id: rule.id, isActive: !rule.isActive });
  };

  const handleDelete = (id: number) => {
    if (window.confirm('Are you sure you want to delete this automation rule?')) {
      deleteMutation.mutate(id);
    }
  };

  return (
    <Box sx={{ height: '100%', width: '100%' }}>
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          mb: 2,
        }}
      >
        <Typography variant="h4" component="h1">
          Automation Rules
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => navigate('/automation/rules/new')}
        >
          Create Rule
        </Button>
      </Box>

      <Paper sx={{ p: 2 }}>
        {isLoading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 2 }}>
            Loading...
          </Box>
        ) : (
          <List>
            {rules.map((rule) => (
              <ListItem key={rule.id} divider>
                <ListItemText
                  primary={rule.name}
                  secondary={`Trigger: ${rule.triggerType.replace('_', ' ')} | Actions: ${rule.actions.length}`}
                />
                <ListItemSecondaryAction>
                  <Switch
                    edge="end"
                    checked={rule.isActive}
                    onChange={() => handleToggle(rule)}
                  />
                  <Tooltip title="Edit">
                    <IconButton
                      onClick={() => navigate(`/automation/rules/${rule.id}/edit`)}
                    >
                      <EditIcon />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Delete">
                    <IconButton
                      onClick={() => handleDelete(rule.id)}
                      disabled={deleteMutation.isPending}
                    >
                      <DeleteIcon />
                    </IconButton>
                  </Tooltip>
                </ListItemSecondaryAction>
              </ListItem>
            ))}
          </List>
        )}
      </Paper>
    </Box>
  );
} 