import React from 'react';
import type { RecommendationStatus } from '../../types/api';

interface StatusBadgeProps {
  status: RecommendationStatus;
  size?: 'sm' | 'md' | 'lg';
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, size = 'md' }) => {
  const configs: Record<
    RecommendationStatus,
    { label: string; bg: string; text: string; border: string; desc: string; icon: string }
  > = {
    SUPPORTED: {
      label: 'Supported Recommendation',
      bg: 'bg-emerald-50',
      text: 'text-emerald-800',
      border: 'border-emerald-300',
      desc: 'Sufficient evidence exists for prototype decision',
      icon: '✓',
    },
    CONDITIONAL: {
      label: 'Conditional Recommendation',
      bg: 'bg-amber-50',
      text: 'text-amber-800',
      border: 'border-amber-300',
      desc: 'Recommendation depends on documented storage/handling conditions',
      icon: '⚠',
    },
    INSUFFICIENT_EVIDENCE: {
      label: 'Insufficient Evidence',
      bg: 'bg-orange-50',
      text: 'text-orange-800',
      border: 'border-orange-300',
      desc: 'Available information is not sufficient for confident recommendation',
      icon: 'ℹ',
    },
    RESEARCH_REQUIRED: {
      label: 'Research Required',
      bg: 'bg-rose-50',
      text: 'text-rose-800',
      border: 'border-rose-300',
      desc: 'Scientific or experimental data is missing; no answer fabricated',
      icon: '!',
    },
  };

  const config = configs[status] || {
    label: status,
    bg: 'bg-slate-50',
    text: 'text-slate-800',
    border: 'border-slate-300',
    desc: 'Status unknown',
    icon: '•',
  };

  const sizeClasses = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-3 py-1 text-xs',
    lg: 'px-4 py-1.5 text-sm',
  };

  return (
    <div className="inline-flex flex-col">
      <span
        className={`inline-flex items-center space-x-1.5 font-bold rounded-lg border ${config.bg} ${config.text} ${config.border} ${sizeClasses[size]}`}
      >
        <span className="font-mono">{config.icon}</span>
        <span>{config.label}</span>
      </span>
      {size === 'lg' && (
        <span className="text-[11px] text-slate-500 mt-1">{config.desc}</span>
      )}
    </div>
  );
};
