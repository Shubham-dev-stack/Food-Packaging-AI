import { useEffect, useState } from 'react'

interface HealthData {
  status: string
  service: string
  version: string
}

export default function App() {
  const [health, setHealth] = useState<HealthData | null>(null)
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetch('/api/health')
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error ${res.status}`)
        }
        return res.json()
      })
      .then((data: HealthData) => {
        setHealth(data)
        setLoading(false)
      })
      .catch((err: Error) => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col justify-between font-sans">
      <header className="border-b border-slate-200 bg-white shadow-xs">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <span className="inline-flex items-center justify-center h-9 w-9 rounded-lg bg-emerald-600 text-white font-bold text-sm">
              FP
            </span>
            <div>
              <h1 className="text-lg font-bold leading-none text-slate-900">
                Food Packaging Material Recommendation System
              </h1>
              <p className="text-xs text-slate-500 mt-1">
                SIH 2026 Problem Statement ID: SIH26236 • Phase 0 Foundation
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <span className="px-2.5 py-1 text-xs font-semibold rounded-full bg-slate-100 text-slate-700 border border-slate-200">
              Phase 0 Tooling Verified
            </span>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-12 flex-1 w-full flex flex-col justify-center">
        <div className="bg-white rounded-xl border border-slate-200 p-8 shadow-sm">
          <div className="mb-6 pb-6 border-b border-slate-100">
            <h2 className="text-2xl font-bold text-slate-800">
              System Architecture & Health Harness
            </h2>
            <p className="text-slate-600 mt-2 text-sm">
              Phase 0 establishes the engineering environment, typed contracts, runtime tooling, and API proxies before domain modelling and recommendation physics begin.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="border border-slate-200 rounded-lg p-4 bg-slate-50">
              <h3 className="font-semibold text-slate-700 text-sm">Backend API Status</h3>
              <div className="mt-3 flex items-center space-x-2">
                {loading && (
                  <span className="text-sm text-slate-500 animate-pulse">Checking /api/health...</span>
                )}
                {error && (
                  <span className="inline-flex items-center px-2.5 py-1 text-xs font-medium rounded-full bg-amber-100 text-amber-800">
                    Offline / Not running ({error})
                  </span>
                )}
                {health && (
                  <span className="inline-flex items-center px-2.5 py-1 text-xs font-medium rounded-full bg-emerald-100 text-emerald-800">
                    Online: {health.status} ({health.service} v{health.version})
                  </span>
                )}
              </div>
              <p className="text-xs text-slate-500 mt-2">
                FastAPI endpoint mounted at <code className="bg-slate-200 px-1 py-0.5 rounded text-[11px]">/api/health</code>
              </p>
            </div>

            <div className="border border-slate-200 rounded-lg p-4 bg-slate-50">
              <h3 className="font-semibold text-slate-700 text-sm">Frontend Tooling</h3>
              <div className="mt-3 flex items-center space-x-2">
                <span className="inline-flex items-center px-2.5 py-1 text-xs font-medium rounded-full bg-sky-100 text-sky-800">
                  Vite + React 19 + TypeScript + Tailwind
                </span>
              </div>
              <p className="text-xs text-slate-500 mt-2">
                Fully typed React build harness verified with strict TypeScript compilation
              </p>
            </div>
          </div>

          <div className="mt-8 rounded-lg bg-emerald-50 border border-emerald-200 p-4">
            <h4 className="font-semibold text-emerald-900 text-sm">Phase 0 Guardrails Active</h4>
            <p className="text-xs text-emerald-800 mt-1">
              Domain logic, database entities, and recommendation algorithms remain strictly locked until Phase 1 data modeling.
            </p>
          </div>
        </div>
      </main>

      <footer className="border-t border-slate-200 bg-white py-4 text-center text-xs text-slate-500">
        SIH 2026 Problem Statement SIH26236 • Decision-Support System Architecture
      </footer>
    </div>
  )
}
