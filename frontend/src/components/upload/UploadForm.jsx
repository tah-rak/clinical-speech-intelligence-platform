import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { CheckCircle, Circle, Loader2 } from 'lucide-react';
import Button from '../ui/Button';
import Card from '../ui/Card';
import FileUpload from '../ui/FileUpload';
import { uploadVisit, processVisit, extractEntities, generateSoap } from '../../api/visits';

const STEPS = ['uploaded', 'transcribed', 'entities', 'soap'];

export default function UploadForm() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    patient_name: '',
    clinician_name: '',
    visit_date: new Date().toISOString().split('T')[0],
    visit_reason: '',
    use_sample_transcript: false,
  });
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentStep, setCurrentStep] = useState(-1);
  const [visitId, setVisitId] = useState(null);

  const handleSubmit = async (processAll = false) => {
    setError(null);
    setLoading(true);

    try {
      const fd = new FormData();
      Object.entries(form).forEach(([k, v]) => fd.append(k, v));
      if (file) fd.append('audio', file);

      setCurrentStep(0);
      const result = await uploadVisit(fd);
      setVisitId(result.visit_id);

      if (!processAll) {
        navigate(`/visits/${result.visit_id}`);
        return;
      }

      if (!form.use_sample_transcript) {
        setCurrentStep(1);
        await processVisit(result.visit_id);
      } else {
        setCurrentStep(1);
        await extractEntities(result.visit_id);
        setCurrentStep(2);
        await generateSoap(result.visit_id);
        setCurrentStep(3);
      }

      navigate(`/visits/${result.visit_id}`);
    } catch (err) {
      setError(err.message);
      setCurrentStep(-1);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid gap-8 lg:grid-cols-3">
      <div className="lg:col-span-2 space-y-6">
        <Card>
          <h3 className="mb-6 text-lg font-semibold">Visit Information</h3>
          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700 dark:text-slate-300">
                Patient Name
              </label>
              <input
                className="input-field"
                value={form.patient_name}
                onChange={(e) => setForm({ ...form, patient_name: e.target.value })}
                placeholder="John Doe"
                required
              />
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700 dark:text-slate-300">
                Clinician Name
              </label>
              <input
                className="input-field"
                value={form.clinician_name}
                onChange={(e) => setForm({ ...form, clinician_name: e.target.value })}
                placeholder="Dr. Smith"
                required
              />
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700 dark:text-slate-300">
                Visit Date
              </label>
              <input
                type="date"
                className="input-field"
                value={form.visit_date}
                onChange={(e) => setForm({ ...form, visit_date: e.target.value })}
              />
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-700 dark:text-slate-300">
                Visit Reason
              </label>
              <input
                className="input-field"
                value={form.visit_reason}
                onChange={(e) => setForm({ ...form, visit_reason: e.target.value })}
                placeholder="Chest pain evaluation"
              />
            </div>
          </div>

          <div className="mt-6">
            <label className="mb-3 flex items-center gap-2">
              <input
                type="checkbox"
                checked={form.use_sample_transcript}
                onChange={(e) => setForm({ ...form, use_sample_transcript: e.target.checked })}
                className="rounded border-slate-300 text-medical-600 focus:ring-medical-500"
              />
              <span className="text-sm text-slate-700 dark:text-slate-300">
                Use sample transcript (demo without audio)
              </span>
            </label>
          </div>

          {!form.use_sample_transcript && (
            <div className="mt-4">
              <FileUpload
                file={file}
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                disabled={loading}
              />
            </div>
          )}
        </Card>

        {error && (
          <div className="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700 dark:bg-red-900/20 dark:text-red-300">
            {error}
          </div>
        )}

        <div className="flex flex-wrap gap-3">
          <Button
            onClick={() => handleSubmit(false)}
            disabled={loading || !form.patient_name || !form.clinician_name}
            variant="secondary"
          >
            Upload Only
          </Button>
          <Button
            onClick={() => handleSubmit(true)}
            disabled={loading || !form.patient_name || !form.clinician_name}
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Processing...
              </>
            ) : (
              'Upload and Process'
            )}
          </Button>
        </div>
      </div>

      <Card>
        <h3 className="mb-6 text-lg font-semibold">Processing Pipeline</h3>
        <div className="space-y-4">
          {[
            { id: 0, label: 'Uploaded', key: 'uploaded' },
            { id: 1, label: 'Transcribed', key: 'transcribed' },
            { id: 2, label: 'Entities Extracted', key: 'entities' },
            { id: 3, label: 'SOAP Generated', key: 'soap' },
          ].map((step) => (
            <div key={step.id} className="flex items-center gap-3">
              {currentStep > step.id ? (
                <CheckCircle className="h-5 w-5 text-emerald-500" />
              ) : currentStep === step.id ? (
                <Loader2 className="h-5 w-5 animate-spin text-medical-600" />
              ) : (
                <Circle className="h-5 w-5 text-slate-300" />
              )}
              <span className={currentStep >= step.id ? 'font-medium text-slate-900 dark:text-white' : 'text-slate-500'}>
                {step.label}
              </span>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
