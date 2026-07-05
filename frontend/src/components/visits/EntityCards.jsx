import Card from '../ui/Card';
import Badge from '../ui/Badge';

const entityConfig = [
  { key: 'symptoms', label: 'Symptoms', color: 'bg-red-50 border-red-200 dark:bg-red-900/10 dark:border-red-800' },
  { key: 'medications', label: 'Medications', color: 'bg-blue-50 border-blue-200 dark:bg-blue-900/10 dark:border-blue-800' },
  { key: 'allergies', label: 'Allergies', color: 'bg-orange-50 border-orange-200 dark:bg-orange-900/10 dark:border-orange-800' },
  { key: 'conditions', label: 'Conditions', color: 'bg-purple-50 border-purple-200 dark:bg-purple-900/10 dark:border-purple-800' },
  { key: 'duration', label: 'Duration', color: 'bg-slate-50 border-slate-200 dark:bg-slate-800 dark:border-slate-700' },
  { key: 'tests_labs', label: 'Tests & Labs', color: 'bg-cyan-50 border-cyan-200 dark:bg-cyan-900/10 dark:border-cyan-800' },
  { key: 'diagnosis', label: 'Diagnosis', color: 'bg-amber-50 border-amber-200 dark:bg-amber-900/10 dark:border-amber-800' },
  { key: 'treatment_plan', label: 'Treatment Plan', color: 'bg-emerald-50 border-emerald-200 dark:bg-emerald-900/10 dark:border-emerald-800' },
  { key: 'follow_up', label: 'Follow-up', color: 'bg-teal-50 border-teal-200 dark:bg-teal-900/10 dark:border-teal-800' },
];

export default function EntityCards({ entities }) {
  if (!entities) {
    return (
      <div className="rounded-xl border border-dashed border-slate-300 p-12 text-center text-slate-500">
        No entities extracted yet.
      </div>
    );
  }

  const hasAny = entityConfig.some(({ key }) => entities[key]?.length > 0);

  if (!hasAny) {
    return (
      <div className="rounded-xl border border-dashed border-slate-300 p-12 text-center text-slate-500">
        No medical entities found in transcript.
      </div>
    );
  }

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {entityConfig.map(({ key, label, color }) => {
        const items = entities[key] || [];
        if (!items.length) return null;
        return (
          <Card key={key} className={`border ${color}`}>
            <h4 className="mb-3 text-sm font-semibold text-slate-900 dark:text-white">{label}</h4>
            <div className="flex flex-wrap gap-2">
              {items.map((item, i) => (
                <Badge key={i} variant="default">{item}</Badge>
              ))}
            </div>
          </Card>
        );
      })}
    </div>
  );
}
