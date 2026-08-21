import { createFileRoute, Link } from "@tanstack/react-router";

export const Route = createFileRoute("/case-studies")({
  component: CaseStudies,
});

function CaseStudies() {
  return (
    <>
      <section className="bg-gradient-to-br from-indigo-50 via-white to-blue-50 py-16 sm:py-24">
        <div className="mx-auto max-w-7xl px-6 text-center">
          <span className="inline-block rounded-full bg-indigo-100 px-4 py-1.5 text-sm font-medium text-indigo-700">
            Founding Clients
          </span>
          <h1 className="mt-6 text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl">
            Be Among Our First 10 Clients
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-600">
            We're building GrowthLabs AI with a small group of founding clients. In exchange
            for your feedback and a case study, you get a full Discovery Audit at no cost.
          </p>
        </div>
      </section>

      <section className="bg-white py-20 sm:py-28">
        <div className="mx-auto max-w-3xl px-6 text-center">
          <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-indigo-100">
            <svg className="h-10 w-10 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
          <h2 className="mt-8 text-2xl font-bold text-gray-900 sm:text-3xl">
            The Founding Client Offer
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-base leading-relaxed text-gray-600">
            We're taking 10 US-based founding clients. Your full Discovery Audit is free
            (normally $495–$995) in exchange for a case study with real numbers and a
            testimonial if you're happy with the work.
          </p>

          <div className="mt-12 grid gap-6 text-left sm:grid-cols-2">
            <div className="rounded-xl border border-gray-100 bg-gray-50 p-6">
              <h3 className="font-semibold text-gray-900">What you get</h3>
              <ul className="mt-4 space-y-2 text-sm text-gray-600">
                {[
                  "Full AI-powered Discovery Audit (normally $495–$995)",
                  "Prioritized revenue opportunities with estimated impact",
                  "Written report and strategy presentation",
                  "90-day execution roadmap",
                  "First access to our Growth Retainer when you're ready",
                ].map((item) => (
                  <li key={item} className="flex items-start gap-2">
                    <svg className="mt-0.5 h-4 w-4 shrink-0 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                    {item}
                  </li>
                ))}
              </ul>
            </div>
            <div className="rounded-xl border border-gray-100 bg-gray-50 p-6">
              <h3 className="font-semibold text-gray-900">What we need</h3>
              <ul className="mt-4 space-y-2 text-sm text-gray-600">
                {[
                  "30 minutes to share your data via screen share",
                  "Honest feedback on the audit process and findings",
                  "A case study with real numbers (anonymized if preferred)",
                  "A testimonial if you're satisfied with the results",
                  "Permission to share your results (with attribution or anonymized)",
                ].map((item) => (
                  <li key={item} className="flex items-start gap-2">
                    <svg className="mt-0.5 h-4 w-4 shrink-0 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" /></svg>
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Industry examples from research */}
      <section className="bg-gray-50 py-16 sm:py-20">
        <div className="mx-auto max-w-5xl px-6">
          <h2 className="text-center text-2xl font-bold text-gray-900 sm:text-3xl">
            What Our Methodology Targets
          </h2>
          <p className="mx-auto mt-3 max-w-2xl text-center text-sm text-gray-500">
            Based on industry research, these are the types of revenue gaps our approach
            is designed to find. Actual results will vary by client.
          </p>
          <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {[
              { metric: "5–15%", label: "Revenue typically lost to pricing mistakes", source: "McKinsey pricing studies" },
              { metric: "15–25%", label: "Annual churn typical in professional services", source: "Industry benchmarks" },
              { metric: "25–50%", label: "Revenue increase from value-based pricing shifts", source: "VeraSage Institute" },
              { metric: "3:1–10:1", label: "Typical ROI range SMBs expect from consulting", source: "Multiple SMB surveys" },
              { metric: "30–50%", label: "Churn reduction from proactive retention programs", source: "SaaS industry data" },
              { metric: "15–25%", label: "Higher LTV from referral vs. paid-acquisition customers", source: "Wharton research" },
            ].map((item) => (
              <div key={item.metric} className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
                <p className="text-2xl font-bold text-indigo-600">{item.metric}</p>
                <p className="mt-1 text-sm font-medium text-gray-900">{item.label}</p>
                <p className="mt-0.5 text-xs text-gray-400">Source: {item.source}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="bg-indigo-600 py-16 sm:py-20">
        <div className="mx-auto max-w-3xl px-6 text-center">
          <h2 className="text-3xl font-bold text-white sm:text-4xl">
            Ready to Be a Founding Client?
          </h2>
          <p className="mt-4 text-lg text-indigo-200">
            Limited to 10 companies. Your audit is free — you only invest 30 minutes of your time.
          </p>
          <div className="mt-8">
            <Link
              to="/contact"
              className="inline-block rounded-lg bg-white px-8 py-3.5 text-base font-semibold text-indigo-700 shadow-lg transition-all hover:bg-indigo-50 hover:shadow-xl"
            >
              Apply for the Founding Cohort →
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}