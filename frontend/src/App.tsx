import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { I18nProvider } from './lib/i18n';
import Layout from './components/Layout';
import HomePage from './pages/HomePage';
import ResultsPage from './pages/ResultsPage';
import HistoryPage from './pages/HistoryPage';
import SettingsPage from './pages/SettingsPage';

export default function App() {
  return (
    <I18nProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<Layout />}>
            <Route path="/" element={<HomePage />} />
            <Route path="/research/:taskId" element={<ResultsPage />} />
            <Route path="/history" element={<HistoryPage />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </I18nProvider>
  );
}
