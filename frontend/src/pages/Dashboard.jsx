import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Users, FileText, Clock, Mic } from 'lucide-react';
import PageHeader from '../components/layout/PageHeader';
import MetricCard from '../components/dashboard/MetricCard';
import ActivityChart from '../components/dashboard/ActivityChart';
import ProviderStatus from '../components/dashboard/ProviderStatus';
import VisitList from '../components/visits/VisitList';
import Button from '../components/ui/Button';
import { getAnalytics } from '../api/analytics';
import { getVisits } from '../api/visits';

export default function Dashboard() {
  const [analytics, setAnalytics] = useState(null);
  const [visits, setVisits] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getAnalytics(), getVisits()])
      .then(([a, v]) => {
        setAnalytics(a);
        setVisits(v.slice(0, 5));
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const chartData = [
    { name: 'Mon', visits: 0 },
    { name: 'Tue', visits: 0 },
    { name: 'Wed', visits: 0 },
    { name: 'Thu', visits: 0 },
    { name: 'Fri', visits: 0 },
    { name: 'Sat', visits: 0 },
    { name: 'Sun', visits: analytics?.files_processed_this_week || 0 },
  ];

  return (
    <div>
      <div className="mb-8 rounded-2xl bg-gradient-to-br from-medical-600 to-medical-800 p-8 text-white">
        <h1 className="text-3xl font-bold">Clinical Speech Intelligence Platform</h1>
        <p className="mt-2 max-w-2xl text-medical-100">
          Convert clinical conversations into transcripts, medical entities, and SOAP notes.
        </p>
        <Link to="/upload" className="mt-6 inline-block">
          <Button className="!bg-white !text-medical-700 hover:!bg-medical-50">
            Upload New Visit
          </Button>
        </Link>
      </div>

      <div className="mb-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <MetricCard
          title="Visits Processed"
          value={analytics?.total_visits ?? '—'}
          icon={Users}
        />
        <MetricCard
          title="SOAP Notes Generated"
          value={analytics?.soap_notes_generated ?? '—'}
          icon={FileText}
        />
        <MetricCard
          title="Avg Processing Time"
          value={analytics ? `${analytics.average_processing_time_seconds}s` : '—'}
          icon={Clock}
        />
        <MetricCard
          title="STT Provider"
          value={analytics?.transcription_provider ?? 'local'}
          icon={Mic}
        />
      </div>

      <div className="mb-8 grid gap-6 lg:grid-cols-2">
        <ActivityChart data={chartData} />
        <ProviderStatus status={analytics?.provider_status} />
      </div>

      <PageHeader
        title="Recent Visits"
        subtitle="Latest processed clinical visits"
        action={
          <Link to="/visits">
            <Button variant="secondary">View All</Button>
          </Link>
        }
      />
      <VisitList visits={visits} loading={loading} />
    </div>
  );
}
