import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Typography,
  Paper,
  Grid,
  Checkbox,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  IconButton,
  Divider,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import { ArrowBack as ArrowBackIcon } from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { campaignApi, leadApi } from '../services/api';

export default function CampaignLeads() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [isAddLeadsDialogOpen, setIsAddLeadsDialogOpen] = useState(false);
  const [selectedLeads, setSelectedLeads] = useState<number[]>([]);

  const { data: campaign, isLoading: isLoadingCampaign } = useQuery({
    queryKey: ['campaign', id],
    queryFn: async () => {
      const response = await campaignApi.getCampaign(Number(id));
      return response.data;
    },
  });

  const { data: campaignLeads = [], isLoading: isLoadingCampaignLeads } = useQuery({
    queryKey: ['campaignLeads', id],
    queryFn: async () => {
      const response = await campaignApi.getCampaignLeads(Number(id));
      return response.data;
    },
  });

  const { data: allLeads = [], isLoading: isLoadingAllLeads } = useQuery({
    queryKey: ['leads'],
    queryFn: async () => {
      const response = await leadApi.getLeads();
      return response.data;
    },
    enabled: isAddLeadsDialogOpen,
  });

  const addLeadsMutation = useMutation({
    mutationFn: (leadIds: number[]) =>
      campaignApi.addLeadsToCampaign(Number(id), leadIds),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['campaignLeads', id] });
      setIsAddLeadsDialogOpen(false);
      setSelectedLeads([]);
    },
  });

  const removeLeadsMutation = useMutation({
    mutationFn: (leadIds: number[]) =>
      campaignApi.removeLeadsFromCampaign(Number(id), leadIds),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['campaignLeads', id] });
      setSelectedLeads([]);
    },
  });

  const handleToggleLead = (leadId: number) => {
    setSelectedLeads((prev) =>
      prev.includes(leadId)
        ? prev.filter((id) => id !== leadId)
        : [...prev, leadId]
    );
  };

  const handleAddLeads = () => {
    addLeadsMutation.mutate(selectedLeads);
  };

  const handleRemoveLeads = () => {
    if (window.confirm('Are you sure you want to remove the selected leads from this campaign?')) {
      removeLeadsMutation.mutate(selectedLeads);
    }
  };

  if (isLoadingCampaign) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (!campaign) {
    return (
      <Box sx={{ mt: 4 }}>
        <Typography>Campaign not found</Typography>
      </Box>
    );
  }

  const availableLeads = allLeads.filter(
    (lead) => !campaignLeads.some((cl) => cl.id === lead.id)
  );

  return (
    <Box>
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          mb: 3,
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <IconButton
            onClick={() => navigate(`/campaigns/${id}`)}
            sx={{ mr: 2 }}
          >
            <ArrowBackIcon />
          </IconButton>
          <Typography variant="h4" component="h1">
            Manage Campaign Leads
          </Typography>
        </Box>
        <Box>
          {selectedLeads.length > 0 && (
            <Button
              variant="outlined"
              color="error"
              onClick={handleRemoveLeads}
              disabled={removeLeadsMutation.isPending}
              sx={{ mr: 2 }}
            >
              Remove Selected
            </Button>
          )}
          <Button
            variant="contained"
            onClick={() => setIsAddLeadsDialogOpen(true)}
          >
            Add Leads
          </Button>
        </Box>
      </Box>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Campaign: {campaign.name}
        </Typography>
        {isLoadingCampaignLeads ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', py: 2 }}>
            <CircularProgress />
          </Box>
        ) : (
          <List>
            {campaignLeads.map((lead, index) => (
              <React.Fragment key={lead.id}>
                <ListItem>
                  <ListItemIcon>
                    <Checkbox
                      checked={selectedLeads.includes(lead.id)}
                      onChange={() => handleToggleLead(lead.id)}
                    />
                  </ListItemIcon>
                  <ListItemText
                    primary={`${lead.firstName} ${lead.lastName}`}
                    secondary={lead.email}
                  />
                </ListItem>
                {index < campaignLeads.length - 1 && <Divider />}
              </React.Fragment>
            ))}
            {campaignLeads.length === 0 && (
              <Typography sx={{ py: 2, textAlign: 'center' }}>
                No leads in this campaign yet
              </Typography>
            )}
          </List>
        )}
      </Paper>

      <Dialog
        open={isAddLeadsDialogOpen}
        onClose={() => setIsAddLeadsDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Add Leads to Campaign</DialogTitle>
        <DialogContent>
          {isLoadingAllLeads ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', py: 2 }}>
              <CircularProgress />
            </Box>
          ) : (
            <List>
              {availableLeads.map((lead, index) => (
                <React.Fragment key={lead.id}>
                  <ListItem>
                    <ListItemIcon>
                      <Checkbox
                        checked={selectedLeads.includes(lead.id)}
                        onChange={() => handleToggleLead(lead.id)}
                      />
                    </ListItemIcon>
                    <ListItemText
                      primary={`${lead.firstName} ${lead.lastName}`}
                      secondary={lead.email}
                    />
                  </ListItem>
                  {index < availableLeads.length - 1 && <Divider />}
                </React.Fragment>
              ))}
              {availableLeads.length === 0 && (
                <Typography sx={{ py: 2, textAlign: 'center' }}>
                  No leads available to add
                </Typography>
              )}
            </List>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setIsAddLeadsDialogOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={handleAddLeads}
            disabled={selectedLeads.length === 0 || addLeadsMutation.isPending}
          >
            Add Selected
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
} 