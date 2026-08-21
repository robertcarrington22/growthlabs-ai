import { createFileRoute, Link } from "@tanstack/react-router";

export const Route = createFileRoute("/pricing")({
  component: Pricing,
});

const TIERS = [
  { revenue: "$500K–$2M", price: "$1,000", per: "month", tag: "" },
  { revenue: "$2M–$5M", price: "$2,000", per: "month", tag: "Most Popular" },
  { revenue: "$5M–$10M", price: "$3,500", per: "month", tag: "" },
  { revenue: "$7.5M–$10M", price: "$4,500", per: "month", tag: "Premium" },
];

function Pricing() {
  return (
    <>
      <section className="bg-gradient-to-br from-indigo-50 via-white to-blue-50 py-16 sm:py-24">
        <div className="mx-auto max-w-7xl px-6 text-center">
          <span className="inline-block rounded-full bg-indigo-100 px-4 py-1.5 text-sm font-medium text-indigo-700">
            Pricing
          </span>
          <h1 className="mt-6 text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl">
            Simple, Transparent Pricing
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-600">
            Start with a free scorecard or a low-risk audit. Then choose a retainer tier
            that fits your company size.
          </p>
        </div>
      </section>

      {/* Free + Audit row */}
      <section className="bg-white py-16 sm:py-20">
        <div className="mx-auto max-w-5xl px-6">
          <div className="grid gap-8 md:grid-cols-2">
            {/* Free */}
            <div className="flex flex-col rounded-2xl border border-gray-200 bg-white p-8 shadow-sm transition-all hover:shadow-lg">
              <span className="text-xs font-semibold uppercase tracking-wider text-indigo-600">Free</span>
              <h2 className="mt-2 text-2xl font-bold text-gray-900">Revenue Health Scorecard</h2>
              <p className="mt-1 text-4xl font-bold text-indigo-600">$0</p>
              <p className="mt-1 text-sm text-gray-500">5-minute self-assessment</p>
              <p className="mt-4 text-sm leading-relaxed text-gray-600">
                A quick diagnostic that scores your business across pricing, churn, upsell,
                channels, and data maturity. You'll get a personalized report showing your
                biggest revenue gaps — no commitment required.
              </p>
              <ul className="mt-6 space-y-3">
                {[
                  "15-question interactive assessment",
                  "Score across 5 revenue dimensions",
                  "Personalized gap analysis",
                  "Benchmark against industry peers",
                ].map((item) => (
                  <li key={item} className="flex items-start gap-2 text-sm text-gray-700">
                    <svg className="mt-0.5 h-4 w-4 shrink-0 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                    {item}
                  </li>
                ))}
              </ul>
              <div className="mt-auto pt-8">
                <Link to="/scorecard" className="block rounded-lg bg-indigo-600 px-6 py-3 text-center text-sm font-semibold text-white shadow-sm transition-all hover:bg-indigo-700">
                  Take the Scorecard →
                </Link>
              </div>
            </div>

            {/* Audit */}
            <div className="flex flex-col rounded-2xl border-2 border-indigo-200 bg-white p-8 shadow-md transition-all hover:shadow-lg">
              <span className="inline-block self-start rounded-full bg-indigo-100 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-indigo-700">
                Recommended Start
              </span>
              <h2 className="mt-2 text-2xl font-bold text-gray-900">Discovery Audit</h2>
              <p className="mt-1 text-4xl font-bold text-indigo-600">$495–$995</p>
              <p className="mt-1 text-sm text-gray-500">One-time flat fee</p>
              <p className="mt-4 text-sm leading-relaxed text-gray-600">
                A comprehensive AI-powered analysis of your revenue data. We identify
                pricing leaks, churn patterns, channel inefficiencies, and upsell gaps —
                then deliver a prioritized growth plan. <strong>The audit fee is credited
                in full toward your first retainer month</strong> if you continue.
              </p>
              <ul className="mt-6 space-y-3">
                {[
                  "Full AI analysis of your CRM, billing & analytics",
                  "Revenue opportunities ranked by estimated impact",
                  "Written report with ROI estimates and shown arithmetic",
                  "Personalized retainer proposal",
                  "Audit fee credited toward first retainer month",
                ].map((item) => (
                  <li key={item} className="flex items-start gap-2 text-sm text-gray-700">
                    <svg className="mt-0.5 h-4 w-4 shrink-0 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                    {item}
                  </li>
                ))}
              </ul>
              <div className="mt-auto pt-8">
                <Link to="/contact" className="block rounded-lg bg-indigo-600 px-6 py-3 text-center text-sm font-semibold text-white shadow-sm transition-all hover:bg-indigo-700">
                  Start Your Audit →
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Retainer tiers */}
      <section className="bg-gray-50 py-16 sm:py-20">
        <div className="mx-auto max-w-5xl px-6">
          <div className="text-center">
            <h2 className="text-3xl font-bold text-gray-900 sm:text-4xl">Growth Retainer</h2>
            <p className="mt-4 text-lg text-gray-600">
              Ongoing support to execute your growth plan. Choose the tier that matches
              your company size.
            </p>
          </div>

          <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {TIERS.map((tier) => (
              <div key={tier.revenue} className={`flex flex-col rounded-2xl border bg-white p-6 shadow-sm transition-all hover:shadow-lg ${tier.tag === "Most Popular" ? "border-2 border-indigo-200" : "border-gray-200"}`}>
                {tier.tag && (
                  <span className={`inline-block self-start rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-wider ${tier.tag === "Most Popular" ? "bg-indigo-100 text-indigo-700" : "bg-gray-100 text-gray-600"}`}>
                    {tier.tag}
                  </span>
                )}
                <h3 className={`mt-3 text-lg font-bold text-gray-900`}>${tier.price}</h3>
                <p className="mt-1 text-sm text-gray-500">{tier.per}</p>
                <p className="mt-3 text-sm text-gray-600">For companies with revenue of <strong>{tier.revenue}</strong></p>
                <ul className="mt-6 space-y-2 text-sm text-gray-600">
                  <li className="flex items-start gap-2">
                    <svg className="mt-0.5 h-4 w-4 shrink-0 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                    Monthly implementation support
                  </li>
                  <li className="flex items-start gap-2">
                    <svg className="mt-0.5 h-4 w-4 shrink-0 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                    Real-time KPI dashboards
                  </li>
                  <li className="flex items-start gap-2">
                    <svg className="mt-0.5 h-4 w-4 shrink-0 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                    Quarterly business reviews
                  </li>
                </ul>
                <div className="mt-auto pt-6">
                  <Link to="/contact" className="block rounded-lg bg-indigo-600 px-4 py-2.5 text-center text-sm font-semibold text-white shadow-sm transition-all hover:bg-indigo-700">
                    Start with an Audit →
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="bg-white py-16 sm:py-20">
        <div className="mx-auto max-w-3xl px-6">
          <h2 className="text-center text-3xl font-bold text-gray-900 sm:text-4xl">How Pricing Works</h2>
          <div className="mt-12 space-y-8">
            {[
              {
                step: "1",
                title: "Start with the Scorecard or Audit",
                desc: "Take the free Revenue Health Scorecard for a quick assessment, or jump straight into the Discovery Audit ($495–$995) for a comprehensive analysis of your revenue gaps.",
              },
              {
                step: "2",
                title: "Review your results",
                desc: "You'll get a detailed report with prioritized opportunities, each with an estimated annual impact. If you started with the audit, the fee is credited toward your first retainer month.",
              },
              {
                step: "3",
                title: "Choose your retainer tier",
                desc: "Select the Growth Retainer tier that matches your company size. No negotiation, no hidden fees — just the support you need at a transparent price.",
              },
            ].map((item) => (
              <div key={item.step} className="flex gap-4">
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-indigo-600 text-sm font-bold text-white">{item.step}</div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">{item.title}</h3>
                  <p className="mt-1 text-sm leading-relaxed text-gray-600">{item.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="bg-gray-50 py-16 sm:py-20">
        <div className="mx-auto max-w-3xl px-6">
          <h2 className="text-center text-3xl font-bold text-gray-900">Pricing FAQ</h2>
          <div className="mt-12 space-y-8">
            {[
              {
                q: "What if I'm not sure which tier I fall into?",
                a: "That's what the Discovery Audit is for. After analyzing your data, we'll know your company's revenue profile and can recommend the right tier. The audit fee is credited toward your first retainer month regardless.",
              },
              {
                q: "Is the audit fee really credited toward the retainer?",
                a: "Yes. If you start a Growth Retainer within 60 days of your audit, the full audit fee is deducted from your first retainer payment. If the audit costs $795 and your retainer is $2,000/month, your first month is $1,205.",
              },
              {
                q: "What if my company is between tiers?",
                a: "Choose the tier that best matches your current revenue. We're flexible — if you're at $4.8M and trending toward $5M, we might start you at the $3,500 tier. We'll discuss this during your audit delivery.",
              },
              {
                q: "Can I start with just the audit?",
                a: "Absolutely. The Discovery Audit stands on its own — you get a complete growth plan with prioritized recommendations and ROI estimates. No commitment to a retainer required.",
              },
            ].map((faq) => (
              <div key={faq.q}>
                <h3 className="text-lg font-semibold text-gray-900">{faq.q}</h3>
                <p className="mt-2 text-sm leading-relaxed text-gray-600">{faq.a}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="bg-indigo-600 py-16 sm:py-20">
        <div className="mx-auto max-w-3xl px-6 text-center">
          <h2 className="text-3xl font-bold text-white sm:text-4xl">
            Ready to Find Your Hidden Revenue?
          </h2>
          <p className="mt-4 text-lg text-indigo-200">
            Start with a free Revenue Health Scorecard or jump straight to the Discovery Audit.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-4">
            <Link to="/scorecard" className="inline-block rounded-lg bg-white px-8 py-3.5 text-base font-semibold text-indigo-700 shadow-lg hover:bg-indigo-50">
              Take the Free Scorecard →
            </Link>
            <Link to="/contact" className="inline-block rounded-lg border border-white/30 px-8 py-3.5 text-base font-semibold text-white hover:bg-white/10">
              Start Your Audit →
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}