import { createFileRoute, Link } from "@tanstack/react-router";

export const Route = createFileRoute("/industries/saas")({
  component: SaaS,
});

function SaaS() {
  return (
    <>
      <section className="bg-gradient-to-br from-indigo-50 via-white to-blue-50 py-16 sm:py-24">
        <div className="mx-auto max-w-7xl px-6 text-center">
          <span className="inline-block rounded-full bg-indigo-100 px-4 py-1.5 text-sm font-medium text-indigo-700">
            SaaS & Tech
          </span>
          <h1 className="mt-6 text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl">
            Optimize Your Subscription Revenue
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-600">
            Most SaaS companies optimize for acquisition but neglect pricing tiers,
            expansion revenue, and churn signals. We close those gaps.
          </p>
        </div>
      </section>

      <section className="bg-white py-16 sm:py-20">
        <div className="mx-auto max-w-5xl px-6">
          <div className="grid gap-12 lg:grid-cols-2">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">The SaaS Growth Paradox</h2>
              <p className="mt-4 text-base leading-relaxed text-gray-600">
                You're acquiring customers — but your Net Revenue Retention (NRR) is below
                110%. That means you're shrinking even as you grow. Every new customer is
                just filling the bucket that's leaking from the bottom.
              </p>
              <p className="mt-3 text-base leading-relaxed text-gray-600">
                Most SMB SaaS companies don't track NRR by segment, don't know which
                pricing tier generates the highest LTV, and have no systematic upsell
                program. Our AI audit surfaces every gap.
              </p>
              <div className="mt-8 space-y-4 rounded-xl border border-gray-100 bg-gray-50 p-6">
                <h3 className="font-semibold text-gray-900">Common Revenue Leaks We Find</h3>
                <ul className="space-y-3">
                  {[
                    { label: "NRR Below 110%", desc: "Expansion revenue isn't offsetting churn — you're contracting" },
                    { label: "Underpriced Entry Tiers", desc: "Free/cheap tiers that don't convert at optimal rates" },
                    { label: "Payment Failures", desc: "A major source of involuntary churn that's fixable" },
                    { label: "Usage Blindspots", desc: "Declining feature adoption is a leading churn indicator you're missing" },
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
              <h3 className="text-xl font-bold">The Land-and-Expand Model</h3>
              <p className="mt-3 text-sm leading-relaxed text-indigo-100">
                Salesforce pioneered this: get a small team onboard, prove value, then
                expand to the whole organization. It's the same logic as our audit → retainer
                model. Low entry, high expansion.
              </p>
              <p className="mt-3 text-sm leading-relaxed text-indigo-100">
                For SaaS specifically, expansion revenue is the single highest-leverage
                growth lever. A 10% improvement in NRR compounds to 2–3× more enterprise
                value over 5 years.
              </p>
              <div className="mt-6">
                <Link to="/contact" className="inline-block rounded-lg bg-white px-6 py-3 text-sm font-semibold text-indigo-700 shadow-sm hover:bg-indigo-50">
                  Book Your Discovery Audit →
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="bg-gray-50 py-16 sm:py-20">
        <div className="mx-auto max-w-5xl px-6">
          <h2 className="text-center text-2xl font-bold text-gray-900 sm:text-3xl">What Our AI Analyzes for SaaS</h2>
          <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {[
              { q: "What is NRR by customer segment?", icon: "📊" },
              { q: "Which pricing tier generates the highest LTV?", icon: "💰" },
              { q: "What's the free-to-paid conversion rate?", icon: "🔄" },
              { q: "Where are payment failures happening?", icon: "💳" },
              { q: "Which accounts are showing churn signals?", icon: "⚠️" },
              { q: "What's the optimal pricing structure?", icon: "📈" },
            ].map((item) => (
              <div key={item.q} className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
                <span className="text-2xl">{item.icon}</span>
                <p className="mt-3 text-sm font-medium text-gray-900">{item.q}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="bg-indigo-600 py-16 sm:py-20">
        <div className="mx-auto max-w-3xl px-6 text-center">
          <h2 className="text-3xl font-bold text-white sm:text-4xl">
            Ready to Optimize Your SaaS Revenue?
          </h2>
          <p className="mt-4 text-lg text-indigo-200">
            Start with a $100 Discovery Audit. We'll analyze your data and show you exactly
            where the growth is hiding.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-4">
            <Link to="/contact" className="inline-block rounded-lg bg-white px-8 py-3.5 text-base font-semibold text-indigo-700 shadow-lg hover:bg-indigo-50">
              Start Your Audit →
            </Link>
            <Link to="/industries" className="inline-block rounded-lg border border-white/30 px-8 py-3.5 text-base font-semibold text-white hover:bg-white/10">
              View All Industries
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}