import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Typography,
  Paper,
  Chip,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  DataGrid,
  GridColDef,
  GridValueFormatter,
  GridRenderCellParams,
  GridToolbar,
} from '@mui/x-data-grid';
import {
  Add as AddIcon,
  Edit as EditIcon,
  PlayArrow as PlayIcon,
  Pause as PauseIcon,
  Delete as DeleteIcon,
  Assessment as MetricsIcon,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { format } from 'date-fns';
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

export default function Campaigns() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: campaigns = [], isLoading } = useQuery({
    queryKey: ['campaigns'],
    queryFn: async () => {
      const response = await campaignApi.getCampaigns();
      return response.data;
    },
  });

  const deleteMutation = useMutation({
    mutationFn: campaignApi.deleteCampaign,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['campaigns'] });
    },
  });

  const statusMutation = useMutation({
    mutationFn: async ({ id, action }: { id: number; action: 'launch' | 'pause' | 'resume' }) => {
      switch (action) {
        case 'launch':
          return campaignApi.launchCampaign(id);
        case 'pause':
          return campaignApi.pauseCampaign(id);
        case 'resume':
          return campaignApi.resumeCampaign(id);
      }
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['campaigns'] });
    },
  });

  const handleStatusChange = (id: number, currentStatus: Campaign['status']) => {
    if (currentStatus === 'draft') {
      statusMutation.mutate({ id, action: 'launch' });
    } else if (currentStatus === 'active') {
      statusMutation.mutate({ id, action: 'pause' });
    } else if (currentStatus === 'paused') {
      statusMutation.mutate({ id, action: 'resume' });
    }
  };

  const columns: GridColDef<Campaign>[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'name', headerName: 'Name', width: 200 },
    { field: 'type', headerName: 'Type', width: 120 },
    {
      field: 'status',
      headerName: 'Status',
      width: 120,
      renderCell: (params: GridRenderCellParams<Campaign>) => (
        <Chip
          label={params.value?.toUpperCase()}
          color={getStatusColor(params.value as Campaign['status'])}
          size="small"
        />
      ),
    },
    {
      field: 'metrics',
      headerName: 'Conversion',
      width: 120,
      valueGetter: (params) => {
        const metrics = params.row.metrics;
        if (metrics.sent === 0) return '0%';
        return `${Math.round((metrics.converted / metrics.sent) * 100)}%`;
      },
    },
    {
      field: 'startDate',
      headerName: 'Start Date',
      width: 120,
      valueFormatter: (params: { value: string }) =>
        format(new Date(params.value), 'MMM d, yyyy'),
    },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 200,
      sortable: false,
      renderCell: (params: GridRenderCellParams<Campaign>) => (
        <Box>
          <Tooltip title="Edit">
            <IconButton
              size="small"
              onClick={() => navigate(`/campaigns/${params.row.id}/edit`)}
            >
              <EditIcon />
            </IconButton>
          </Tooltip>
          <Tooltip title="View Metrics">
            <IconButton
              size="small"
              onClick={() => navigate(`/campaigns/${params.row.id}`)}
            >
              <MetricsIcon />
            </IconButton>
          </Tooltip>
          {params.row.status !== 'completed' && (
            <Tooltip
              title={
                params.row.status === 'active'
                  ? 'Pause'
                  : params.row.status === 'paused'
                  ? 'Resume'
                  : 'Launch'
              }
            >
              <IconButton
                size="small"
                onClick={() => handleStatusChange(params.row.id, params.row.status)}
                disabled={statusMutation.isPending}
              >
                {params.row.status === 'active' ? (
                  <PauseIcon />
                ) : (
                  <PlayIcon />
                )}
              </IconButton>
            </Tooltip>
          )}
          <Tooltip title="Delete">
            <IconButton
              size="small"
              onClick={() => {
                if (window.confirm('Are you sure you want to delete this campaign?')) {
                  deleteMutation.mutate(params.row.id);
                }
              }}
              disabled={deleteMutation.isPending}
            >
              <DeleteIcon />
            </IconButton>
          </Tooltip>
        </Box>
      ),
    },
  ];

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
          Campaigns
        </Typography>
        <Box>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => navigate('/campaigns/new')}
          >
            Create Campaign
          </Button>
        </Box>
      </Box>

      <Paper sx={{ height: 'calc(100vh - 200px)', width: '100%' }}>
        <DataGrid
          rows={campaigns}
          columns={columns}
          loading={isLoading}
          disableRowSelectionOnClick
          slots={{ toolbar: GridToolbar }}
          slotProps={{
            toolbar: {
              showQuickFilter: true,
            },
          }}
          initialState={{
            pagination: {
              paginationModel: { pageSize: 25, page: 0 },
            },
            sorting: {
              sortModel: [{ field: 'startDate', sort: 'desc' }],
            },
          }}
        />
      </Paper>
    </Box>
  );
} 