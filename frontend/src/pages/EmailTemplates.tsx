import React from 'react';
import {
  Box,
  Button,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  CardActions,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Chip,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  ContentCopy as DuplicateIcon,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { automationApi, type EmailTemplate } from '../services/api';

export default function EmailTemplates() {
  const queryClient = useQueryClient();
  const [openDialog, setOpenDialog] = React.useState(false);
  const [selectedTemplate, setSelectedTemplate] = React.useState<EmailTemplate | null>(null);

  const { data: templates = [], isLoading } = useQuery({
    queryKey: ['email-templates'],
    queryFn: async () => {
      const response = await automationApi.getTemplates();
      return response.data;
    },
  });

  const createMutation = useMutation({
    mutationFn: automationApi.createTemplate,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['email-templates'] });
      setOpenDialog(false);
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, template }: { id: number; template: Partial<EmailTemplate> }) =>
      automationApi.updateTemplate(id, template),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['email-templates'] });
      setOpenDialog(false);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: automationApi.deleteTemplate,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['email-templates'] });
    },
  });

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const templateData = {
      name: formData.get('name') as string,
      subject: formData.get('subject') as string,
      content: formData.get('content') as string,
      variables: (formData.get('variables') as string).split(',').map(v => v.trim()),
    };

    if (selectedTemplate) {
      updateMutation.mutate({
        id: selectedTemplate.id,
        template: templateData,
      });
    } else {
      createMutation.mutate(templateData);
    }
  };

  const handleDelete = (id: number) => {
    if (window.confirm('Are you sure you want to delete this template?')) {
      deleteMutation.mutate(id);
    }
  };

  const handleDuplicate = (template: EmailTemplate) => {
    const { id, ...templateData } = template;
    createMutation.mutate({
      ...templateData,
      name: `${template.name} (Copy)`,
    });
  };

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
          Email Templates
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => {
            setSelectedTemplate(null);
            setOpenDialog(true);
          }}
        >
          Create Template
        </Button>
      </Box>

      {isLoading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 2 }}>
          Loading...
        </Box>
      ) : (
        <Grid container spacing={3}>
          {templates.map((template) => (
            <Grid item xs={12} md={6} lg={4} key={template.id}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    {template.name}
                  </Typography>
                  <Typography color="text.secondary" gutterBottom>
                    Subject: {template.subject}
                  </Typography>
                  <Box sx={{ mt: 2 }}>
                    {template.variables.map((variable) => (
                      <Chip
                        key={variable}
                        label={variable}
                        size="small"
                        sx={{ mr: 1, mb: 1 }}
                      />
                    ))}
                  </Box>
                </CardContent>
                <CardActions>
                  <IconButton
                    onClick={() => {
                      setSelectedTemplate(template);
                      setOpenDialog(true);
                    }}
                  >
                    <EditIcon />
                  </IconButton>
                  <IconButton onClick={() => handleDuplicate(template)}>
                    <DuplicateIcon />
                  </IconButton>
                  <IconButton
                    onClick={() => handleDelete(template.id)}
                    disabled={deleteMutation.isPending}
                  >
                    <DeleteIcon />
                  </IconButton>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      <Dialog
        open={openDialog}
        onClose={() => setOpenDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <form onSubmit={handleSubmit}>
          <DialogTitle>
            {selectedTemplate ? 'Edit Template' : 'Create Template'}
          </DialogTitle>
          <DialogContent>
            <Grid container spacing={3} sx={{ mt: 1 }}>
              <Grid item xs={12}>
                <TextField
                  name="name"
                  label="Template Name"
                  defaultValue={selectedTemplate?.name}
                  fullWidth
                  required
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  name="subject"
                  label="Email Subject"
                  defaultValue={selectedTemplate?.subject}
                  fullWidth
                  required
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  name="content"
                  label="Email Content"
                  defaultValue={selectedTemplate?.content}
                  multiline
                  rows={8}
                  fullWidth
                  required
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  name="variables"
                  label="Variables (comma-separated)"
                  defaultValue={selectedTemplate?.variables.join(', ')}
                  fullWidth
                  helperText="Example: firstName, lastName, companyName"
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
            <Button
              type="submit"
              variant="contained"
              disabled={createMutation.isPending || updateMutation.isPending}
            >
              {selectedTemplate ? 'Update' : 'Create'}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Box>
  );
} 