import axios from 'axios';
import { useAuthStore } from '../store/authStore';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface Lead {
  id: number;
  firstName: string;
  lastName: string;
  email: string;
  phone?: string;
  company?: string;
  jobTitle?: string;
  leadScore: number;
  createdAt: string;
  updatedAt: string;
}

export interface Campaign {
  id: number;
  name: string;
  description: string;
  status: 'draft' | 'active' | 'paused' | 'completed';
  type: 'email' | 'sms' | 'social';
  targetAudience: string;
  startDate: string;
  endDate?: string;
  budget?: number;
  metrics: {
    sent: number;
    delivered: number;
    opened: number;
    clicked: number;
    converted: number;
  };
  createdAt: string;
  updatedAt: string;
}

export interface CreateCampaignDto {
  name: string;
  description: string;
  type: 'email' | 'sms' | 'social';
  targetAudience: string;
  startDate: string;
  endDate?: string;
  budget?: number;
}

export interface UpdateCampaignDto extends Partial<CreateCampaignDto> {
  status?: 'draft' | 'active' | 'paused' | 'completed';
}

export interface CreateLeadDto {
  firstName: string;
  lastName: string;
  email: string;
  phone?: string;
  company?: string;
  jobTitle?: string;
}

export interface UpdateLeadDto extends Partial<CreateLeadDto> {
  leadScore?: number;
}

export interface AutomationRule {
  id: number;
  name: string;
  triggerType: 'lead_created' | 'lead_updated' | 'score_changed' | 'event_occurred';
  conditions: {
    field: string;
    operator: 'equals' | 'not_equals' | 'greater_than' | 'less_than' | 'contains';
    value: string;
  }[];
  actions: {
    type: 'send_email' | 'update_lead' | 'add_to_campaign' | 'notify_team';
    config: Record<string, any>;
  }[];
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface EmailTemplate {
  id: number;
  name: string;
  subject: string;
  content: string;
  variables: string[];
  createdAt: string;
  updatedAt: string;
}

export interface CreateAutomationRuleDto {
  name: string;
  triggerType: AutomationRule['triggerType'];
  conditions: AutomationRule['conditions'];
  actions: AutomationRule['actions'];
  isActive?: boolean;
}

export interface CreateEmailTemplateDto {
  name: string;
  subject: string;
  content: string;
  variables: string[];
}

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout();
    }
    return Promise.reject(error);
  }
);

export const leadApi = {
  getLeads: () => api.get<Lead[]>('/leads'),
  getLead: (id: number) => api.get<Lead>(`/leads/${id}`),
  createLead: (data: CreateLeadDto) => api.post<Lead>('/leads', data),
  updateLead: (id: number, data: UpdateLeadDto) =>
    api.patch<Lead>(`/leads/${id}`, data),
  deleteLead: (id: number) => api.delete(`/leads/${id}`),
  scoreLead: (id: number) => api.post<Lead>(`/leads/${id}/score`),
  getLeadEvents: (id: number) => api.get(`/leads/${id}/events`),
};

export const campaignApi = {
  getCampaigns: () => api.get<Campaign[]>('/campaigns'),
  getCampaign: (id: number) => api.get<Campaign>(`/campaigns/${id}`),
  createCampaign: (data: CreateCampaignDto) => api.post<Campaign>('/campaigns', data),
  updateCampaign: (id: number, data: UpdateCampaignDto) =>
    api.patch<Campaign>(`/campaigns/${id}`, data),
  deleteCampaign: (id: number) => api.delete(`/campaigns/${id}`),
  launchCampaign: (id: number) => api.post(`/campaigns/${id}/launch`),
  pauseCampaign: (id: number) => api.post(`/campaigns/${id}/pause`),
  resumeCampaign: (id: number) => api.post(`/campaigns/${id}/resume`),
  getCampaignMetrics: (id: number) => api.get(`/campaigns/${id}/metrics`),
  getCampaignLeads: (id: number) => api.get<Lead[]>(`/campaigns/${id}/leads`),
  addLeadsToCampaign: (id: number, leadIds: number[]) =>
    api.post(`/campaigns/${id}/leads`, { leadIds }),
  removeLeadsFromCampaign: (id: number, leadIds: number[]) =>
    api.delete(`/campaigns/${id}/leads`, { data: { leadIds } }),
};

export const authApi = {
  login: (email: string, password: string) => 
    api.post<{ token: string }>('/auth/login', { email, password }),
  register: (data: { email: string; password: string; firstName: string; lastName: string }) =>
    api.post('/auth/register', data),
  getProfile: () => api.get('/auth/profile'),
};

export const automationApi = {
  // Automation Rules
  getRules: () => api.get<AutomationRule[]>('/automation/rules'),
  getRule: (id: number) => api.get<AutomationRule>(`/automation/rules/${id}`),
  createRule: (data: CreateAutomationRuleDto) => 
    api.post<AutomationRule>('/automation/rules', data),
  updateRule: (id: number, data: Partial<CreateAutomationRuleDto>) =>
    api.patch<AutomationRule>(`/automation/rules/${id}`, data),
  deleteRule: (id: number) => api.delete(`/automation/rules/${id}`),
  toggleRule: (id: number, isActive: boolean) =>
    api.patch<AutomationRule>(`/automation/rules/${id}/toggle`, { isActive }),

  // Email Templates
  getTemplates: () => api.get<EmailTemplate[]>('/automation/templates'),
  getTemplate: (id: number) => api.get<EmailTemplate>(`/automation/templates/${id}`),
  createTemplate: (data: CreateEmailTemplateDto) =>
    api.post<EmailTemplate>('/automation/templates', data),
  updateTemplate: (id: number, data: Partial<CreateEmailTemplateDto>) =>
    api.patch<EmailTemplate>(`/automation/templates/${id}`, data),
  deleteTemplate: (id: number) => api.delete(`/automation/templates/${id}`),
  duplicateTemplate: (id: number) =>
    api.post<EmailTemplate>(`/automation/templates/${id}/duplicate`),
};

export default api; 