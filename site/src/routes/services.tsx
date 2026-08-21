import { createFileRoute, Link } from "@tanstack/react-router";

export const Route = createFileRoute("/services")({
  component: Services,
});

const SERVICES = [
  {
    id: "discovery-audit",
    title: "Discovery Audit",
    price: "$495–$995",
    tagline: "Know exactly where your revenue is leaking.",
    headline: "Know exactly where your revenue is leaking.",
    description:
      "A comprehensive AI-driven analysis of your customer and revenue data. We ingest your CRM, billing records, and analytics — then surface every pricing inefficiency, churn pattern, and upsell opportunity. You walk away with a prioritized list of revenue opportunities, each with an estimated impact, plus a written report and strategy presentation. The audit fee is credited in full toward your first retainer month.",
    whatYouGet: [
      "AI-driven analysis of your customer & revenue data (pricing, churn, channel performance, upsell gaps)",
      "Prioritized list of revenue opportunities with estimated impact",
      "Written report & strategy presentation",
    ],
    cta: "Book Your Audit →",
  },
  {
    id: "growth-retainer",
    title: "Growth Retainer",
    price: "From $1,000/month",
    tagline: "Don't just know what to fix. Fix it.",
    headline: "Don't just know what to fix. Fix it.",
    description:
      "Implementation support for the recommendations from your audit — plus ongoing monitoring, optimization, and AI-powered analysis as new data comes in. We become your growth partner, tracking progress through shared dashboards and delivering quarterly business reviews. Published pricing by company revenue tier: $1K (to $2M), $2K (to $5M), $3.5K (to $10M), or $4.5K (to $10M+ premium).",
    whatYouGet: [
      "Implementation support for audit recommendations",
      "Monthly monitoring & optimization",
      "Ongoing AI-powered analysis as new data comes in",
      "Quarterly business review",
    ],
    cta: "Talk to Our Team →",
  },
];

function Services() {
  return (
    <>
      <section className="bg-gradient-to-br from-indigo-50 via-white to-blue-50 py-16 sm:py-24">
        <div className="mx-auto max-w-7xl px-6 text-center">
          <span className="inline-block rounded-full bg-indigo-100 px-4 py-1.5 text-sm font-medium text-indigo-700">
            Our Services
          </span>
          <h1 className="mt-6 text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl">
            Revenue Growth Services
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-600">
            From a one-time diagnostic to an ongoing growth partnership — we have an
            engagement model that fits where you are and where you want to go.
          </p>
        </div>
      </section>

      {SERVICES.map((svc, i) => (
        <section
          key={svc.id}
          className={`py-16 sm:py-20 ${i % 2 === 0 ? "bg-white" : "bg-gray-50"}`}
        >
          <div className="mx-auto max-w-7xl px-6">
            <div className="mx-auto max-w-3xl">
              <div className="flex flex-wrap items-baseline gap-3">
                <h2 className="text-3xl font-bold text-gray-900 sm:text-4xl">
                  {svc.title}
                </h2>
                <span className="rounded-full bg-indigo-100 px-3 py-1 text-sm font-medium text-indigo-700">
                  {svc.price}
                </span>
              </div>
              <p className="mt-4 text-xl text-indigo-600">{svc.tagline}</p>
              <p className="mt-4 text-base leading-relaxed text-gray-600">
                {svc.description}
              </p>

              <h3 className="mt-10 text-sm font-semibold uppercase tracking-wider text-gray-900">
                What You Get
              </h3>
              <ul className="mt-4 grid gap-3 sm:grid-cols-2">
                {svc.whatYouGet.map((item) => (
                  <li
                    key={item}
                    className="flex items-start gap-3 rounded-lg border border-gray-100 bg-white p-4 text-sm text-gray-700 shadow-sm"
                  >
                    <svg
                      className="mt-0.5 h-5 w-5 shrink-0 text-green-500"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                      />
                    </svg>
                    {item}
                  </li>
                ))}
              </ul>

              <div className="mt-10">
                <Link
                  to="/contact"
                  className="rounded-lg bg-indigo-600 px-8 py-3.5 text-base font-semibold text-white shadow-sm transition-all hover:bg-indigo-700 hover:shadow-md"
                >
                  {svc.cta}
                </Link>
              </div>
            </div>
          </div>
        </section>
      ))}

      {/* FAQ */}
      <section className="bg-gray-50 py-16 sm:py-20">
        <div className="mx-auto max-w-3xl px-6">
          <h2 className="text-center text-3xl font-bold text-gray-900">
            Frequently Asked Questions
          </h2>
          <div className="mt-12 space-y-8">
            {[
              {
                q: "What kind of data do you need for the audit?",
                a: "We typically need access to CRM data (deals, pipeline, win/loss), billing/invoicing records, marketing analytics (ad spend, channel performance), and customer feedback (surveys, support tickets). The more data we have, the sharper our analysis. We use secure, read-only integrations wherever possible.",
              },
              {
                q: "How long does the Discovery Audit take?",
                a: "Most audits complete in 2–3 weeks. The timeline depends on data accessibility — if your systems are well-organized and we can integrate quickly, we can move faster.",
              },
              {
                q: "What if I don't have clean data?",
                a: "That's more common than you'd think — and we're built for it. Our AI engine is designed to work with real-world, imperfect data. We'll flag gaps and help you clean up what matters.",
              },
              {
                q: "Can I start with just the audit?",
                a: "Absolutely. Many clients start with a Discovery Audit to validate the value before committing to a retainer. The audit stands on its own — you'll get a complete growth plan you can execute yourself or with our help.",
              },
              {
                q: "How do you measure revenue impact?",
                a: "We establish clear baselines before starting any engagement. For one-time audits, we estimate ROI for each recommendation. For retainers, we track actual revenue changes against those baselines. Performance bonus clients get third-party verification options.",
              },
              {
                q: "How much does the retainer cost?",
                a: <>Retainer pricing is published by company revenue tier: <strong>$1,000/month</strong> ($500K–$2M), <strong>$2,000/month</strong> ($2M–$5M), <strong>$3,500/month</strong> ($5M–$10M), or <strong>$4,500/month</strong> ($7.5M–$10M premium). See our <Link to="/pricing" className="text-indigo-600 underline hover:text-indigo-700">full pricing model</Link> for details.</>,
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
            Not Sure Which Service Fits?
          </h2>
          <p className="mt-4 text-lg text-indigo-200">
            Book a free 30-minute call. We'll listen to your situation and recommend
            the right approach — no pressure, no hard sell.
          </p>
          <div className="mt-8">
            <Link
              to="/contact"
              className="inline-block rounded-lg bg-white px-8 py-3.5 text-base font-semibold text-indigo-700 shadow-lg transition-all hover:bg-indigo-50 hover:shadow-xl"
            >
              Book Your Free Call
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}