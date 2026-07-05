import { useEffect, useState } from 'react';
import PageHeader from '../components/layout/PageHeader';
import WerForm from '../components/evaluation/WerForm';
import EvaluationResults from '../components/evaluation/EvaluationResults';
import { getVisits } from '../api/visits';
import { computeWer } from '../api/analytics';

export default function Evaluation() {
  const [visits, setVisits] = useState([]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    getVisits().then(setVisits).catch(console.error);
  }, []);

  const handleCalculate = async (reference, hypothesis) => {
    setLoading(true);
    try {
      const res = await computeWer(reference, hypothesis);
      setResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <PageHeader
        title="Evaluation"
        subtitle="Compare reference and generated transcripts using Word Error Rate"
      />
      <div className="grid gap-6 lg:grid-cols-2">
        <WerForm visits={visits} onCalculate={handleCalculate} loading={loading} />
        <EvaluationResults result={result} />
      </div>
    </div>
  );
}
