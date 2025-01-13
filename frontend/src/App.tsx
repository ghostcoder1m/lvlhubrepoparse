import React, { Suspense } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { CircularProgress } from '@mui/material';
import Layout from './components/Layout';

// Lazy load components
const Login = React.lazy(() => import('./pages/Login'));
const Leads = React.lazy(() => import('./pages/Leads'));
const LeadDetail = React.lazy(() => import('./pages/LeadDetail'));
const CreateLead = React.lazy(() => import('./pages/CreateLead'));
const EditLead = React.lazy(() => import('./pages/EditLead'));
const Campaigns = React.lazy(() => import('./pages/Campaigns'));
const CampaignDetail = React.lazy(() => import('./pages/CampaignDetail'));
const CreateCampaign = React.lazy(() => import('./pages/CreateCampaign'));
const EditCampaign = React.lazy(() => import('./pages/EditCampaign'));
const CampaignLeads = React.lazy(() => import('./pages/CampaignLeads'));
const AutomationRules = React.lazy(() => import('./pages/AutomationRules'));
const EmailTemplates = React.lazy(() => import('./pages/EmailTemplates'));

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Suspense fallback={<CircularProgress />}>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/" element={<Layout />}>
              <Route index element={<Navigate to="/leads" replace />} />
              
              {/* Lead Routes */}
              <Route path="leads" element={<Leads />} />
              <Route path="leads/new" element={<CreateLead />} />
              <Route path="leads/:id" element={<LeadDetail />} />
              <Route path="leads/:id/edit" element={<EditLead />} />
              
              {/* Campaign Routes */}
              <Route path="campaigns" element={<Campaigns />} />
              <Route path="campaigns/new" element={<CreateCampaign />} />
              <Route path="campaigns/:id" element={<CampaignDetail />} />
              <Route path="campaigns/:id/edit" element={<EditCampaign />} />
              <Route path="campaigns/:id/leads" element={<CampaignLeads />} />
              
              {/* Automation Routes */}
              <Route path="automation/rules" element={<AutomationRules />} />
              <Route path="automation/templates" element={<EmailTemplates />} />
            </Route>
          </Routes>
        </Suspense>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App; 