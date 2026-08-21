import { createFileRoute, Link } from "@tanstack/react-router";
import { useState } from "react";

export const Route = createFileRoute("/roi")({
  component: ROI,
});

function ROI() {
  const [revenue, setRevenue] = useState(1000000);
  const [gapPercent, setGapPercent] = useState(8);
  const [churnRate, setChurnRate] = useState(20);

  const revenueGap = Math.round(revenue * (gapPercent / 100));
  const churnSavings = Math.round(revenue * (churnRate / 100) * 0.3); // 30% of churn is recoverable
  const totalOpportunity = revenueGap + churnSavings;
  const estRetainerCost = revenue <= 2000000 ? 1000 : revenue <= 5000000 ? 2000 : 3500;
  const annualRetainerCost = estRetainerCost * 12;
  const netROI = totalOpportunity - annualRetainerCost;
  const roiMultiple = annualRetainerCost > 0 ? (totalOpportunity / annualRetainerCost).toFixed(1) : "0";

  return (
    <>
      <section className="bg-gradient-to-br from-indigo-50 via-white to-blue-50 py-16 sm:py-24">
        <div className="mx-auto max-w-7xl px-6 text-center">
          <span className="inline-block rounded-full bg-indigo-100 px-4 py-1.5 text-sm font-medium text-indigo-700">ROI Calculator</span>
          <h1 className="mt-6 text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl">How Much Revenue Is Your Business Leaving on the Table?</h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-600">Use this calculator to estimate the revenue opportunity — and what a GrowthLabs AI engagement could return.</p>
        </div>
      </section>

      <section className="bg-white py-16 sm:py-20">
        <div className="mx-auto max-w-5xl px-6">
          <div className="grid gap-12 lg:grid-cols-2">
            {/* Inputs */}
            <div className="space-y-8">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Annual Revenue: <span className="font-bold text-indigo-600">${revenue.toLocaleString()}</span>
                </label>
                <input type="range" min="500000" max="10000000" step="100000" value={revenue} onChange={(e) => setRevenue(Number(e.target.value))}
                  className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600" />
                <div className="flex justify-between text-xs text-gray-400 mt-1">
                  <span>$500K</span>
                  <span>$10M</span>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Estimated Revenue Gap: <span className="font-bold text-indigo-600">{gapPercent}%</span>
                </label>
                <input type="range" min="2" max="25" step="1" value={gapPercent} onChange={(e) => setGapPercent(Number(e.target.value))}
                  className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600" />
                <div className="flex justify-between text-xs text-gray-400 mt-1">
                  <span>2% (minimal)</span>
                  <span>25% (significant)</span>
                </div>
                <p className="mt-1 text-xs text-gray-400">Typical range: 5–15%. Most businesses have 8–12% in pricing gaps alone.</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Current Annual Churn Rate: <span className="font-bold text-indigo-600">{churnRate}%</span>
                </label>
                <input type="range" min="5" max="40" step="1" value={churnRate} onChange={(e) => setChurnRate(Number(e.target.value))}
                  className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600" />
                <div className="flex justify-between text-xs text-gray-400 mt-1">
                  <span>5% (low)</span>
                  <span>40% (high)</span>
                </div>
                <p className="mt-1 text-xs text-gray-400">Professional services average 15–25%. SaaS averages 5–10%.</p>
              </div>

              <div className="rounded-xl bg-gray-50 p-4">
                <p className="text-xs text-gray-500">
                  <strong>How we calculate:</strong> Revenue gap = annual revenue × estimated gap %.
                  Churn recovery = annual revenue × churn rate × 30% (industry average recoverable).
                  These are conservative estimates based on industry benchmarks.
                </p>
              </div>
            </div>

            {/* Results */}
            <div className="space-y-6">
              <h2 className="text-xl font-bold text-gray-900">Estimated Opportunity</h2>
              
              <div className="grid gap-4">
                <div className="rounded-xl border border-gray-200 bg-white p-5">
                  <p className="text-sm text-gray-500">Revenue Gap Recovery</p>
                  <p className="text-2xl font-bold text-indigo-600">${revenueGap.toLocaleString()}/year</p>
                  <p className="text-xs text-gray-400">From pricing inefficiencies, upsell gaps, and channel optimization</p>
                </div>
                <div className="rounded-xl border border-gray-200 bg-white p-5">
                  <p className="text-sm text-gray-500">Churn Reduction Savings</p>
                  <p className="text-2xl font-bold text-green-600">${churnSavings.toLocaleString()}/year</p>
                  <p className="text-xs text-gray-400">Based on recovering 30% of churned revenue</p>
                </div>
              </div>

              <div className="rounded-xl border-2 border-indigo-200 bg-indigo-50 p-6">
                <p className="text-sm font-medium text-indigo-700">Total Estimated Opportunity</p>
                <p className="text-3xl font-extrabold text-indigo-600">${totalOpportunity.toLocaleString()}/year</p>
              </div>

              <div className="rounded-xl border border-gray-200 bg-white p-5">
                <p className="text-sm text-gray-500">Estimated Retainer Investment</p>
                <p className="text-xl font-bold text-gray-900">${annualRetainerCost.toLocaleString()}/year</p>
                <p className="text-xs text-gray-400">~${estRetainerCost.toLocaleString()}/month based on your revenue tier</p>
              </div>

              <div className="rounded-xl border-2 border-green-200 bg-green-50 p-6 text-center">
                <p className="text-sm font-medium text-green-700">Net ROI</p>
                <p className="text-3xl font-extrabold text-green-600">+${netROI.toLocaleString()}/year</p>
                <p className="mt-1 text-sm font-semibold text-green-700">{roiMultiple}× return on investment</p>
              </div>

              <Link to="/contact" className="block rounded-lg bg-indigo-600 px-8 py-4 text-center text-base font-semibold text-white shadow-sm transition-all hover:bg-indigo-700">
                Get Your Real Numbers — Start the Audit →
              </Link>
              <p className="text-center text-xs text-gray-400">This is an estimate based on industry benchmarks. Your actual opportunity will be quantified in your Discovery Audit.</p>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}