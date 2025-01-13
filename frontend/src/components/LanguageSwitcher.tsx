import React from 'react';
import { useTranslation } from 'react-i18next';
import { Select, MenuItem, FormControl } from '@mui/material';

const LanguageSwitcher: React.FC = () => {
  const { i18n } = useTranslation();

  const handleLanguageChange = (event: any) => {
    const language = event.target.value;
    i18n.changeLanguage(language);
  };

  return (
    <FormControl size="small">
      <Select
        value={i18n.language}
        onChange={handleLanguageChange}
        variant="outlined"
        sx={{ minWidth: 100 }}
      >
        <MenuItem value="en">English</MenuItem>
        <MenuItem value="es">Español</MenuItem>
      </Select>
    </FormControl>
  );
};

export default LanguageSwitcher; 