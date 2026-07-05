import Card from '../ui/Card';

export default function EvaluationResults({ result }) {
  if (!result) return null;

  const werPercent = (result.wer * 100).toFixed(2);
  const accuracy = ((1 - result.wer) * 100).toFixed(2);

  return (
    <Card>
      <h3 className="mb-6 text-lg font-semibold">Evaluation Results</h3>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <div className="rounded-xl bg-medical-50 p-4 text-center dark:bg-medical-900/20">
          <p className="text-3xl font-bold text-medical-700 dark:text-medical-300">{werPercent}%</p>
          <p className="text-sm text-slate-500">Word Error Rate</p>
        </div>
        <div className="rounded-xl bg-emerald-50 p-4 text-center dark:bg-emerald-900/20">
          <p className="text-3xl font-bold text-emerald-700 dark:text-emerald-300">{accuracy}%</p>
          <p className="text-sm text-slate-500">Accuracy</p>
        </div>
        <div className="rounded-xl bg-slate-50 p-4 text-center dark:bg-slate-800">
          <p className="text-3xl font-bold">{result.reference_word_count}</p>
          <p className="text-sm text-slate-500">Reference Words</p>
        </div>
        <div className="rounded-xl bg-slate-50 p-4 text-center dark:bg-slate-800">
          <p className="text-3xl font-bold">{result.hypothesis_word_count}</p>
          <p className="text-sm text-slate-500">Hypothesis Words</p>
        </div>
      </div>
      <div className="mt-6 grid gap-4 sm:grid-cols-3">
        <div className="rounded-lg border border-slate-200 p-4 dark:border-slate-700">
          <p className="text-2xl font-bold text-amber-600">{result.substitutions}</p>
          <p className="text-sm text-slate-500">Substitutions</p>
        </div>
        <div className="rounded-lg border border-slate-200 p-4 dark:border-slate-700">
          <p className="text-2xl font-bold text-red-500">{result.deletions}</p>
          <p className="text-sm text-slate-500">Deletions</p>
        </div>
        <div className="rounded-lg border border-slate-200 p-4 dark:border-slate-700">
          <p className="text-2xl font-bold text-blue-500">{result.insertions}</p>
          <p className="text-sm text-slate-500">Insertions</p>
        </div>
      </div>
    </Card>
  );
}
