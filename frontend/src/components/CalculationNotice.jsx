import { AlertTriangle, ArrowUpRight } from "lucide-react";

export const CalculationNotice = ({ basis, onReview }) => {
  if (!basis) return null;
  return <details className="border-y border-amber-200 bg-amber-50/70 text-amber-950" data-testid="calculation-basis-notice">
    <summary className="flex cursor-pointer flex-wrap items-center justify-between gap-2 px-3 py-2.5 text-xs" data-testid="calculation-basis-toggle">
      <span className="flex items-center gap-2"><AlertTriangle size={14} className="shrink-0" /><strong>Preliminary · engineer review required</strong></span>
      <span className="text-[11px]">{basis.warnings.length} input warnings · View basis</span>
    </summary>
    <div className="border-t border-amber-200 px-4 py-3 text-xs leading-relaxed" data-testid="calculation-basis-details">
      {basis.warnings.length > 0 && <ul className="mb-3 list-disc space-y-1 pl-4">{basis.warnings.map(w => <li key={w.id} data-testid={`calculation-warning-${w.id}`}>{w.message}</li>)}</ul>}
      <p className="font-medium">Area method: {basis.area_method}</p><p className="mt-2">{basis.precision_policy}</p>
      <ul className="mt-3 list-disc space-y-1 pl-4">{basis.limitations.map((text, i) => <li key={text} data-testid={`calculation-limitation-${i}`}>{text}</li>)}</ul>
      <button className="mt-4 inline-flex items-center gap-1 font-semibold underline underline-offset-4" onClick={onReview} data-testid="calculation-review-inputs">Review data reliability <ArrowUpRight size={13} /></button>
    </div>
  </details>;
};