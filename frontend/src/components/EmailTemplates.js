import React, { useState } from "react";
import {
  Box,
  Typography,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  IconButton,
  Grid,
  Card,
  CardContent,
  CardActions,
  Chip,
  Tooltip
} from "@mui/material";
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  FileCopy as DuplicateIcon,
  Visibility as PreviewIcon
} from "@mui/icons-material";

const EmailTemplates = () => {
  const [templates, setTemplates] = useState([
    {
      id: 1,
      name: "Welcome Email",
      subject: "Welcome to Our Platform!",
      content: "Hi {{firstName}},\n\nWelcome to our platform! We're excited to have you here...",
      variables: ["firstName", "companyName"],
    },
    {
      id: 2,
      name: "High Value Lead Follow-up",
      subject: "Let's Schedule a Call",
      content: "Hi {{firstName}},\n\nWe noticed your interest in {{productName}}...",
      variables: ["firstName", "productName", "companyName"],
    }
  ]);
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [previewMode, setPreviewMode] = useState(false);

  const handleSaveTemplate = () => {
    if (selectedTemplate) {
      if (selectedTemplate.id) {
        // Update existing template
        setTemplates(templates.map(template => 
          template.id === selectedTemplate.id ? selectedTemplate : template
        ));
      } else {
        // Create new template
        const newTemplate = {
          ...selectedTemplate,
          id: Math.max(...templates.map(t => t.id), 0) + 1,
        };
        setTemplates([...templates, newTemplate]);
      }
    }
    handleCloseDialog();
  };

  const handleOpenDialog = (template = null, preview = false) => {
    setSelectedTemplate(template || {
      name: "",
      subject: "",
      content: "",
      variables: []
    });
    setPreviewMode(preview);
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setSelectedTemplate(null);
    setPreviewMode(false);
    setOpenDialog(false);
  };

  const handleDuplicateTemplate = (template) => {
    const newTemplate = {
      ...template,
      id: Math.max(...templates.map(t => t.id)) + 1,
      name: `${template.name} (Copy)`,
    };
    setTemplates([...templates, newTemplate]);
  };

  const handleDeleteTemplate = (templateId) => {
    setTemplates(templates.filter(template => template.id !== templateId));
  };

  return (
    <Box sx={{ p: 3, mt: 8 }}>
      <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 3 }}>
        <Typography variant="h4">
          Email Templates
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
        >
          Create Template
        </Button>
      </Box>

      <Grid container spacing={3}>
        {templates.map(template => (
          <Grid item xs={12} md={6} key={template.id}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {template.name}
                </Typography>
                <Typography variant="body2" color="textSecondary" gutterBottom>
                  Subject: {template.subject}
                </Typography>
                <Box sx={{ mb: 2 }}>
                  {template.variables.map(variable => (
                    <Chip
                      key={variable}
                      label={variable}
                      size="small"
                      sx={{ mr: 0.5, mb: 0.5 }}
                    />
                  ))}
                </Box>
                <Typography
                  variant="body2"
                  sx={{
                    maxHeight: 100,
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                    display: "-webkit-box",
                    WebkitLineClamp: 4,
                    WebkitBoxOrient: "vertical",
                  }}
                >
                  {template.content}
                </Typography>
              </CardContent>
              <CardActions sx={{ justifyContent: "flex-end" }}>
                <Tooltip title="Preview">
                  <IconButton onClick={() => handleOpenDialog(template, true)}>
                    <PreviewIcon />
                  </IconButton>
                </Tooltip>
                <Tooltip title="Edit">
                  <IconButton onClick={() => handleOpenDialog(template)}>
                    <EditIcon />
                  </IconButton>
                </Tooltip>
                <Tooltip title="Duplicate">
                  <IconButton onClick={() => handleDuplicateTemplate(template)}>
                    <DuplicateIcon />
                  </IconButton>
                </Tooltip>
                <Tooltip title="Delete">
                  <IconButton onClick={() => handleDeleteTemplate(template.id)} color="error">
                    <DeleteIcon />
                  </IconButton>
                </Tooltip>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        <DialogTitle>
          {previewMode ? 'Preview Template' : (selectedTemplate ? 'Edit Template' : 'Create Template')}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 2, display: "flex", flexDirection: "column", gap: 2 }}>
            <TextField
              label="Template Name"
              value={selectedTemplate?.name || ""}
              onChange={(e) => setSelectedTemplate(prev => ({ ...prev, name: e.target.value }))}
              fullWidth
            />
            <TextField
              label="Subject Line"
              value={selectedTemplate?.subject || ""}
              onChange={(e) => setSelectedTemplate(prev => ({ ...prev, subject: e.target.value }))}
              fullWidth
            />
            <TextField
              label="Variables (comma-separated)"
              value={selectedTemplate?.variables.join(", ") || ""}
              onChange={(e) => setSelectedTemplate(prev => ({ ...prev, variables: e.target.value.split(",").map(v => v.trim()) }))}
              fullWidth
              helperText="Example: firstName, companyName"
            />
            <TextField
              label="Email Content"
              value={selectedTemplate?.content || ""}
              onChange={(e) => setSelectedTemplate(prev => ({ ...prev, content: e.target.value }))}
              multiline
              rows={8}
              fullWidth
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog} color="inherit">
            Cancel
          </Button>
          {!previewMode && (
            <Button onClick={handleSaveTemplate} color="primary" variant="contained">
              Save Template
            </Button>
          )}
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default EmailTemplates; 