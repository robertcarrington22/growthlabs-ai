import { createFileRoute, Link } from "@tanstack/react-router";

export const Route = createFileRoute("/how-it-works")({
  component: HowItWorks,
});

const PHASES = [
  {
    num: "01",
    title: "Audit",
    time: "Week 1–2",
    description:
      "We connect to your data sources — CRM, billing, analytics — and let our AI engine map your revenue landscape. It analyzes customer segments, pricing tiers, churn signals, channel performance, and upsell opportunities. What takes humans weeks, our AI does in hours.",
    details: [
      "Connect your data (CRM, billing, analytics) with secure read-only integrations",
      "AI engine maps customer segments, pricing tiers, and churn signals",
      "We identify 10–20 revenue opportunities ranked by impact",
      "Pricing efficiency, churn patterns, channel attribution, upsell pathways",
    ],
    deliverable: "Discovery Audit Report",
  },
  {
    num: "02",
    title: "Plan",
    time: "Week 3",
    description:
      "We present our findings in a collaborative strategy session. Together, we review the data, discuss what's realistic for your team, and prioritize 3–5 highest-impact initiatives. We also present a personalized Growth Retainer proposal with pricing based on your company size and the scope of opportunity we've identified. You leave with a clear 90-day execution roadmap that your team can start implementing immediately.",
    details: [
      "We present findings in a strategy session with your team",
      "Prioritize 3–5 highest-impact initiatives based on effort vs. return",
      "Receive a personalized Growth Retainer proposal with pricing",
      "Build a detailed 90-day execution roadmap",
      "Clear owners, timelines, and success metrics for every initiative",
    ],
    deliverable: "Revenue Growth Plan",
  },
  {
    num: "03",
    title: "Execute",
    time: "Ongoing",
    description:
      "This is where we become your growth partner. We provide monthly implementation support, track progress with shared dashboards, and continuously optimize based on what the data says. Real results, real accountability.",
    details: [
      "Monthly implementation support from your dedicated growth advisor",
      "Track progress with shared dashboards updated in real time",
      "Iterate based on real results — double down on what works",
      "Quarterly business reviews to assess progress and reset priorities",
    ],
    deliverable: "Monthly Growth Reports",
  },
];

function HowItWorks() {
  return (
    <>
      <section className="bg-gradient-to-br from-indigo-50 via-white to-blue-50 py-16 sm:py-24">
        <div className="mx-auto max-w-7xl px-6 text-center">
          <span className="inline-block rounded-full bg-indigo-100 px-4 py-1.5 text-sm font-medium text-indigo-700">
            How It Works
          </span>
          <h1 className="mt-6 text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl">
            From data to dollars in three phases.
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-600">
            A proven process designed to minimize friction and maximize results. Here's
            exactly what to expect when you work with GrowthLabs AI.
          </p>
        </div>
      </section>

      <section className="bg-white py-16 sm:py-24">
        <div className="mx-auto max-w-4xl px-6">
          <div className="relative space-y-16">
            <div className="absolute left-8 top-0 hidden h-full w-0.5 bg-indigo-100 md:block" />
            {PHASES.map((phase, i) => (
              <div key={phase.num} className="relative md:flex md:gap-10">
                <div className="relative z-10 flex h-16 w-16 shrink-0 items-center justify-center rounded-full bg-indigo-600 text-xl font-bold text-white shadow-lg md:mx-0">
                  {phase.num}
                </div>
                <div className="mt-4 flex-1 md:mt-0">
                  <span className="text-sm font-semibold uppercase tracking-wider text-indigo-600">
                    Phase {phase.num} — {phase.time}
                  </span>
                  <h2 className="mt-2 text-2xl font-bold text-gray-900 sm:text-3xl">
                    {phase.title}
                  </h2>
                  <p className="mt-4 text-base leading-relaxed text-gray-600">
                    {phase.description}
                  </p>
                  <ul className="mt-6 space-y-3">
                    {phase.details.map((d) => (
                      <li key={d} className="flex items-start gap-3 text-sm text-gray-700">
                        <svg
                          className="mt-0.5 h-5 w-5 shrink-0 text-indigo-500"
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M13 7l5 5m0 0l-5 5m5-5H6"
                          />
                        </svg>
                        {d}
                      </li>
                    ))}
                  </ul>
                  <div className="mt-6 inline-block rounded-full bg-indigo-50 px-4 py-1.5 text-xs font-semibold uppercase tracking-wider text-indigo-700">
                    Deliverable: {phase.deliverable}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="bg-gray-50 py-16 sm:py-24">
        <div className="mx-auto max-w-7xl px-6">
          <div className="mx-auto max-w-3xl text-center">
            <h2 className="text-3xl font-bold text-gray-900 sm:text-4xl">
              Choose Your Engagement Path
            </h2>
            <p className="mt-4 text-lg text-gray-600">
              Both paths follow the same process through Phase 2. The difference is how much
              support you want after that.
            </p>
          </div>
          <div className="mt-12 grid gap-8 md:grid-cols-2">
            <div className="rounded-2xl border border-gray-200 bg-white p-8 shadow-sm">
              <h3 className="text-xl font-bold text-gray-900">Discovery Audit</h3>
              <p className="mt-2 text-3xl font-bold text-indigo-600">$495–$995</p>
              <p className="mt-1 text-sm text-gray-500">One-time fee — credited toward first retainer month</p>
              <p className="mt-4 text-sm leading-relaxed text-gray-600">
                Best for: businesses that want a complete diagnostic and a clear roadmap
                they can execute internally.
              </p>
              <ul className="mt-6 space-y-3">
                {[
                  "A full analysis of your pricing, customers, and channels",
                  "Prioritized growth roadmap with ROI estimates",
                  "Written report & strategy presentation",
                  "90-day execution plan",
                ].map((item) => (
                  <li key={item} className="flex items-start gap-2 text-sm text-gray-700">
                    <svg className="mt-0.5 h-4 w-4 shrink-0 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                    {item}
                  </li>
                ))}
              </ul>
              <Link to="/services" className="mt-8 block rounded-lg bg-indigo-600 px-6 py-3 text-center font-semibold text-white transition-all hover:bg-indigo-700">
                View Services →
              </Link>
            </div>
            <div className="rounded-2xl border-2 border-indigo-200 bg-white p-8 shadow-md">
              <span className="inline-block rounded-full bg-indigo-100 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-indigo-700">
                Recommended
              </span>
              <h3 className="mt-3 text-xl font-bold text-gray-900">Growth Retainer</h3>
              <p className="mt-2 text-3xl font-bold text-indigo-600">Priced after audit</p>
              <p className="mt-1 text-sm text-gray-500">Ongoing — pricing based on your company size</p>
              <p className="mt-4 text-sm leading-relaxed text-gray-600">
                Best for: businesses that want a dedicated growth partner to execute the plan alongside them.
              </p>
              <ul className="mt-6 space-y-3">
                {[
                  "Everything in the Discovery Audit",
                  "Monthly implementation support",
                  "Real-time KPI dashboards",
                  "Quarterly business reviews",
                ].map((item) => (
                  <li key={item} className="flex items-start gap-2 text-sm text-gray-700">
                    <svg className="mt-0.5 h-4 w-4 shrink-0 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                    {item}
                  </li>
                ))}
              </ul>
              <Link to="/contact" className="mt-8 block rounded-lg bg-indigo-600 px-6 py-3 text-center font-semibold text-white shadow-sm transition-all hover:bg-indigo-700">
                Start Your Audit →
              </Link>
            </div>
          </div>
        </div>
      </section>

      <section className="bg-indigo-600 py-16 sm:py-20">
        <div className="mx-auto max-w-3xl px-6 text-center">
          <h2 className="text-3xl font-bold text-white sm:text-4xl">
            Ready to Start Your Growth Journey?
          </h2>
          <p className="mt-4 text-lg text-indigo-200">
            Your free discovery call is just 30 minutes away. Let's find your revenue
            gaps together.
          </p>
          <div className="mt-8">
            <Link to="/contact" className="inline-block rounded-lg bg-white px-8 py-3.5 text-base font-semibold text-indigo-700 shadow-lg transition-all hover:bg-indigo-50 hover:shadow-xl">
              Start Your Audit →
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}