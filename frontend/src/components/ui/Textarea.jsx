export default function Textarea({ className = '', ...props }) {
  return (
    <textarea
      className={`input-field min-h-[120px] resize-y ${className}`}
      {...props}
    />
  );
}
