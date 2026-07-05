import { useState, useEffect } from 'react';
import { Save } from 'lucide-react';
import Button from '../ui/Button';
import Textarea from '../ui/Textarea';
import Card from '../ui/Card';

const sections = [
  { key: 'subjective', label: 'Subjective', description: 'Patient-reported symptoms and history' },
  { key: 'objective', label: 'Objective', description: 'Observable findings and vitals' },
  { key: 'assessment', label: 'Assessment', description: 'Clinical impression and diagnosis' },
  { key: 'plan', label: 'Plan', description: 'Treatment and follow-up plan' },
];

export default function SoapEditor({ soap, onSave, status, onStatusChange }) {
  const [form, setForm] = useState({ subjective: '', objective: '', assessment: '', plan: '' });
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    if (soap) {
      setForm({
        subjective: soap.subjective || '',
        objective: soap.objective || '',
        assessment: soap.assessment || '',
        plan: soap.plan || '',
      });
    }
  }, [soap]);

  const handleSave = async () => {
    setSaving(true);
    try {
      await onSave(form);
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
    } finally {
      setSaving(false);
    }
  };

  if (!soap) {
    return (
      <div className="rounded-xl border border-dashed border-slate-300 p-12 text-center text-slate-500">
        No SOAP note generated yet.
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <span className="text-sm text-slate-500">Review status:</span>
          <select
            value={status || 'draft'}
            onChange={(e) => onStatusChange?.(e.target.value)}
            className="input-field w-auto"
          >
            <option value="draft">Draft</option>
            <option value="reviewed">Reviewed</option>
            <option value="approved">Approved</option>
          </select>
        </div>
        <Button onClick={handleSave} disabled={saving}>
          <Save className="mr-2 h-4 w-4" />
          {saving ? 'Saving...' : saved ? 'Saved!' : 'Save SOAP Note'}
        </Button>
      </div>

      {sections.map(({ key, label, description }) => (
        <Card key={key}>
          <div className="mb-3">
            <h4 className="font-semibold text-slate-900 dark:text-white">{label}</h4>
            <p className="text-xs text-slate-500">{description}</p>
          </div>
          <Textarea
            value={form[key]}
            onChange={(e) => setForm({ ...form, [key]: e.target.value })}
            rows={4}
          />
        </Card>
      ))}
    </div>
  );
}
