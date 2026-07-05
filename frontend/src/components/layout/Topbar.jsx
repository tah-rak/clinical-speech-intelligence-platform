import { Moon, Sun } from 'lucide-react';

export default function Topbar({ darkMode, onToggleDark }) {
  return (
    <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-slate-200 bg-white/80 px-8 backdrop-blur dark:border-slate-800 dark:bg-slate-900/80">
      <div />
      <button
        onClick={onToggleDark}
        className="rounded-lg p-2 text-slate-500 transition hover:bg-slate-100 hover:text-slate-700 dark:hover:bg-slate-800"
        aria-label="Toggle dark mode"
      >
        {darkMode ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
      </button>
    </header>
  );
}
