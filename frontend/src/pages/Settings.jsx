import { useEffect, useState } from 'react';
import { AlertTriangle, CheckCircle } from 'lucide-react';
import PageHeader from '../components/layout/PageHeader';
import Card from '../components/ui/Card';
import Badge from '../components/ui/Badge';
import { getHealth } from '../api/analytics';

export default function Settings() {
  const [health, setHealth] = useState(null);

  useEffect(() => {
    getHealth().then(setHealth).catch(console.error);
  }, []);

  const providers = health?.providers || {};

  const configItems = [
    { label: 'STT Provider', value: providers.stt_provider, required: true },
    { label: 'Storage Provider', value: providers.storage_provider, required: true },
    { label: 'Database Provider', value: providers.database_provider, required: true },
    { label: 'Whisper Model', value: providers.whisper_model },
    { label: 'LLM Provider', value: providers.llm_provider || (providers.llm_enabled ? 'configured' : 'Disabled (template fallback)') },
    { label: 'AWS S3', value: providers.aws_enabled ? 'Enabled' : 'Disabled' },
    { label: 'Azure Speech', value: providers.azure_speech_enabled ? 'Enabled' : 'Disabled' },
    { label: 'GCP', value: providers.gcp_enabled ? 'Enabled' : 'Disabled' },
    { label: 'Ollama', value: providers.ollama_enabled ? 'Enabled' : 'Disabled' },
  ];

  const warnings = [];
  if (!providers.azure_speech_enabled && providers.stt_provider === 'azure') {
    warnings.push('Azure Speech is selected but not configured. Falling back to local Whisper.');
  }
  if (!providers.aws_enabled && providers.storage_provider === 's3') {
    warnings.push('S3 storage is selected but AWS is not enabled.');
  }

  return (
    <div>
      <PageHeader
        title="Settings"
        subtitle="Current provider configuration (secrets are never displayed)"
      />

      {warnings.map((w, i) => (
        <div key={i} className="mb-4 flex items-start gap-2 rounded-lg bg-amber-50 px-4 py-3 text-sm text-amber-800 dark:bg-amber-900/20 dark:text-amber-300">
          <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0" />
          {w}
        </div>
      ))}

      <Card>
        <h3 className="mb-4 text-lg font-semibold">Provider Configuration</h3>
        <div className="divide-y divide-slate-200 dark:divide-slate-800">
          {configItems.map(({ label, value, required }) => (
            <div key={label} className="flex items-center justify-between py-3">
              <span className="text-sm text-slate-600 dark:text-slate-400">{label}</span>
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium capitalize">{value || '—'}</span>
                {required && value && (
                  <CheckCircle className="h-4 w-4 text-emerald-500" />
                )}
              </div>
            </div>
          ))}
        </div>
      </Card>

      <Card className="mt-6">
        <h3 className="mb-2 text-lg font-semibold">Environment Variables</h3>
        <p className="text-sm text-slate-500">
          Configure providers via backend <code className="rounded bg-slate-100 px-1 dark:bg-slate-800">.env</code> file.
          See <code className="rounded bg-slate-100 px-1 dark:bg-slate-800">backend/.env.example</code> for all options.
        </p>
        <div className="mt-4 flex flex-wrap gap-2">
          <Badge>STT_PROVIDER</Badge>
          <Badge>STORAGE_PROVIDER</Badge>
          <Badge>AWS_ENABLED</Badge>
          <Badge>AZURE_SPEECH_KEY</Badge>
          <Badge>LLM_PROVIDER</Badge>
          <Badge>LLM_API_KEY</Badge>
          <Badge>GCP_ENABLED</Badge>
        </div>
      </Card>
    </div>
  );
}
