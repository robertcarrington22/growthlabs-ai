import { createFileRoute, Link } from "@tanstack/react-router";

export const Route = createFileRoute("/industries/")({
  component: Industries,
});

const INDUSTRIES = [
  {
    id: "agencies",
    name: "Agencies & Consultancies",
    icon: "🏢",
    desc: "Digital agencies, marketing firms, management consultancies, and professional services firms losing revenue to scope creep, utilization gaps, and outdated hourly billing.",
    painPoints: ["Scope creep eating 5-15% of revenue", "Utilization rates below 70%", "Hourly billing limiting growth", "Project profitability blindspots"],
    cta: "See How We Help Agencies →",
  },
  {
    id: "saas",
    name: "SaaS & Tech",
    icon: "☁️",
    desc: "SaaS companies, B2B platforms, and tech startups struggling with pricing tiers, churn, expansion revenue, and customer acquisition cost optimization.",
    painPoints: ["NRR below 110% — you're shrinking", "Pricing tiers not optimized", "Churn predictable but unaddressed", "Expansion revenue <10% of ARR"],
    cta: "See How We Help SaaS →",
  },
  {
    id: "local-services",
    name: "Local Service Businesses",
    icon: "🏪",
    desc: "Healthcare practices, trades, hospitality, and local service providers with untapped pricing power and no systematic approach to customer retention or upselling.",
    painPoints: ["No pricing strategy — using competitor rates", "Owner capacity limits growth", "No systematic upsell program", "Seasonal revenue without smoothing"],
    cta: "See How We Help Local Services →",
  },
  {
    id: "ecommerce",
    name: "E-Commerce & Retail",
    icon: "🛒",
    desc: "Online retailers, DTC brands, and multi-channel merchants fighting margin compression, cart abandonment, and rising customer acquisition costs.",
    painPoints: ["70% cart abandonment — no recovery strategy", "CLV unknown by channel", "Price competition compressing margins", "Low repeat purchase rates"],
    cta: "See How We Help E-Commerce →",
  },
  {
    id: "manufacturing",
    name: "Manufacturing & Distribution",
    icon: "🏭",
    desc: "B2B manufacturers, distributors, and industrial service providers with complex pricing structures, customer concentration risk, and margin visibility gaps.",
    painPoints: ["True margin by product line is unknown", "Top 3 customers = 50%+ of revenue", "Volume discounts leaking margin", "Pricing not adjusted for material costs"],
    cta: "See How We Help Manufacturing →",
  },
];

function Industries() {
  return (
    <>
      <section className="bg-gradient-to-br from-indigo-50 via-white to-blue-50 py-16 sm:py-24">
        <div className="mx-auto max-w-7xl px-6 text-center">
          <span className="inline-block rounded-full bg-indigo-100 px-4 py-1.5 text-sm font-medium text-indigo-700">
            Industries
          </span>
          <h1 className="mt-6 text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl">
            Revenue Growth by Industry
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-600">
            Every industry has unique revenue dynamics. We tailor our AI-powered analysis
            to the specific patterns of your sector — uncovering gaps that generic
            consulting misses.
          </p>
        </div>
      </section>

      <section className="bg-white py-16 sm:py-24">
        <div className="mx-auto max-w-7xl px-6">
          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            {INDUSTRIES.map((ind) => (
              <Link
                key={ind.id}
                to={`/industries/${ind.id}`}
                className="group rounded-2xl border border-gray-200 bg-white p-8 shadow-sm transition-all hover:border-indigo-200 hover:shadow-lg"
              >
                <span className="text-4xl">{ind.icon}</span>
                <h2 className="mt-4 text-xl font-bold text-gray-900 group-hover:text-indigo-600 transition-colors">
                  {ind.name}
                </h2>
                <p className="mt-3 text-sm leading-relaxed text-gray-600">
                  {ind.desc}
                </p>
                <ul className="mt-6 space-y-2">
                  {ind.painPoints.map((pp) => (
                    <li key={pp} className="flex items-start gap-2 text-xs text-gray-500">
                      <svg className="mt-0.5 h-3.5 w-3.5 shrink-0 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                      {pp}
                    </li>
                  ))}
                </ul>
                <span className="mt-6 inline-block text-sm font-semibold text-indigo-600 group-hover:text-indigo-700">
                  {ind.cta}
                </span>
              </Link>
            ))}
          </div>
        </div>
      </section>

      <section className="bg-gray-50 py-16 sm:py-20">
        <div className="mx-auto max-w-3xl px-6 text-center">
          <h2 className="text-3xl font-bold text-gray-900 sm:text-4xl">
            Don't See Your Industry?
          </h2>
          <p className="mt-4 text-lg text-gray-600">
            Our AI engine works across any service business. If you have customer and
            revenue data, we can analyze it. Book a free call and we'll show you what's
            possible.
          </p>
          <div className="mt-8">
            <Link
              to="/contact"
              className="inline-block rounded-lg bg-indigo-600 px-8 py-3.5 text-base font-semibold text-white shadow-sm transition-all hover:bg-indigo-700"
            >
              Book Your Free Call
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}