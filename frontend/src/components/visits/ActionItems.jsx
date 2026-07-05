import { CheckCircle2, Circle, FlaskConical, Calendar, Pill, Eye } from 'lucide-react';
import Card from '../ui/Card';

const categoryIcons = {
  lab_work: FlaskConical,
  follow_up: Calendar,
  medication: Pill,
  monitor: Eye,
  default: Circle,
};

export default function ActionItems({ items, summary }) {
  return (
    <div className="space-y-6">
      {summary && (
        <Card>
          <h4 className="mb-2 font-semibold text-slate-900 dark:text-white">Visit Summary</h4>
          <p className="text-sm leading-relaxed text-slate-600 dark:text-slate-400">{summary}</p>
        </Card>
      )}

      <Card>
        <h4 className="mb-4 font-semibold text-slate-900 dark:text-white">Action Items</h4>
        {!items?.length ? (
          <p className="text-sm text-slate-500">No action items generated.</p>
        ) : (
          <ul className="space-y-3">
            {items.map((item) => {
              const Icon = categoryIcons[item.category] || categoryIcons.default;
              return (
                <li
                  key={item.id}
                  className="flex items-start gap-3 rounded-lg border border-slate-200 p-3 dark:border-slate-700"
                >
                  <Icon className="mt-0.5 h-5 w-5 shrink-0 text-medical-600" />
                  <div className="flex-1">
                    <p className="text-sm text-slate-700 dark:text-slate-300">{item.text}</p>
                    <span className="mt-1 inline-block text-xs capitalize text-slate-400">
                      {item.category?.replace('_', ' ')}
                    </span>
                  </div>
                  {item.completed ? (
                    <CheckCircle2 className="h-5 w-5 text-emerald-500" />
                  ) : (
                    <Circle className="h-5 w-5 text-slate-300" />
                  )}
                </li>
              );
            })}
          </ul>
        )}
      </Card>
    </div>
  );
}
