import { Upload } from 'lucide-react';

export default function FileUpload({ onChange, accept = '.wav,.mp3,.m4a', file, disabled }) {
  return (
    <label className={`flex flex-col items-center justify-center rounded-xl border-2 border-dashed border-slate-300 bg-slate-50 p-8 transition hover:border-medical-400 hover:bg-medical-50/50 dark:border-slate-700 dark:bg-slate-800/50 dark:hover:border-medical-600 ${disabled ? 'opacity-50 pointer-events-none' : 'cursor-pointer'}`}>
      <Upload className="mb-3 h-10 w-10 text-medical-500" />
      <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
        {file ? file.name : 'Click to upload audio'}
      </span>
      <span className="mt-1 text-xs text-slate-500">WAV, MP3, or M4A</span>
      <input
        type="file"
        accept={accept}
        className="hidden"
        onChange={onChange}
        disabled={disabled}
      />
    </label>
  );
}
