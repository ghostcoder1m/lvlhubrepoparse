import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { 
  AppBar, 
  Toolbar, 
  Typography, 
  Button, 
  IconButton,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Box,
  useTheme,
  useMediaQuery
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  Campaign as CampaignIcon,
  People as PeopleIcon,
  AccountTree as WorkflowIcon,
  Settings as SettingsIcon,
  Logout as LogoutIcon,
  AutoAwesome as AutomationIcon,
  Email as EmailIcon
} from '@mui/icons-material';
import { useAuth } from '../AuthContext';

const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { currentUser, loading } = useAuth();
  const [mobileOpen, setMobileOpen] = React.useState(false);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  const menuItems = [
    { text: 'Dashboard', icon: <DashboardIcon />, path: '/dashboard' },
    { text: 'Campaigns', icon: <CampaignIcon />, path: '/campaigns' },
    { text: 'Leads', icon: <PeopleIcon />, path: '/leads' },
    { text: 'Automation', icon: <AutomationIcon />, path: '/automation/rules' },
    { text: 'Email Templates', icon: <EmailIcon />, path: '/automation/templates' },
    { text: 'Workflows', icon: <WorkflowIcon />, path: '/workflows' },
    { text: 'Settings', icon: <SettingsIcon />, path: '/settings' }
  ];

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleNavigation = (path) => {
    navigate(path);
    if (isMobile) {
      handleDrawerToggle();
    }
  };

  const drawer = (
    <Box sx={{ width: 250 }}>
      <List>
        {menuItems.map((item) => (
          <ListItem 
            button 
            key={item.text}
            onClick={() => handleNavigation(item.path)}
            selected={location.pathname === item.path}
          >
            <ListItemIcon>{item.icon}</ListItemIcon>
            <ListItemText primary={item.text} />
          </ListItem>
        ))}
      </List>
    </Box>
  );

  if (loading) {
    return null;
  }

  return (
    <>
      <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
        <Toolbar>
          {currentUser && (
            <IconButton
              color="inherit"
              aria-label="open drawer"
              edge="start"
              onClick={handleDrawerToggle}
              sx={{ mr: 2, display: { sm: 'none' } }}
            >
              <MenuIcon />
            </IconButton>
          )}
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            STEPS Marketing
          </Typography>
          {currentUser ? (
            <Button 
              color="inherit"
              startIcon={<LogoutIcon />}
              onClick={() => {/* Add logout handler */}}
            >
              Logout
            </Button>
          ) : (
            <>
              <Button color="inherit" onClick={() => navigate('/login')}>Login</Button>
              <Button color="inherit" onClick={() => navigate('/register')}>Register</Button>
            </>
          )}
        </Toolbar>
      </AppBar>
      {currentUser && (
        <Box sx={{ display: 'flex' }}>
          <Box
            component="nav"
            sx={{ width: { sm: 250 }, flexShrink: { sm: 0 } }}
          >
            <Drawer
              variant={isMobile ? 'temporary' : 'permanent'}
              open={isMobile ? mobileOpen : true}
              onClose={handleDrawerToggle}
              ModalProps={{
                keepMounted: true // Better open performance on mobile.
              }}
              sx={{
                '& .MuiDrawer-paper': {
                  width: 250,
                  boxSizing: 'border-box',
                  marginTop: '64px'
                }
              }}
            >
              {drawer}
            </Drawer>
          </Box>
        </Box>
      )}
    </>
  );
};

export default Navbar;
