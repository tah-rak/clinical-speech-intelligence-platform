import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import PageHeader from '../components/layout/PageHeader';
import Tabs from '../components/ui/Tabs';
import Badge from '../components/ui/Badge';
import TranscriptViewer from '../components/visits/TranscriptViewer';
import EntityCards from '../components/visits/EntityCards';
import SoapEditor from '../components/visits/SoapEditor';
import ActionItems from '../components/visits/ActionItems';
import Card from '../components/ui/Card';
import { getVisit, updateSoap, updateStatus } from '../api/visits';
import { format, formatDuration } from '../utils/date';

const TABS = [
  { id: 'transcript', label: 'Transcript' },
  { id: 'entities', label: 'Medical Entities' },
  { id: 'soap', label: 'SOAP Note' },
  { id: 'summary', label: 'Summary' },
  { id: 'evaluation', label: 'Evaluation' },
];

export default function VisitDetailPage() {
  const { id } = useParams();
  const [visit, setVisit] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('transcript');

  const refresh = () => {
    getVisit(id)
      .then(setVisit)
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    refresh();
  }, [id]);

  if (loading) {
    return <div className="animate-pulse space-y-4">
      <div className="h-8 w-64 rounded bg-slate-200 dark:bg-slate-800" />
      <div className="h-64 rounded-xl bg-slate-200 dark:bg-slate-800" />
    </div>;
  }

  if (!visit) {
    return <div className="text-center text-slate-500">Visit not found.</div>;
  }

  return (
    <div>
      <PageHeader
        title={visit.patient_name}
        subtitle={`${visit.clinician_name} · ${format(visit.visit_date)}`}
        action={<Badge variant={visit.status}>{visit.status}</Badge>}
      />

      <Card className="mb-6">
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4 text-sm">
          <div>
            <span className="text-slate-500">Visit Reason</span>
            <p className="font-medium">{visit.visit_reason || '—'}</p>
          </div>
          <div>
            <span className="text-slate-500">Audio Duration</span>
            <p className="font-medium">{formatDuration(visit.audio_duration_seconds)}</p>
          </div>
          <div>
            <span className="text-slate-500">STT Provider</span>
            <p className="font-medium capitalize">{visit.transcription_provider || '—'}</p>
          </div>
          <div>
            <span className="text-slate-500">Processing Time</span>
            <p className="font-medium">{visit.processing_time_seconds ? `${visit.processing_time_seconds}s` : '—'}</p>
          </div>
        </div>
      </Card>

      <Tabs tabs={TABS} active={activeTab} onChange={setActiveTab} />

      <div className="mt-6">
        {activeTab === 'transcript' && <TranscriptViewer visit={visit} />}
        {activeTab === 'entities' && <EntityCards entities={visit.entities_json} />}
        {activeTab === 'soap' && (
          <SoapEditor
            soap={visit.soap_note_json}
            status={visit.status}
            onSave={async (soap) => {
              await updateSoap(id, soap);
              refresh();
            }}
            onStatusChange={async (status) => {
              await updateStatus(id, status);
              refresh();
            }}
          />
        )}
        {activeTab === 'summary' && (
          <ActionItems items={visit.action_items_json} summary={visit.visit_summary} />
        )}
        {activeTab === 'evaluation' && (
          <Card>
            <h4 className="mb-4 font-semibold">Processing Metrics</h4>
            <div className="grid gap-4 sm:grid-cols-3">
              <div className="rounded-lg bg-slate-50 p-4 dark:bg-slate-800">
                <p className="text-2xl font-bold">{visit.processing_time_seconds || 0}s</p>
                <p className="text-sm text-slate-500">Processing Time</p>
              </div>
              <div className="rounded-lg bg-slate-50 p-4 dark:bg-slate-800">
                <p className="text-2xl font-bold">{visit.transcript_text?.split(/\s+/).length || 0}</p>
                <p className="text-sm text-slate-500">Transcript Words</p>
              </div>
              <div className="rounded-lg bg-slate-50 p-4 dark:bg-slate-800">
                <p className="text-2xl font-bold">
                  {visit.entities_json
                    ? Object.values(visit.entities_json).flat().length
                    : 0}
                </p>
                <p className="text-sm text-slate-500">Entities Extracted</p>
              </div>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
}
