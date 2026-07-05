import { Clock, User } from 'lucide-react';
import Badge from '../ui/Badge';

export default function TranscriptViewer({ visit }) {
  const segments = visit?.transcript_segments?.segments || [];
  const formatted = visit?.transcript_segments?.formatted || visit?.transcript_text;

  if (!formatted && !segments.length) {
    return (
      <div className="rounded-xl border border-dashed border-slate-300 p-12 text-center text-slate-500 dark:border-slate-700">
        No transcript available. Run transcription to generate.
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {visit?.speaker_labels_estimated && (
        <div className="rounded-lg bg-amber-50 px-4 py-3 text-sm text-amber-800 dark:bg-amber-900/20 dark:text-amber-300">
          Speaker labels are estimated based on transcript segments, not true diarization.
        </div>
      )}

      {segments.length > 0 ? (
        <div className="space-y-4">
          {segments.map((seg, i) => (
            <div key={i} className="flex gap-4 rounded-xl border border-slate-200 p-4 dark:border-slate-700">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-medical-100 text-medical-700 dark:bg-medical-900/30">
                <User className="h-5 w-5" />
              </div>
              <div className="flex-1">
                <div className="mb-1 flex items-center gap-2">
                  <span className="font-semibold text-slate-900 dark:text-white">
                    {seg.speaker || 'Speaker'}
                  </span>
                  <span className="flex items-center gap-1 text-xs text-slate-400">
                    <Clock className="h-3 w-3" />
                    {seg.start?.toFixed(1)}s – {seg.end?.toFixed(1)}s
                  </span>
                  {seg.confidence && (
                    <Badge variant="default">{Math.round(seg.confidence * 100)}%</Badge>
                  )}
                </div>
                <p className="text-slate-700 dark:text-slate-300">{seg.text}</p>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <pre className="whitespace-pre-wrap rounded-xl border border-slate-200 bg-slate-50 p-6 text-sm leading-relaxed dark:border-slate-700 dark:bg-slate-800">
          {formatted}
        </pre>
      )}
    </div>
  );
}
