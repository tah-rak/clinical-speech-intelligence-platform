import { Link } from 'react-router-dom';
import { format } from '../../utils/date';
import Badge from '../ui/Badge';
import Card from '../ui/Card';

export default function VisitList({ visits, loading }) {
  if (loading) {
    return (
      <Card>
        <div className="animate-pulse space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-12 rounded-lg bg-slate-100 dark:bg-slate-800" />
          ))}
        </div>
      </Card>
    );
  }

  if (!visits?.length) {
    return (
      <Card className="text-center py-12">
        <p className="text-slate-500">No visits yet. Upload your first clinical visit to get started.</p>
        <Link to="/upload" className="mt-4 inline-block text-medical-600 hover:underline">
          Upload Visit →
        </Link>
      </Card>
    );
  }

  return (
    <Card className="overflow-hidden p-0">
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-slate-200 bg-slate-50 dark:border-slate-800 dark:bg-slate-800/50">
              <th className="px-6 py-3 text-left font-medium text-slate-500">Patient</th>
              <th className="px-6 py-3 text-left font-medium text-slate-500">Clinician</th>
              <th className="px-6 py-3 text-left font-medium text-slate-500">Date</th>
              <th className="px-6 py-3 text-left font-medium text-slate-500">Status</th>
              <th className="px-6 py-3 text-left font-medium text-slate-500">Provider</th>
            </tr>
          </thead>
          <tbody>
            {visits.map((visit) => (
              <tr
                key={visit.id}
                className="border-b border-slate-100 transition hover:bg-slate-50 dark:border-slate-800 dark:hover:bg-slate-800/50"
              >
                <td className="px-6 py-4">
                  <Link to={`/visits/${visit.id}`} className="font-medium text-medical-600 hover:underline">
                    {visit.patient_name}
                  </Link>
                </td>
                <td className="px-6 py-4 text-slate-600 dark:text-slate-400">{visit.clinician_name}</td>
                <td className="px-6 py-4 text-slate-600 dark:text-slate-400">{format(visit.visit_date)}</td>
                <td className="px-6 py-4">
                  <Badge variant={visit.status}>{visit.status}</Badge>
                </td>
                <td className="px-6 py-4 text-slate-500 capitalize">{visit.transcription_provider || '—'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  );
}
