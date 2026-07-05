import { useEffect, useState } from 'react';
import PageHeader from '../components/layout/PageHeader';
import VisitList from '../components/visits/VisitList';
import { getVisits } from '../api/visits';

export default function Visits() {
  const [visits, setVisits] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [status, setStatus] = useState('');

  const fetchVisits = () => {
    setLoading(true);
    const params = {};
    if (search) params.search = search;
    if (status) params.status = status;
    getVisits(params)
      .then(setVisits)
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchVisits();
  }, [status]);

  return (
    <div>
      <PageHeader title="Visits" subtitle="Browse and manage clinical visits" />
      <div className="mb-6 flex flex-wrap gap-4">
        <input
          className="input-field max-w-xs"
          placeholder="Search patient, clinician..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && fetchVisits()}
        />
        <select
          className="input-field w-auto"
          value={status}
          onChange={(e) => setStatus(e.target.value)}
        >
          <option value="">All Statuses</option>
          <option value="draft">Draft</option>
          <option value="reviewed">Reviewed</option>
          <option value="approved">Approved</option>
        </select>
        <button onClick={fetchVisits} className="btn-secondary">Search</button>
      </div>
      <VisitList visits={visits} loading={loading} />
    </div>
  );
}
