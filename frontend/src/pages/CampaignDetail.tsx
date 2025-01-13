import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Typography,
  Paper,
  Grid,
  Chip,
  IconButton,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  ListItemSecondaryAction,
  Divider,
} from '@mui/material';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  PlayArrow as PlayIcon,
  Pause as PauseIcon,
  Person as PersonIcon,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { format } from 'date-fns';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { campaignApi, Campaign } from '../services/api';

const getStatusColor = (status: Campaign['status']) => {
  switch (status) {
    case 'active':
      return 'success';
    case 'paused':
      return 'warning';
    case 'completed':
      return 'info';
    default:
      return 'default';
  }
};

export default function CampaignDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: campaign, isLoading: isLoadingCampaign } = useQuery({
    queryKey: ['campaign', id],
    queryFn: async () => {
      const response = await campaignApi.getCampaign(Number(id));
      return response.data;
    },
  });

  const { data: leads = [], isLoading: isLoadingLeads } = useQuery({
    queryKey: ['campaignLeads', id],
    queryFn: async () => {
      const response = await campaignApi.getCampaignLeads(Number(id));
      return response.data;
    },
  });

  const deleteMutation = useMutation({
    mutationFn: () => campaignApi.deleteCampaign(Number(id)),
    onSuccess: () => {
      navigate('/campaigns');
    },
  });

  const statusMutation = useMutation({
    mutationFn: async (action: 'launch' | 'pause' | 'resume') => {
      switch (action) {
        case 'launch':
          return campaignApi.launchCampaign(Number(id));
        case 'pause':
          return campaignApi.pauseCampaign(Number(id));
        case 'resume':
          return campaignApi.resumeCampaign(Number(id));
      }
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['campaign', id] });
    },
  });

  const handleStatusChange = (currentStatus: Campaign['status']) => {
    if (currentStatus === 'draft') {
      statusMutation.mutate('launch');
    } else if (currentStatus === 'active') {
      statusMutation.mutate('pause');
    } else if (currentStatus === 'paused') {
      statusMutation.mutate('resume');
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

  const metricsData = [
    { name: 'Sent', value: campaign.metrics.sent },
    { name: 'Delivered', value: campaign.metrics.delivered },
    { name: 'Opened', value: campaign.metrics.opened },
    { name: 'Clicked', value: campaign.metrics.clicked },
    { name: 'Converted', value: campaign.metrics.converted },
  ];

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
          Campaign Details
        </Typography>
        <Box>
          <IconButton
            onClick={() => navigate(`/campaigns/${id}/edit`)}
            sx={{ mr: 1 }}
          >
            <EditIcon />
          </IconButton>
          <IconButton
            onClick={() => {
              if (window.confirm('Are you sure you want to delete this campaign?')) {
                deleteMutation.mutate();
              }
            }}
            color="error"
            sx={{ mr: 1 }}
          >
            <DeleteIcon />
          </IconButton>
          {campaign.status !== 'completed' && (
            <Button
              variant="contained"
              startIcon={campaign.status === 'active' ? <PauseIcon /> : <PlayIcon />}
              onClick={() => handleStatusChange(campaign.status)}
              disabled={statusMutation.isPending}
            >
              {campaign.status === 'active'
                ? 'Pause Campaign'
                : campaign.status === 'paused'
                ? 'Resume Campaign'
                : 'Launch Campaign'}
            </Button>
          )}
        </Box>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Campaign Information
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Typography color="text.secondary" gutterBottom>
                  Name
                </Typography>
                <Typography>{campaign.name}</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography color="text.secondary" gutterBottom>
                  Type
                </Typography>
                <Typography>{campaign.type.toUpperCase()}</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography color="text.secondary" gutterBottom>
                  Status
                </Typography>
                <Chip
                  label={campaign.status.toUpperCase()}
                  color={getStatusColor(campaign.status)}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography color="text.secondary" gutterBottom>
                  Target Audience
                </Typography>
                <Typography>{campaign.targetAudience}</Typography>
              </Grid>
              <Grid item xs={12}>
                <Typography color="text.secondary" gutterBottom>
                  Description
                </Typography>
                <Typography>{campaign.description}</Typography>
              </Grid>
            </Grid>
          </Paper>

          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Campaign Metrics
            </Typography>
            <Box sx={{ height: 300, mt: 2 }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={metricsData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="value" fill="#2563eb" />
                </BarChart>
              </ResponsiveContainer>
            </Box>
          </Paper>

          <Paper sx={{ p: 3 }}>
            <Box
              sx={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                mb: 2,
              }}
            >
              <Typography variant="h6">Campaign Leads</Typography>
              <Button
                variant="outlined"
                startIcon={<PersonIcon />}
                onClick={() => navigate(`/campaigns/${id}/leads`)}
              >
                Manage Leads
              </Button>
            </Box>
            {isLoadingLeads ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', py: 2 }}>
                <CircularProgress />
              </Box>
            ) : (
              <List>
                {leads.map((lead, index) => (
                  <React.Fragment key={lead.id}>
                    <ListItem>
                      <ListItemText
                        primary={`${lead.firstName} ${lead.lastName}`}
                        secondary={lead.email}
                      />
                      <ListItemSecondaryAction>
                        <IconButton
                          size="small"
                          onClick={() => navigate(`/leads/${lead.id}`)}
                        >
                          <PersonIcon />
                        </IconButton>
                      </ListItemSecondaryAction>
                    </ListItem>
                    {index < leads.length - 1 && <Divider />}
                  </React.Fragment>
                ))}
              </List>
            )}
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Campaign Timeline
            </Typography>
            <Box sx={{ mt: 2 }}>
              <Typography color="text.secondary" gutterBottom>
                Start Date
              </Typography>
              <Typography>
                {format(new Date(campaign.startDate), 'MMM d, yyyy')}
              </Typography>
            </Box>
            {campaign.endDate && (
              <Box sx={{ mt: 2 }}>
                <Typography color="text.secondary" gutterBottom>
                  End Date
                </Typography>
                <Typography>
                  {format(new Date(campaign.endDate), 'MMM d, yyyy')}
                </Typography>
              </Box>
            )}
            <Box sx={{ mt: 2 }}>
              <Typography color="text.secondary" gutterBottom>
                Created
              </Typography>
              <Typography>
                {format(new Date(campaign.createdAt), 'MMM d, yyyy HH:mm')}
              </Typography>
            </Box>
            <Box sx={{ mt: 2 }}>
              <Typography color="text.secondary" gutterBottom>
                Last Updated
              </Typography>
              <Typography>
                {format(new Date(campaign.updatedAt), 'MMM d, yyyy HH:mm')}
              </Typography>
            </Box>
            {campaign.budget && (
              <Box sx={{ mt: 2 }}>
                <Typography color="text.secondary" gutterBottom>
                  Budget
                </Typography>
                <Typography>${campaign.budget.toLocaleString()}</Typography>
              </Box>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
} 