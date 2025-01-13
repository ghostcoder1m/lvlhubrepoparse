import React from 'react';
import {
  Box,
  Button,
  TextField,
  MenuItem,
  IconButton,
  Grid,
  Typography,
  Paper,
  Divider,
} from '@mui/material';
import { Add as AddIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { useForm, useFieldArray, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { AutomationRule } from '../services/automationService';

const triggerTypes = [
  { value: 'lead_created', label: 'Lead Created' },
  { value: 'lead_updated', label: 'Lead Updated' },
  { value: 'score_changed', label: 'Score Changed' },
  { value: 'event_occurred', label: 'Event Occurred' },
];

const operators = [
  { value: 'equals', label: 'Equals' },
  { value: 'contains', label: 'Contains' },
  { value: 'greater_than', label: 'Greater Than' },
  { value: 'less_than', label: 'Less Than' },
];

const actionTypes = [
  { value: 'send_email', label: 'Send Email' },
  { value: 'update_lead', label: 'Update Lead' },
  { value: 'add_to_campaign', label: 'Add to Campaign' },
  { value: 'notify_team', label: 'Notify Team' },
];

const schema = z.object({
  name: z.string().min(1, 'Name is required'),
  triggerType: z.enum(['lead_created', 'lead_updated', 'score_changed', 'event_occurred']),
  conditions: z.array(z.object({
    field: z.string().min(1, 'Field is required'),
    operator: z.enum(['equals', 'contains', 'greater_than', 'less_than']),
    value: z.union([z.string(), z.number()]).transform(val => String(val)),
  })).min(1, 'At least one condition is required'),
  actions: z.array(z.object({
    type: z.enum(['send_email', 'update_lead', 'add_to_campaign', 'notify_team']),
    params: z.record(z.any()),
  })).min(1, 'At least one action is required'),
  isActive: z.boolean(),
});

type FormData = z.infer<typeof schema>;

interface Props {
  rule?: AutomationRule;
  onSubmit: (data: FormData) => void;
  isLoading?: boolean;
}

export default function AutomationRuleForm({ rule, onSubmit, isLoading }: Props) {
  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: rule || {
      name: '',
      triggerType: 'lead_created',
      conditions: [{ field: '', operator: 'equals', value: '' }],
      actions: [{ type: 'send_email', params: {} }],
      isActive: true,
    },
  });

  const { fields: conditionFields, append: appendCondition, remove: removeCondition } =
    useFieldArray({
      control,
      name: 'conditions',
    });

  const { fields: actionFields, append: appendAction, remove: removeAction } =
    useFieldArray({
      control,
      name: 'actions',
    });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Controller
              name="name"
              control={control}
              render={({ field }) => (
                <TextField
                  {...field}
                  label="Rule Name"
                  fullWidth
                  error={!!errors.name}
                  helperText={errors.name?.message}
                />
              )}
            />
          </Grid>
          <Grid item xs={12}>
            <Controller
              name="triggerType"
              control={control}
              render={({ field }) => (
                <TextField
                  {...field}
                  select
                  label="Trigger Type"
                  fullWidth
                  error={!!errors.triggerType}
                  helperText={errors.triggerType?.message}
                >
                  {triggerTypes.map((option) => (
                    <MenuItem key={option.value} value={option.value}>
                      {option.label}
                    </MenuItem>
                  ))}
                </TextField>
              )}
            />
          </Grid>
        </Grid>
      </Paper>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
          <Typography variant="h6">Conditions</Typography>
          <Button
            startIcon={<AddIcon />}
            onClick={() => appendCondition({ field: '', operator: 'equals', value: '' })}
          >
            Add Condition
          </Button>
        </Box>
        <Divider sx={{ mb: 2 }} />
        {conditionFields.map((field, index) => (
          <Grid container spacing={2} key={field.id} sx={{ mb: 2 }}>
            <Grid item xs={4}>
              <Controller
                name={`conditions.${index}.field`}
                control={control}
                render={({ field }) => (
                  <TextField {...field} label="Field" fullWidth />
                )}
              />
            </Grid>
            <Grid item xs={3}>
              <Controller
                name={`conditions.${index}.operator`}
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    select
                    label="Operator"
                    fullWidth
                  >
                    {operators.map((option) => (
                      <MenuItem key={option.value} value={option.value}>
                        {option.label}
                      </MenuItem>
                    ))}
                  </TextField>
                )}
              />
            </Grid>
            <Grid item xs={4}>
              <Controller
                name={`conditions.${index}.value`}
                control={control}
                render={({ field }) => (
                  <TextField {...field} label="Value" fullWidth />
                )}
              />
            </Grid>
            <Grid item xs={1}>
              <IconButton
                onClick={() => removeCondition(index)}
                disabled={conditionFields.length === 1}
              >
                <DeleteIcon />
              </IconButton>
            </Grid>
          </Grid>
        ))}
      </Paper>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
          <Typography variant="h6">Actions</Typography>
          <Button
            startIcon={<AddIcon />}
            onClick={() => appendAction({ type: 'send_email', params: {} })}
          >
            Add Action
          </Button>
        </Box>
        <Divider sx={{ mb: 2 }} />
        {actionFields.map((field, index) => (
          <Grid container spacing={2} key={field.id} sx={{ mb: 2 }}>
            <Grid item xs={11}>
              <Controller
                name={`actions.${index}.type`}
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    select
                    label="Action Type"
                    fullWidth
                  >
                    {actionTypes.map((option) => (
                      <MenuItem key={option.value} value={option.value}>
                        {option.label}
                      </MenuItem>
                    ))}
                  </TextField>
                )}
              />
            </Grid>
            <Grid item xs={1}>
              <IconButton
                onClick={() => removeAction(index)}
                disabled={actionFields.length === 1}
              >
                <DeleteIcon />
              </IconButton>
            </Grid>
          </Grid>
        ))}
      </Paper>

      <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
        <Button
          type="submit"
          variant="contained"
          disabled={isLoading}
        >
          {rule ? 'Update Rule' : 'Create Rule'}
        </Button>
      </Box>
    </form>
  );
} 