import { useState, useEffect } from 'react';
import { Routes, Route } from 'react-router-dom';
import Sidebar from './components/layout/Sidebar';
import Topbar from './components/layout/Topbar';
import Dashboard from './pages/Dashboard';
import UploadVisit from './pages/UploadVisit';
import Visits from './pages/Visits';
import VisitDetailPage from './pages/VisitDetailPage';
import Evaluation from './pages/Evaluation';
import Settings from './pages/Settings';

export default function App() {
  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem('darkMode') === 'true';
  });

  useEffect(() => {
    document.documentElement.classList.toggle('dark', darkMode);
    localStorage.setItem('darkMode', darkMode);
  }, [darkMode]);

  return (
    <div className="min-h-screen">
      <Sidebar />
      <div className="ml-64">
        <Topbar darkMode={darkMode} onToggleDark={() => setDarkMode(!darkMode)} />
        <main className="p-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/upload" element={<UploadVisit />} />
            <Route path="/visits" element={<Visits />} />
            <Route path="/visits/:id" element={<VisitDetailPage />} />
            <Route path="/evaluation" element={<Evaluation />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </main>
        <footer className="border-t border-slate-200 px-8 py-4 text-center text-xs text-slate-500 dark:border-slate-800">
          This application is a research and portfolio prototype. It is not a medical device and must not be used for diagnosis or treatment decisions. All generated notes require clinician review.
        </footer>
      </div>
    </div>
  );
}
