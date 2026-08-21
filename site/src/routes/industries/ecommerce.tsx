import { createFileRoute, Link } from "@tanstack/react-router";

export const Route = createFileRoute("/industries/ecommerce")({
  component: Ecommerce,
});

function Ecommerce() {
  return (
    <>
      <section className="bg-gradient-to-br from-indigo-50 via-white to-blue-50 py-16 sm:py-24">
        <div className="mx-auto max-w-7xl px-6 text-center">
          <span className="inline-block rounded-full bg-indigo-100 px-4 py-1.5 text-sm font-medium text-indigo-700">
            E-Commerce & Retail
          </span>
          <h1 className="mt-6 text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl">
            Stop Fighting Price Wars You Can't Win
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-600">
            Margin compression, cart abandonment, and rising CAC are crushing e-commerce margins. We find the data-driven pricing and retention strategies that reverse the trend.
          </p>
        </div>
      </section>

      <section className="bg-white py-16 sm:py-20">
        <div className="mx-auto max-w-5xl px-6">
          <div className="grid gap-12 lg:grid-cols-2">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">The E-Commerce Margin Squeeze</h2>
              <p className="mt-4 text-base leading-relaxed text-gray-600">
                You're competing on price, paying more for ads every quarter, and watching 70% of visitors leave without buying. Your repeat purchase rate is low. You know the problem — you just don't have the data to fix it.
              </p>
              <div className="mt-8 space-y-4 rounded-xl border border-gray-100 bg-gray-50 p-6">
                <h3 className="font-semibold text-gray-900">Common Revenue Leaks We Find</h3>
                <ul className="space-y-3">
                  {[
                    { label: "Cart Abandonment", desc: "70% average — best-in-class recovery is 50-60%" },
                    { label: "CLV Blindspot", desc: "Lifetime value unknown by channel or customer segment" },
                    { label: "Low Repeat Rate", desc: "Most customers buy once and never return" },
                    { label: "Channel Waste", desc: "20-40% of ad spend goes to low-LTV channels" },
                  ].map((item) => (
                    <li key={item.label} className="flex items-start gap-3 text-sm">
                      <svg className="mt-0.5 h-4 w-4 shrink-0 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                      <div><span className="font-medium text-gray-900">{item.label}:</span> <span className="text-gray-600">{item.desc}</span></div>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
            <div className="flex flex-col justify-center rounded-2xl bg-indigo-600 p-8 text-white">
              <h3 className="text-xl font-bold">What Our AI Analyzes</h3>
              <ul className="mt-6 space-y-3 text-sm text-indigo-100">
                <li>• True CLV by acquisition channel</li>
                <li>• Cart abandonment patterns and recovery rates</li>
                <li>• Pricing strategies that max AOV without hurting conversion</li>
                <li>• Products that drive repeat purchases</li>
                <li>• Channel-level ROI (where to double down)</li>
              </ul>
              <div className="mt-6">
                <Link to="/contact" className="inline-block rounded-lg bg-white px-6 py-3 text-sm font-semibold text-indigo-700 shadow-sm hover:bg-indigo-50">
                  Book Your Discovery Audit →
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="bg-indigo-600 py-16 sm:py-20">
        <div className="mx-auto max-w-3xl px-6 text-center">
          <h2 className="text-3xl font-bold text-white sm:text-4xl">Turn Data Into Margin</h2>
          <p className="mt-4 text-lg text-indigo-200">Start with a $100 Discovery Audit. We'll find the revenue hiding in your data.</p>
          <div className="mt-8 flex flex-wrap justify-center gap-4">
            <Link to="/contact" className="inline-block rounded-lg bg-white px-8 py-3.5 text-base font-semibold text-indigo-700 shadow-lg hover:bg-indigo-50">Start Your Audit →</Link>
            <Link to="/industries" className="inline-block rounded-lg border border-white/30 px-8 py-3.5 text-base font-semibold text-white hover:bg-white/10">View All Industries</Link>
          </div>
        </div>
      </section>
    </>
  );
}