import { CheckCircle, XCircle, Cloud, Mic, Database } from 'lucide-react';
import Card from '../ui/Card';
import Badge from '../ui/Badge';

const providers = [
  { key: 'whisper', label: 'Local Whisper', icon: Mic, check: (s) => s?.stt_provider === 'local' || true },
  { key: 'aws', label: 'AWS S3', icon: Cloud, check: (s) => s?.aws_enabled },
  { key: 'azure', label: 'Azure Speech', icon: Mic, check: (s) => s?.azure_speech_enabled },
  { key: 'gcp', label: 'GCP Firestore', icon: Database, check: (s) => s?.gcp_enabled },
];

export default function ProviderStatus({ status }) {
  return (
    <Card>
      <h3 className="mb-4 text-sm font-semibold text-slate-900 dark:text-white">
        Provider Status
      </h3>
      <div className="grid gap-3 sm:grid-cols-2">
        {providers.map(({ key, label, icon: Icon, check }) => {
          const enabled = check(status || {});
          return (
            <div
              key={key}
              className="flex items-center justify-between rounded-lg border border-slate-200 p-3 dark:border-slate-700"
            >
              <div className="flex items-center gap-2">
                <Icon className="h-4 w-4 text-medical-600" />
                <span className="text-sm font-medium">{label}</span>
              </div>
              {enabled ? (
                <Badge variant="success"><CheckCircle className="mr-1 h-3 w-3 inline" /> Active</Badge>
              ) : (
                <Badge variant="default"><XCircle className="mr-1 h-3 w-3 inline" /> Off</Badge>
              )}
            </div>
          );
        })}
      </div>
    </Card>
  );
}
