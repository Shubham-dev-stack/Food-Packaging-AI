import React from 'react';

interface FormFieldProps {
  label: string;
  sublabel?: string;
  error?: string;
  required?: boolean;
  isOverride?: boolean;
  onResetOverride?: () => void;
  children: React.ReactNode;
}

export const FormField: React.FC<FormFieldProps> = ({
  label,
  sublabel,
  error,
  required,
  isOverride,
  onResetOverride,
  children,
}) => {
  return (
    <div className="space-y-1.5">
      <div className="flex items-center justify-between text-xs">
        <label className="font-semibold text-slate-700 flex items-center space-x-1">
          <span>{label}</span>
          {required && <span className="text-rose-500 font-bold">*</span>}
          {isOverride && (
            <span className="ml-1.5 inline-flex items-center px-1.5 py-0.2 rounded text-[10px] font-medium bg-amber-100 text-amber-800 border border-amber-300">
              User Override
            </span>
          )}
        </label>
        {isOverride && onResetOverride && (
          <button
            type="button"
            onClick={onResetOverride}
            className="text-[11px] text-slate-500 hover:text-slate-800 underline cursor-pointer"
          >
            Reset to Baseline
          </button>
        )}
      </div>
      {sublabel && <p className="text-[11px] text-slate-500">{sublabel}</p>}
      <div>{children}</div>
      {error && (
        <p className="text-[11px] text-rose-600 font-medium flex items-center space-x-1">
          <span>⚠</span>
          <span>{error}</span>
        </p>
      )}
    </div>
  );
};
