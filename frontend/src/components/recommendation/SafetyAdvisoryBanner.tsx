import React from 'react';

interface SafetyAdvisoryBannerProps {
  advisory: string | null;
}

export const SafetyAdvisoryBanner: React.FC<SafetyAdvisoryBannerProps> = ({ advisory }) => {
  if (!advisory) {
    return null;
  }

  return (
    <div
      role="alert"
      className="bg-amber-50 border-2 border-amber-400 rounded-2xl p-5 shadow-xs space-y-2"
    >
      <div className="flex items-center space-x-2 text-amber-900 font-bold text-sm">
        <span className="w-6 h-6 rounded-full bg-amber-400 text-white flex items-center justify-center text-xs font-black">
          !
        </span>
        <span className="uppercase tracking-wider">
          Contextual Food Safety Advisory (Decision-Support Warning)
        </span>
      </div>

      <div className="text-xs text-amber-950 font-medium leading-relaxed bg-white/70 p-3.5 rounded-xl border border-amber-200">
        {advisory}
      </div>

      <p className="text-[11px] text-amber-800 italic">
        Notice: This system provides contextual decision-support heuristics and does not certify
        commercial food safety or regulatory compliance (21 CFR 114 / FSSAI regulations). Process
        validation by an accredited food safety authority is required.
      </p>
    </div>
  );
};
