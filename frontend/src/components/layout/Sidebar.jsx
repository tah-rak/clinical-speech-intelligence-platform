import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Upload,
  FileText,
  BarChart3,
  Settings,
  Stethoscope,
} from 'lucide-react';
import clsx from 'clsx';

const navItems = [
  { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/upload', icon: Upload, label: 'Upload Visit' },
  { to: '/visits', icon: FileText, label: 'Visits' },
  { to: '/evaluation', icon: BarChart3, label: 'Evaluation' },
  { to: '/settings', icon: Settings, label: 'Settings' },
];

export default function Sidebar() {
  return (
    <aside className="fixed left-0 top-0 z-40 flex h-screen w-64 flex-col border-r border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900">
      <div className="flex items-center gap-3 border-b border-slate-200 px-6 py-5 dark:border-slate-800">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-medical-600 text-white">
          <Stethoscope className="h-5 w-5" />
        </div>
        <div>
          <h1 className="text-sm font-bold text-slate-900 dark:text-white">CSIP</h1>
          <p className="text-xs text-slate-500">Clinical Speech AI</p>
        </div>
      </div>
      <nav className="flex-1 space-y-1 p-4">
        {navItems.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            className={({ isActive }) =>
              clsx(
                'flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition',
                isActive
                  ? 'bg-medical-50 text-medical-700 dark:bg-medical-900/20 dark:text-medical-300'
                  : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900 dark:text-slate-400 dark:hover:bg-slate-800'
              )
            }
          >
            <Icon className="h-5 w-5" />
            {label}
          </NavLink>
        ))}
      </nav>
      <div className="border-t border-slate-200 p-4 dark:border-slate-800">
        <p className="text-xs leading-relaxed text-slate-500">
          Research prototype. Not for clinical diagnosis. All notes require clinician review.
        </p>
      </div>
    </aside>
  );
}
