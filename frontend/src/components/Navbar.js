import React from 'react';
import { Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { useTranslation } from 'react-i18next';
import LanguageSwitcher from './LanguageSwitcher';

const Navbar = () => {
  const { t } = useTranslation();

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component={Link} to="/" sx={{ flexGrow: 1, textDecoration: 'none', color: 'inherit' }}>
          LvlHub
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Button color="inherit" component={Link} to="/dashboard">
            {t('navigation.dashboard')}
          </Button>
          <Button color="inherit" component={Link} to="/campaigns">
            {t('navigation.campaigns')}
          </Button>
          <Button color="inherit" component={Link} to="/leads">
            {t('navigation.leads')}
          </Button>
          <Button color="inherit" component={Link} to="/workflows">
            {t('navigation.workflows')}
          </Button>
          <Button color="inherit" component={Link} to="/settings">
            {t('navigation.settings')}
          </Button>
          <LanguageSwitcher />
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
