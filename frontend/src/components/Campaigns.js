import React, { useState } from 'react';
import {
  Container,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  Box,
  Chip,
  IconButton,
  Tooltip
} from '@mui/material';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  PlayArrow as PlayArrowIcon,
  Pause as PauseIcon
} from '@mui/icons-material';

// Sample data - replace with actual API calls
const sampleCampaigns = [
  {
    id: 1,
    name: 'Summer Sale 2024',
    status: 'active',
    type: 'email',
    leads: 1250,
    conversions: 125,
    conversionRate: '10%'
  },
  {
    id: 2,
    name: 'New Product Launch',
    status: 'draft',
    type: 'social',
    leads: 0,
    conversions: 0,
    conversionRate: '0%'
  },
  {
    id: 3,
    name: 'Customer Reactivation',
    status: 'paused',
    type: 'email',
    leads: 850,
    conversions: 68,
    conversionRate: '8%'
  }
];

const Campaigns = () => {
  const [campaigns] = useState(sampleCampaigns);

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'success';
      case 'draft':
        return 'default';
      case 'paused':
        return 'warning';
      default:
        return 'default';
    }
  };

  const handleEdit = (id) => {
    // TODO: Implement edit functionality
    console.log('Edit campaign:', id);
  };

  const handleDelete = (id) => {
    // TODO: Implement delete functionality
    console.log('Delete campaign:', id);
  };

  const handleToggleStatus = (id) => {
    // TODO: Implement status toggle functionality
    console.log('Toggle status:', id);
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" gutterBottom>
          Campaigns
        </Typography>
        <Button variant="contained" color="primary">
          Create Campaign
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Type</TableCell>
              <TableCell align="right">Leads</TableCell>
              <TableCell align="right">Conversions</TableCell>
              <TableCell align="right">Rate</TableCell>
              <TableCell align="center">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {campaigns.map((campaign) => (
              <TableRow key={campaign.id}>
                <TableCell>{campaign.name}</TableCell>
                <TableCell>
                  <Chip
                    label={campaign.status}
                    color={getStatusColor(campaign.status)}
                    size="small"
                  />
                </TableCell>
                <TableCell>{campaign.type}</TableCell>
                <TableCell align="right">{campaign.leads}</TableCell>
                <TableCell align="right">{campaign.conversions}</TableCell>
                <TableCell align="right">{campaign.conversionRate}</TableCell>
                <TableCell align="center">
                  <Tooltip title={campaign.status === 'active' ? 'Pause' : 'Activate'}>
                    <IconButton
                      size="small"
                      onClick={() => handleToggleStatus(campaign.id)}
                    >
                      {campaign.status === 'active' ? (
                        <PauseIcon fontSize="small" />
                      ) : (
                        <PlayArrowIcon fontSize="small" />
                      )}
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Edit">
                    <IconButton
                      size="small"
                      onClick={() => handleEdit(campaign.id)}
                    >
                      <EditIcon fontSize="small" />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Delete">
                    <IconButton
                      size="small"
                      onClick={() => handleDelete(campaign.id)}
                    >
                      <DeleteIcon fontSize="small" />
                    </IconButton>
                  </Tooltip>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  );
};

export default Campaigns;
