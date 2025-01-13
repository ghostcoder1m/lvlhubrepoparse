import React, { useState } from 'react';
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
  GridRenderCellParams,
  GridToolbar,
} from '@mui/x-data-grid';
import {
  Add as AddIcon,
  Psychology as AIIcon,
  Visibility as ViewIcon,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { format } from 'date-fns';
import { leadApi, Lead } from '../services/api';

export default function Leads() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [selectedLeads, setSelectedLeads] = useState<number[]>([]);

  // Fetch leads
  const { data: leads = [], isLoading } = useQuery({
    queryKey: ['leads'],
    queryFn: async () => {
      const response = await leadApi.getLeads();
      return response.data;
    },
  });

  // Score lead mutation
  const scoreMutation = useMutation({
    mutationFn: (leadId: number) => leadApi.scoreLead(leadId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['leads'] });
    },
  });

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'firstName', headerName: 'First Name', width: 130 },
    { field: 'lastName', headerName: 'Last Name', width: 130 },
    { field: 'email', headerName: 'Email', width: 200 },
    { field: 'company', headerName: 'Company', width: 150 },
    {
      field: 'leadScore',
      headerName: 'Lead Score',
      width: 130,
      renderCell: (params: GridRenderCellParams<Lead>) => {
        const score = params.row.leadScore;
        let color: 'success' | 'warning' | 'error' = 'error';
        if (score >= 0.7) color = 'success';
        else if (score >= 0.4) color = 'warning';

        return (
          <Chip
            label={`${Math.round(score * 100)}%`}
            color={color}
            size="small"
          />
        );
      },
    },
    {
      field: 'createdAt',
      headerName: 'Created',
      width: 150,
      valueFormatter: (params) =>
        format(new Date(params.value), 'MMM d, yyyy'),
    },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 120,
      sortable: false,
      renderCell: (params: GridRenderCellParams<Lead>) => (
        <Box>
          <Tooltip title="View Details">
            <IconButton
              size="small"
              onClick={() => navigate(`/leads/${params.row.id}`)}
            >
              <ViewIcon />
            </IconButton>
          </Tooltip>
          <Tooltip title="AI Score">
            <IconButton
              size="small"
              onClick={() => scoreMutation.mutate(params.row.id)}
              disabled={scoreMutation.isPending}
            >
              <AIIcon />
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
          Leads
        </Typography>
        <Box>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => navigate('/leads/new')}
          >
            Add Lead
          </Button>
        </Box>
      </Box>

      <Paper sx={{ height: 'calc(100vh - 200px)', width: '100%' }}>
        <DataGrid
          rows={leads}
          columns={columns}
          loading={isLoading}
          checkboxSelection
          disableRowSelectionOnClick
          onRowSelectionModelChange={(newSelection) => {
            setSelectedLeads(newSelection as number[]);
          }}
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
              sortModel: [{ field: 'leadScore', sort: 'desc' }],
            },
          }}
        />
      </Paper>
    </Box>
  );
} 