import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Box, Typography, Paper, CircularProgress } from '@mui/material';
import { useQuery, useMutation } from '@tanstack/react-query';
import { campaignApi, UpdateCampaignDto } from '../services/api';
import CampaignForm from '../components/CampaignForm';

export default function EditCampaign() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const { data: campaign, isLoading } = useQuery({
    queryKey: ['campaign', id],
    queryFn: async () => {
      const response = await campaignApi.getCampaign(Number(id));
      return response.data;
    },
  });

  const updateMutation = useMutation({
    mutationFn: (data: UpdateCampaignDto) =>
      campaignApi.updateCampaign(Number(id), data),
    onSuccess: (response) => {
      navigate(`/campaigns/${response.data.id}`);
    },
  });

  if (isLoading) {
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

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Edit Campaign
      </Typography>
      <Paper sx={{ p: 3, maxWidth: 800, mx: 'auto' }}>
        <CampaignForm
          campaign={campaign}
          onSubmit={(data) => updateMutation.mutate(data as UpdateCampaignDto)}
          isLoading={updateMutation.isPending}
        />
      </Paper>
    </Box>
  );
} 