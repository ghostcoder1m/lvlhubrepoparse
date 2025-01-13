import axios from 'axios';
import { Campaign } from './api';

export interface AutomationRule {
  id: number;
  name: string;
  triggerType: 'lead_created' | 'lead_updated' | 'score_changed' | 'event_occurred';
  conditions: {
    field: string;
    operator: 'equals' | 'contains' | 'greater_than' | 'less_than';
    value: string | number;
  }[];
  actions: {
    type: 'send_email' | 'update_lead' | 'add_to_campaign' | 'notify_team';
    params: Record<string, any>;
  }[];
  isActive: boolean;
}

export interface EmailTemplate {
  id: number;
  name: string;
  subject: string;
  content: string;
  variables: string[];
}

export const automationApi = {
  // Automation Rules
  getRules: () => axios.get<AutomationRule[]>('/api/automation/rules'),
  getRule: (id: number) => axios.get<AutomationRule>(`/api/automation/rules/${id}`),
  createRule: (rule: Omit<AutomationRule, 'id'>) => 
    axios.post<AutomationRule>('/api/automation/rules', rule),
  updateRule: (id: number, rule: Partial<AutomationRule>) =>
    axios.patch<AutomationRule>(`/api/automation/rules/${id}`, rule),
  deleteRule: (id: number) => axios.delete(`/api/automation/rules/${id}`),
  toggleRule: (id: number, isActive: boolean) =>
    axios.patch(`/api/automation/rules/${id}/toggle`, { isActive }),

  // Email Templates
  getTemplates: () => axios.get<EmailTemplate[]>('/api/automation/templates'),
  getTemplate: (id: number) => axios.get<EmailTemplate>(`/api/automation/templates/${id}`),
  createTemplate: (template: Omit<EmailTemplate, 'id'>) =>
    axios.post<EmailTemplate>('/api/automation/templates', template),
  updateTemplate: (id: number, template: Partial<EmailTemplate>) =>
    axios.patch<EmailTemplate>(`/api/automation/templates/${id}`, template),
  deleteTemplate: (id: number) => axios.delete(`/api/automation/templates/${id}`),

  // Campaign Automation
  scheduleEmails: (campaignId: number, templateId: number, schedule: {
    startDate: string;
    frequency: 'once' | 'daily' | 'weekly';
    endDate?: string;
  }) => axios.post(`/api/campaigns/${campaignId}/schedule`, { templateId, schedule }),
  
  pauseAutomation: (campaignId: number) =>
    axios.post(`/api/campaigns/${campaignId}/pause-automation`),
  
  resumeAutomation: (campaignId: number) =>
    axios.post(`/api/campaigns/${campaignId}/resume-automation`),

  // Analytics
  getAutomationStats: (campaignId: number) =>
    axios.get(`/api/campaigns/${campaignId}/automation-stats`),
}; 