import clsx from 'clsx';

export default function Tabs({ tabs, active, onChange }) {
  return (
    <div className="border-b border-slate-200 dark:border-slate-800">
      <nav className="-mb-px flex gap-6 overflow-x-auto">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => onChange(tab.id)}
            className={clsx(
              'whitespace-nowrap border-b-2 pb-3 text-sm font-medium transition',
              active === tab.id
                ? 'border-medical-600 text-medical-600'
                : 'border-transparent text-slate-500 hover:border-slate-300 hover:text-slate-700 dark:text-slate-400'
            )}
          >
            {tab.label}
          </button>
        ))}
      </nav>
    </div>
  );
}
