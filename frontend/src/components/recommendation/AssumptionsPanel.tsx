import React, { useState } from 'react';

interface AssumptionsPanelProps {
  assumptions: string[];
}

export const AssumptionsPanel: React.FC<AssumptionsPanelProps> = ({ assumptions }) => {
  const [isOpen, setIsOpen] = useState(false);

  if (assumptions.length === 0) {
    return null;
  }

  return (
    <div className="border border-slate-200 rounded-2xl bg-white shadow-xs overflow-hidden">
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between px-6 py-4 bg-slate-50 hover:bg-slate-100 transition cursor-pointer text-left"
        aria-expanded={isOpen}
      >
        <div className="flex items-center space-x-3">
          <span className="text-sm font-bold text-slate-800">
            Documented Engineering Assumptions
          </span>
          <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-blue-100 text-blue-800 border border-blue-200">
            {assumptions.length} Prototype Assumptions
          </span>
        </div>
        <div className="flex items-center space-x-2 text-slate-500 text-xs font-medium">
          <span>{isOpen ? 'Collapse' : 'Inspect Modeling Assumptions'}</span>
          <svg
            className={`w-4 h-4 transform transition-transform ${isOpen ? 'rotate-180' : ''}`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </button>

      {isOpen && (
        <div className="p-6 space-y-3 bg-white">
          <p className="text-xs text-slate-500">
            The decision engine incorporates the following analytical assumptions to model mass
            transfer and barrier kinetics under standard commercial operating conditions:
          </p>

          <ul className="space-y-2">
            {assumptions.map((item, idx) => (
              <li
                key={idx}
                className="p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs text-slate-700 font-medium leading-relaxed flex items-start space-x-2.5"
              >
                <span className="text-blue-600 font-bold mt-0.5">•</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
