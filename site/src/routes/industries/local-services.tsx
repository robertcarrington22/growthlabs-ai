import { createFileRoute, Link } from "@tanstack/react-router";

export const Route = createFileRoute("/industries/local-services")({
  component: LocalServices,
});

function LocalServices() {
  return (
    <>
      <section className="bg-gradient-to-br from-indigo-50 via-white to-blue-50 py-16 sm:py-24">
        <div className="mx-auto max-w-7xl px-6 text-center">
          <span className="inline-block rounded-full bg-indigo-100 px-4 py-1.5 text-sm font-medium text-indigo-700">
            Local Service Businesses
          </span>
          <h1 className="mt-6 text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl">
            Unlock the Revenue in Your Existing Clientele
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-600">
            Healthcare practices, trades, hospitality, and local services have untapped pricing power. You don't need more customers — you need the right pricing and retention strategy.
          </p>
        </div>
      </section>

      <section className="bg-white py-16 sm:py-20">
        <div className="mx-auto max-w-5xl px-6">
          <div className="grid gap-12 lg:grid-cols-2">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">The Capacity Trap</h2>
              <p className="mt-4 text-base leading-relaxed text-gray-600">
                Your growth is capped by your own hours. You can't clone yourself. But you can raise your prices, increase repeat visits, and build systematic upsell programs that don't require more of your time.
              </p>
              <p className="mt-3 text-base leading-relaxed text-gray-600">
                Most local service businesses compete on price because they don't know their true cost-to-serve, customer lifetime value, or willingness-to-pay. Our AI audit reveals where you have pricing power you didn't know you had.
              </p>
              <div className="mt-8 space-y-4 rounded-xl border border-gray-100 bg-gray-50 p-6">
                <h3 className="font-semibold text-gray-900">Common Revenue Leaks We Find</h3>
                <ul className="space-y-3">
                  {[
                    { label: "Pricing by Instinct", desc: "Using competitor rates instead of value-based pricing" },
                    { label: "No Repeat Strategy", desc: "25-40% annual churn without any retention program" },
                    { label: "Zero Upsell", desc: "No systematic cross-sell or upgrade program for existing clients" },
                    { label: "Seasonal Revenue", desc: "No smoothing mechanisms for predictable cash flow" },
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
              <h3 className="text-xl font-bold">Premium Positioning Works</h3>
              <p className="mt-3 text-sm leading-relaxed text-indigo-100">
                The most profitable local service businesses don't compete on price. They
                compete on reliability, quality, and guaranteed outcomes. A move from
                competitive undercutting to premium positioning typically yields
                <strong> 25% revenue increases and 50% margin improvements</strong>.
              </p>
              <p className="mt-3 text-sm leading-relaxed text-indigo-100">
                But you need data to make that move. Our audit shows you exactly what your
                services are worth and who will pay for premium delivery.
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

      <section className="bg-indigo-600 py-16 sm:py-20">
        <div className="mx-auto max-w-3xl px-6 text-center">
          <h2 className="text-3xl font-bold text-white sm:text-4xl">
            Ready to Grow Without Burning Out?
          </h2>
          <p className="mt-4 text-lg text-indigo-200">
            Start with a $100 Discovery Audit. We'll show you exactly where your pricing
            power is hiding.
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