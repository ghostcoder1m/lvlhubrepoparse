import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Box, Typography, Paper, CircularProgress } from '@mui/material';
import { useQuery, useMutation } from '@tanstack/react-query';
import { leadApi, UpdateLeadDto } from '../services/api';
import LeadForm from '../components/LeadForm';

export default function EditLead() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const { data: lead, isLoading } = useQuery({
    queryKey: ['lead', id],
    queryFn: async () => {
      const response = await leadApi.getLead(Number(id));
      return response.data;
    },
  });

  const updateMutation = useMutation({
    mutationFn: (data: UpdateLeadDto) =>
      leadApi.updateLead(Number(id), data),
    onSuccess: (response) => {
      navigate(`/leads/${response.data.id}`);
    },
  });

  if (isLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (!lead) {
    return (
      <Box sx={{ mt: 4 }}>
        <Typography>Lead not found</Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Edit Lead
      </Typography>
      <Paper sx={{ p: 3, maxWidth: 800, mx: 'auto' }}>
        <LeadForm
          lead={lead}
          onSubmit={(data) => updateMutation.mutate(data as UpdateLeadDto)}
          isLoading={updateMutation.isPending}
        />
      </Paper>
    </Box>
  );
} 