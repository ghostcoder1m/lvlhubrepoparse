import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Typography,
  Paper,
  Grid,
  Divider,
  List,
  ListItem,
  ListItemText,
  Chip,
  IconButton,
  CircularProgress,
} from '@mui/material';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  Psychology as AIIcon,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { format } from 'date-fns';
import { leadApi } from '../services/api';

export default function LeadDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: lead, isLoading: isLoadingLead } = useQuery({
    queryKey: ['lead', id],
    queryFn: async () => {
      const response = await leadApi.getLead(Number(id));
      return response.data;
    },
  });

  const { data: events = [], isLoading: isLoadingEvents } = useQuery({
    queryKey: ['leadEvents', id],
    queryFn: async () => {
      const response = await leadApi.getLeadEvents(Number(id));
      return response.data;
    },
  });

  const deleteMutation = useMutation({
    mutationFn: () => leadApi.deleteLead(Number(id)),
    onSuccess: () => {
      navigate('/leads');
    },
  });

  const scoreMutation = useMutation({
    mutationFn: () => leadApi.scoreLead(Number(id)),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['lead', id] });
    },
  });

  if (isLoadingLead) {
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
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          mb: 3,
        }}
      >
        <Typography variant="h4" component="h1">
          Lead Details
        </Typography>
        <Box>
          <IconButton
            onClick={() => navigate(`/leads/${id}/edit`)}
            sx={{ mr: 1 }}
          >
            <EditIcon />
          </IconButton>
          <IconButton
            onClick={() => {
              if (window.confirm('Are you sure you want to delete this lead?')) {
                deleteMutation.mutate();
              }
            }}
            color="error"
            sx={{ mr: 1 }}
          >
            <DeleteIcon />
          </IconButton>
          <Button
            variant="contained"
            startIcon={<AIIcon />}
            onClick={() => scoreMutation.mutate()}
            disabled={scoreMutation.isPending}
          >
            Update Score
          </Button>
        </Box>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Lead Information
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Typography color="text.secondary" gutterBottom>
                  Name
                </Typography>
                <Typography>
                  {lead.firstName} {lead.lastName}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography color="text.secondary" gutterBottom>
                  Email
                </Typography>
                <Typography>{lead.email}</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography color="text.secondary" gutterBottom>
                  Phone
                </Typography>
                <Typography>{lead.phone || 'N/A'}</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography color="text.secondary" gutterBottom>
                  Company
                </Typography>
                <Typography>{lead.company || 'N/A'}</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography color="text.secondary" gutterBottom>
                  Job Title
                </Typography>
                <Typography>{lead.jobTitle || 'N/A'}</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography color="text.secondary" gutterBottom>
                  Lead Score
                </Typography>
                <Chip
                  label={`${Math.round(lead.leadScore * 100)}%`}
                  color={
                    lead.leadScore >= 0.7
                      ? 'success'
                      : lead.leadScore >= 0.4
                      ? 'warning'
                      : 'error'
                  }
                />
              </Grid>
            </Grid>
          </Paper>

          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Event History
            </Typography>
            {isLoadingEvents ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', py: 2 }}>
                <CircularProgress />
              </Box>
            ) : (
              <List>
                {events.map((event, index) => (
                  <React.Fragment key={event.id}>
                    <ListItem>
                      <ListItemText
                        primary={event.eventType}
                        secondary={format(
                          new Date(event.timestamp),
                          'MMM d, yyyy HH:mm'
                        )}
                      />
                    </ListItem>
                    {index < events.length - 1 && <Divider />}
                  </React.Fragment>
                ))}
              </List>
            )}
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Timeline
            </Typography>
            <Box sx={{ mt: 2 }}>
              <Typography color="text.secondary" gutterBottom>
                Created
              </Typography>
              <Typography>
                {format(new Date(lead.createdAt), 'MMM d, yyyy HH:mm')}
              </Typography>
            </Box>
            <Box sx={{ mt: 2 }}>
              <Typography color="text.secondary" gutterBottom>
                Last Updated
              </Typography>
              <Typography>
                {format(new Date(lead.updatedAt), 'MMM d, yyyy HH:mm')}
              </Typography>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
} 