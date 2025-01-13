import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Typography, Paper } from '@mui/material';
import { useMutation } from '@tanstack/react-query';
import { campaignApi, CreateCampaignDto } from '../services/api';
import CampaignForm from '../components/CampaignForm';

export default function CreateCampaign() {
  const navigate = useNavigate();

  const createMutation = useMutation({
    mutationFn: (data: CreateCampaignDto) => campaignApi.createCampaign(data),
    onSuccess: (response) => {
      navigate(`/campaigns/${response.data.id}`);
    },
  });

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Create Campaign
      </Typography>
      <Paper sx={{ p: 3, maxWidth: 800, mx: 'auto' }}>
        <CampaignForm
          onSubmit={(data) => createMutation.mutate(data as CreateCampaignDto)}
          isLoading={createMutation.isPending}
        />
      </Paper>
    </Box>
  );
} 