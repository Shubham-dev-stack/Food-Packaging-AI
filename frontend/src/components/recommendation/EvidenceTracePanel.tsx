import React, { useEffect, useState } from 'react';
import { api, ApiError } from '../../services/api';
import type { EvidenceSourceResponse } from '../../types/api';

interface EvidenceTracePanelProps {
  citedSourceIds: string[];
}

export const EvidenceTracePanel: React.FC<EvidenceTracePanelProps> = ({ citedSourceIds }) => {
  const [sources, setSources] = useState<Record<string, EvidenceSourceResponse | null>>({});
  const [loading, setLoading] = useState<boolean>(citedSourceIds.length > 0);
  const [selectedSourceForModal, setSelectedSourceForModal] = useState<EvidenceSourceResponse | null>(null);
  const [fetchErrors, setFetchErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    let isMounted = true;
    if (citedSourceIds.length === 0) {
      return;
    }

    const loadEvidence = async () => {
      setLoading(true);
      const results: Record<string, EvidenceSourceResponse | null> = {};
      const errors: Record<string, string> = {};

      await Promise.all(
        citedSourceIds.map(async (refId) => {
          try {
            const data = await api.getEvidence(refId);
            if (isMounted) results[refId] = data;
          } catch (err) {
            if (isMounted) {
              results[refId] = null;
              if (err instanceof ApiError && err.status === 404) {
                errors[refId] = 'Reference not found in knowledge repository';
              } else {
                errors[refId] = 'Failed to load evidence metadata';
              }
            }
          }
        })
      );

      if (isMounted) {
        setSources(results);
        setFetchErrors(errors);
        setLoading(false);
      }
    };

    loadEvidence();
    return () => {
      isMounted = false;
    };
  }, [citedSourceIds]);

  const getSourceTypeBadge = (sourceType: string) => {
    switch (sourceType) {
      case 'peer_reviewed_journal':
        return (
          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-purple-100 text-purple-800 border border-purple-200">
            Peer-Reviewed Journal
          </span>
        );
      case 'standards_document':
        return (
          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-100 text-blue-800 border border-blue-200">
            ASTM / ISO Standard
          </span>
        );
      case 'government_compendium':
        return (
          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-200">
            Government / Regulatory Compendium
          </span>
        );
      case 'textbook':
        return (
          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-800 border border-amber-200">
            Academic Textbook
          </span>
        );
      default:
        return (
          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-100 text-slate-800 border border-slate-200">
            {sourceType.replace('_', ' ')}
          </span>
        );
    }
  };

  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-5">
      <div className="border-b border-slate-200 pb-3 flex items-center justify-between">
        <div>
          <h3 className="text-base font-bold text-slate-900">
            Scientific Evidence Traceability
          </h3>
          <p className="text-xs text-slate-500">
            Peer-reviewed literature, ASTM standards, and USDA/FDA reference sources cited by this decision
          </p>
        </div>
        <span className="px-2.5 py-1 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-300">
          {citedSourceIds.length} Cited Sources
        </span>
      </div>

      {loading && (
        <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl flex items-center space-x-3 text-xs text-slate-600">
          <div className="w-4 h-4 border-2 border-emerald-600 border-t-transparent rounded-full animate-spin" />
          <span>Resolving bibliographic citations from evidence knowledge base...</span>
        </div>
      )}

      {!loading && citedSourceIds.length === 0 && (
        <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-500">
          No explicit citations referenced for this scenario.
        </div>
      )}

      {!loading && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {citedSourceIds.map((refId) => {
            const source = sources[refId];
            const error = fetchErrors[refId];

            if (error || !source) {
              return (
                <div
                  key={refId}
                  className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-2 text-xs"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-mono font-bold text-slate-700">{refId}</span>
                    <span className="text-[10px] font-bold text-amber-700 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
                      Unresolved Reference
                    </span>
                  </div>
                  <p className="text-slate-500 text-[11px]">
                    {error || 'Metadata unavailable from evidence repository.'}
                  </p>
                </div>
              );
            }

            return (
              <div
                key={refId}
                className="p-4 bg-slate-50 hover:bg-slate-100/70 transition rounded-xl border border-slate-200 space-y-2.5 text-xs flex flex-col justify-between"
              >
                <div className="space-y-1.5">
                  <div className="flex items-center justify-between gap-2">
                    <span className="font-bold text-slate-900 text-sm">
                      {source.citation_short || source.reference_id}
                    </span>
                    {getSourceTypeBadge(source.source_type)}
                  </div>

                  <p className="font-semibold text-slate-800 leading-snug line-clamp-2">
                    {source.title}
                  </p>

                  <div className="text-[11px] text-slate-600 space-y-0.5">
                    {source.authors && <div>Authors: {source.authors}</div>}
                    <div className="flex items-center space-x-3 text-slate-500">
                      {source.publication_year && <span>Year: {source.publication_year}</span>}
                      {source.doi_or_standard_number && (
                        <span className="font-mono text-[10px] bg-white px-1.5 py-0.5 rounded border border-slate-200">
                          {source.doi_or_standard_number}
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                <div className="pt-2 border-t border-slate-200 flex items-center justify-between">
                  <span className="font-mono text-[10px] text-slate-400">{refId}</span>
                  <button
                    type="button"
                    onClick={() => setSelectedSourceForModal(source)}
                    className="text-emerald-700 hover:text-emerald-900 font-bold text-[11px] cursor-pointer"
                  >
                    View Citation Details →
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Citation Detail Modal */}
      {selectedSourceForModal && (
        <div
          role="dialog"
          aria-modal="true"
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-xs"
        >
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 space-y-4 shadow-xl border border-slate-200 animate-fade-in">
            <div className="flex items-start justify-between border-b border-slate-200 pb-3">
              <div>
                <span className="font-mono text-[10px] text-slate-500 uppercase tracking-wider block">
                  Evidence Citation
                </span>
                <h4 className="text-base font-bold text-slate-900">
                  {selectedSourceForModal.citation_short}
                </h4>
              </div>
              <button
                type="button"
                onClick={() => setSelectedSourceForModal(null)}
                className="text-slate-400 hover:text-slate-600 p-1 text-lg font-bold cursor-pointer"
                aria-label="Close modal"
              >
                ✕
              </button>
            </div>

            <div className="space-y-3 text-xs text-slate-700">
              <div>
                <span className="font-bold text-slate-900 block text-sm">
                  {selectedSourceForModal.title}
                </span>
                <span className="text-slate-500 text-[11px]">
                  {selectedSourceForModal.authors} ({selectedSourceForModal.publication_year || 'n.d.'})
                </span>
              </div>

              <div className="flex flex-wrap gap-2 pt-1">
                {getSourceTypeBadge(selectedSourceForModal.source_type)}
                {selectedSourceForModal.doi_or_standard_number && (
                  <span className="font-mono text-[10px] bg-slate-100 text-slate-700 px-2 py-0.5 rounded border border-slate-200">
                    ID / DOI: {selectedSourceForModal.doi_or_standard_number}
                  </span>
                )}
              </div>

              {selectedSourceForModal.notes && (
                <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200 space-y-1">
                  <span className="font-bold text-slate-800 text-[11px] block">
                    Verification & Scientific Scope:
                  </span>
                  <p className="text-slate-600 leading-relaxed text-[11px]">
                    {selectedSourceForModal.notes}
                  </p>
                </div>
              )}
            </div>

            <div className="pt-3 border-t border-slate-100 flex justify-end">
              <button
                type="button"
                onClick={() => setSelectedSourceForModal(null)}
                className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-xl transition cursor-pointer"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
