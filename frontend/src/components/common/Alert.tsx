import React from 'react';

interface AlertProps {
  type?: 'info' | 'warning' | 'error' | 'success';
  title?: string;
  children: React.ReactNode;
  className?: string;
}

export const Alert: React.FC<AlertProps> = ({
  type = 'info',
  title,
  children,
  className = '',
}) => {
  const styles = {
    info: 'bg-blue-50 border-blue-200 text-blue-900',
    warning: 'bg-amber-50 border-amber-200 text-amber-900',
    error: 'bg-rose-50 border-rose-200 text-rose-900',
    success: 'bg-emerald-50 border-emerald-200 text-emerald-900',
  };

  const badgeStyles = {
    info: 'bg-blue-200 text-blue-900',
    warning: 'bg-amber-200 text-amber-900',
    error: 'bg-rose-200 text-rose-900',
    success: 'bg-emerald-200 text-emerald-900',
  };

  return (
    <div
      role="alert"
      className={`border rounded-xl p-4 text-sm ${styles[type]} ${className}`}
    >
      {title && (
        <div className="flex items-center space-x-2 font-semibold mb-1">
          <span className={`text-xs px-2 py-0.5 rounded font-mono ${badgeStyles[type]}`}>
            {type.toUpperCase()}
          </span>
          <span>{title}</span>
        </div>
      )}
      <div className="leading-relaxed">{children}</div>
    </div>
  );
};
