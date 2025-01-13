import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Typography, Paper } from '@mui/material';
import { useMutation } from '@tanstack/react-query';
import { leadApi, CreateLeadDto } from '../services/api';
import LeadForm from '../components/LeadForm';

export default function CreateLead() {
  const navigate = useNavigate();

  const createMutation = useMutation({
    mutationFn: (data: CreateLeadDto) => leadApi.createLead(data),
    onSuccess: (response) => {
      navigate(`/leads/${response.data.id}`);
    },
  });

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Create Lead
      </Typography>
      <Paper sx={{ p: 3, maxWidth: 800, mx: 'auto' }}>
        <LeadForm
          onSubmit={(data) => createMutation.mutate(data as CreateLeadDto)}
          isLoading={createMutation.isPending}
        />
      </Paper>
    </Box>
  );
} 