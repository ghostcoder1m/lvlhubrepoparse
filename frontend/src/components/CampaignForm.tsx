import React from 'react';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import {
  Box,
  Button,
  TextField,
  Grid,
  CircularProgress,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormHelperText,
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { Campaign, CreateCampaignDto, UpdateCampaignDto } from '../services/api';

const campaignSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  description: z.string().min(1, 'Description is required'),
  type: z.enum(['email', 'sms', 'social'], {
    required_error: 'Campaign type is required',
  }),
  targetAudience: z.string().min(1, 'Target audience is required'),
  startDate: z.string().min(1, 'Start date is required'),
  endDate: z.string().optional(),
  budget: z.number().min(0).optional(),
});

type CampaignFormData = z.infer<typeof campaignSchema>;

interface CampaignFormProps {
  campaign?: Campaign;
  onSubmit: (data: CreateCampaignDto | UpdateCampaignDto) => void;
  isLoading?: boolean;
}

export default function CampaignForm({
  campaign,
  onSubmit,
  isLoading,
}: CampaignFormProps) {
  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<CampaignFormData>({
    resolver: zodResolver(campaignSchema),
    defaultValues: {
      name: campaign?.name || '',
      description: campaign?.description || '',
      type: campaign?.type || 'email',
      targetAudience: campaign?.targetAudience || '',
      startDate: campaign?.startDate || '',
      endDate: campaign?.endDate || '',
      budget: campaign?.budget || 0,
    },
  });

  return (
    <Box
      component="form"
      onSubmit={handleSubmit(onSubmit)}
      noValidate
      sx={{ mt: 1 }}
    >
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <Controller
            name="name"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                required
                fullWidth
                label="Campaign Name"
                error={!!errors.name}
                helperText={errors.name?.message}
                disabled={isLoading}
              />
            )}
          />
        </Grid>
        <Grid item xs={12}>
          <Controller
            name="description"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                required
                fullWidth
                multiline
                rows={4}
                label="Description"
                error={!!errors.description}
                helperText={errors.description?.message}
                disabled={isLoading}
              />
            )}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <Controller
            name="type"
            control={control}
            render={({ field }) => (
              <FormControl
                fullWidth
                error={!!errors.type}
                disabled={isLoading}
              >
                <InputLabel>Campaign Type</InputLabel>
                <Select {...field} label="Campaign Type">
                  <MenuItem value="email">Email</MenuItem>
                  <MenuItem value="sms">SMS</MenuItem>
                  <MenuItem value="social">Social Media</MenuItem>
                </Select>
                {errors.type && (
                  <FormHelperText>{errors.type.message}</FormHelperText>
                )}
              </FormControl>
            )}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <Controller
            name="targetAudience"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                required
                fullWidth
                label="Target Audience"
                error={!!errors.targetAudience}
                helperText={errors.targetAudience?.message}
                disabled={isLoading}
              />
            )}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <Controller
            name="startDate"
            control={control}
            render={({ field }) => (
              <DatePicker
                label="Start Date"
                value={field.value ? new Date(field.value) : null}
                onChange={(date) => field.onChange(date?.toISOString())}
                disabled={isLoading}
                slotProps={{
                  textField: {
                    fullWidth: true,
                    error: !!errors.startDate,
                    helperText: errors.startDate?.message,
                  },
                }}
              />
            )}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <Controller
            name="endDate"
            control={control}
            render={({ field }) => (
              <DatePicker
                label="End Date (Optional)"
                value={field.value ? new Date(field.value) : null}
                onChange={(date) => field.onChange(date?.toISOString())}
                disabled={isLoading}
                slotProps={{
                  textField: {
                    fullWidth: true,
                    error: !!errors.endDate,
                    helperText: errors.endDate?.message,
                  },
                }}
              />
            )}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <Controller
            name="budget"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                type="number"
                fullWidth
                label="Budget (Optional)"
                error={!!errors.budget}
                helperText={errors.budget?.message}
                disabled={isLoading}
                InputProps={{
                  startAdornment: '$',
                }}
              />
            )}
          />
        </Grid>
      </Grid>
      <Box sx={{ mt: 3 }}>
        <Button
          type="submit"
          variant="contained"
          fullWidth
          disabled={isLoading}
          startIcon={isLoading && <CircularProgress size={20} />}
        >
          {campaign ? 'Update Campaign' : 'Create Campaign'}
        </Button>
      </Box>
    </Box>
  );
} 