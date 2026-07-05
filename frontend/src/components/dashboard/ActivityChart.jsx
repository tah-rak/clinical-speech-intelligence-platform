import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import Card from '../ui/Card';

export default function ActivityChart({ data }) {
  const chartData = data?.length ? data : [
    { name: 'Mon', visits: 0 },
    { name: 'Tue', visits: 0 },
    { name: 'Wed', visits: 0 },
    { name: 'Thu', visits: 0 },
    { name: 'Fri', visits: 0 },
    { name: 'Sat', visits: 0 },
    { name: 'Sun', visits: 0 },
  ];

  return (
    <Card>
      <h3 className="mb-4 text-sm font-semibold text-slate-900 dark:text-white">
        Weekly Activity
      </h3>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" className="stroke-slate-200 dark:stroke-slate-700" />
            <XAxis dataKey="name" tick={{ fontSize: 12 }} />
            <YAxis tick={{ fontSize: 12 }} allowDecimals={false} />
            <Tooltip />
            <Bar dataKey="visits" fill="#0d9488" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}
