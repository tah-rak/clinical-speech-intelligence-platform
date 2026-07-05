import { useState } from 'react';
import Button from '../ui/Button';
import Textarea from '../ui/Textarea';
import Card from '../ui/Card';

export default function WerForm({ visits, onCalculate, loading }) {
  const [reference, setReference] = useState('');
  const [visitId, setVisitId] = useState('');

  const handleVisitSelect = (id) => {
    setVisitId(id);
    const visit = visits.find((v) => v.id === id);
    if (visit?.transcript_text) {
      // hypothesis will be set from visit
    }
  };

  const selectedVisit = visits.find((v) => v.id === visitId);
  const hypothesis = selectedVisit?.transcript_text || '';

  return (
    <Card>
      <h3 className="mb-4 text-lg font-semibold">Word Error Rate Calculator</h3>
      <div className="space-y-4">
        <div>
          <label className="mb-1 block text-sm font-medium">Reference Transcript</label>
          <Textarea
            value={reference}
            onChange={(e) => setReference(e.target.value)}
            placeholder="Paste the ground-truth reference transcript..."
            rows={6}
          />
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium">Generated Transcript (from visit)</label>
          <select
            className="input-field mb-2"
            value={visitId}
            onChange={(e) => handleVisitSelect(e.target.value)}
          >
            <option value="">Select a visit...</option>
            {visits.map((v) => (
              <option key={v.id} value={v.id}>
                {v.patient_name} — {v.visit_date}
              </option>
            ))}
          </select>
          <Textarea value={hypothesis} readOnly rows={6} className="bg-slate-50 dark:bg-slate-800" />
        </div>
        <Button
          onClick={() => onCalculate(reference, hypothesis)}
          disabled={loading || !reference || !hypothesis}
        >
          {loading ? 'Calculating...' : 'Calculate WER'}
        </Button>
      </div>
    </Card>
  );
}
