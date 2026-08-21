import { createFileRoute, Link } from "@tanstack/react-router";

export const Route = createFileRoute("/industries/agencies")({
  component: Agencies,
});

function Agencies() {
  return (
    <>
      <section className="bg-gradient-to-br from-indigo-50 via-white to-blue-50 py-16 sm:py-24">
        <div className="mx-auto max-w-7xl px-6 text-center">
          <span className="inline-block rounded-full bg-indigo-100 px-4 py-1.5 text-sm font-medium text-indigo-700">
            Agencies & Consultancies
          </span>
          <h1 className="mt-6 text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl">
            Stop Leaving Revenue on the Table
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-600">
            Most agencies hit a revenue ceiling because their pricing, utilization, and
            project profitability are invisible. We make them visible — and fixable.
          </p>
        </div>
      </section>

      <section className="bg-white py-16 sm:py-20">
        <div className="mx-auto max-w-5xl px-6">
          <div className="grid gap-12 lg:grid-cols-2">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">The Agency Revenue Trap</h2>
              <p className="mt-4 text-base leading-relaxed text-gray-600">
                You're billing by the hour. Your best people are fully utilized. Revenue
                is flat. You're working harder for the same (or less) money.
              </p>
              <p className="mt-3 text-base leading-relaxed text-gray-600">
                The problem isn't your team or your work. It's that your pricing model
                caps your earnings at the number of hours you can sell. Every agency hits
                this ceiling — the ones that break through are the ones that shift from
                hourly billing to value-based pricing.
              </p>
              <div className="mt-8 space-y-4 rounded-xl border border-gray-100 bg-gray-50 p-6">
                <h3 className="font-semibold text-gray-900">Common Revenue Leaks We Find</h3>
                <ul className="space-y-3">
                  {[
                    { label: "Scope Creep", desc: "5–15% of revenue lost to unbilled overruns" },
                    { label: "Utilization Rates", desc: "Most agencies run below 70% — every 10% gain = 20–30% more revenue" },
                    { label: "Project Profitability", desc: "20% of projects often subsidize the rest — but you can't see it" },
                    { label: "Blended Billing Rate", desc: "Average $/hour across all staff — not tracked by project or client" },
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
              <h3 className="text-xl font-bold">From Hourly to Value-Based Pricing</h3>
              <p className="mt-3 text-sm leading-relaxed text-indigo-100">
                The single most impactful transition an agency can make. Firms that switch
                from hourly to value-based pricing typically see <strong>25–50% revenue increases</strong>.
              </p>
              <p className="mt-3 text-sm leading-relaxed text-indigo-100">
                Our AI audit analyzes your project data to determine exactly where your
                pricing leverage is, which clients are underpriced, and what a value-based
                model would look like for your agency.
              </p>
              <div className="mt-6">
                <Link to="/contact" className="inline-block rounded-lg bg-white px-6 py-3 text-sm font-semibold text-indigo-700 shadow-sm transition-all hover:bg-indigo-50">
                  Book Your Discovery Audit →
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="bg-gray-50 py-16 sm:py-20">
        <div className="mx-auto max-w-5xl px-6">
          <h2 className="text-center text-2xl font-bold text-gray-900 sm:text-3xl">What Our AI Analyzes for Agencies</h2>
          <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {[
              { q: "What's the true project-level profitability?", icon: "📊" },
              { q: "Where is scope creep happening most?", icon: "🔍" },
              { q: "Which clients are underpriced relative to value?", icon: "💰" },
              { q: "What's the utilization rate by team and project?", icon: "⏱️" },
              { q: "Which channels bring the highest-value clients?", icon: "📈" },
              { q: "What would a value-based pricing model look like?", icon: "🔄" },
            ].map((item) => (
              <div key={item.q} className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
                <span className="text-2xl">{item.icon}</span>
                <p className="mt-3 text-sm font-medium text-gray-900">{item.q}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="bg-white py-16 sm:py-20">
        <div className="mx-auto max-w-3xl px-6">
          <h2 className="text-center text-2xl font-bold text-gray-900 sm:text-3xl">From Our Research</h2>
          <div className="mt-8 space-y-6">
            <div className="rounded-xl border border-indigo-100 bg-indigo-50 p-6">
              <p className="text-sm leading-relaxed text-gray-700">
                <strong>The $1M Ceiling:</strong> Most agencies hit a revenue wall around $1M because
                the founder can personally serve only so many clients. The fix isn't always
                hiring — often pricing changes alone can unlock the next level.
              </p>
            </div>
            <div className="rounded-xl border border-indigo-100 bg-indigo-50 p-6">
              <p className="text-sm leading-relaxed text-gray-700">
                <strong>Churn Reality:</strong> Professional services firms lose 15–25% of clients
                annually. Most don't track leading churn indicators like declining engagement
                or procurement involvement — patterns our AI catches before you lose the client.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="bg-indigo-600 py-16 sm:py-20">
        <div className="mx-auto max-w-3xl px-6 text-center">
          <h2 className="text-3xl font-bold text-white sm:text-4xl">
            Ready to Find Your Agency's Revenue Gaps?
          </h2>
          <p className="mt-4 text-lg text-indigo-200">
            Start with a $100 Discovery Audit. We'll analyze your data and show you exactly
            where the money's hiding.
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