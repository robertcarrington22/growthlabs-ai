import { createFileRoute, Link } from "@tanstack/react-router";
import { Reveal } from "~/components/Reveal";

export const Route = createFileRoute("/")({
  component: Home,
});

const SERVICES = [
  {
    title: "Revenue Discovery Audit",
    price: "$495–$995",
    desc: "We study your sales and customer history and hand you a ranked list of the changes worth the most money — what to charge, who's about to leave, what your best customers would happily buy next. Written in plain English, walked through together. Credited toward your first retainer month.",
    cta: "Learn More",
  },
  {
    title: "Inventory Health Audit",
    price: "$495–$995",
    desc: "For retailers and online stores. We find the cash trapped in slow-moving stock, the best sellers you keep running out of, and exactly how much to reorder and when — using the same statistical methods big-box retailers rely on, sized for independent retail.",
    cta: "Learn More",
  },
  {
    title: "Growth Retainer",
    price: "From $1,000/month",
    desc: "We stay on as your growth team: help putting the recommendations to work, a fresh what-to-fix-next list every month, and simple dashboards that show whether it's working. Pricing published by company size — no mystery quotes.",
    cta: "Learn More",
  },
];

const QUESTIONS = [
  {
    title: "Am I charging enough?",
    desc: "Most owners haven't raised prices in years. We find where you're undercharging — and by how much.",
    icon: (
      <svg className="h-8 w-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v12m-3-2.818l.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.415.33M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
  },
  {
    title: "Why do customers leave?",
    desc: "Customers rarely announce they're drifting away. Your sales history shows it months in advance — we spot it in time to act.",
    icon: (
      <svg className="h-8 w-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
      </svg>
    ),
  },
  {
    title: "Which marketing actually pays?",
    desc: "You're probably spending on channels that bring the wrong customers. We show you which ones bring the keepers.",
    icon: (
      <svg className="h-8 w-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
        <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
      </svg>
    ),
  },
  {
    title: "What else would my customers buy?",
    desc: "Your happiest customers would buy more — if you offered. We find who's ready and what to offer them.",
    icon: (
      <svg className="h-8 w-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 18L9 11.25l4.306 4.307a11.95 11.95 0 015.814-5.519l2.74-1.22m0 0l-5.94-2.28m5.94 2.28l-2.28 5.941" />
      </svg>
    ),
  },
  {
    title: "How much cash is stuck on my shelves?",
    desc: "For retailers: slow stock ties up money you could be using to grow. We find it, value it, and show you how to free it.",
    icon: (
      <svg className="h-8 w-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="m21 7.5-9-5.25L3 7.5m18 0-9 5.25m9-5.25v9l-9 5.25M3 7.5l9 5.25M3 7.5v9l9 5.25m0-9v9" />
      </svg>
    ),
  },
];

const INDUSTRIES = [
  { to: "/industries/agencies", label: "Agencies & Studios" },
  { to: "/industries/saas", label: "Software & SaaS" },
  { to: "/industries/ecommerce", label: "Retail & Online Stores" },
  { to: "/industries/local-services", label: "Local Services" },
  { to: "/industries/manufacturing", label: "Makers & Distributors" },
];

function Home() {
  return (
    <>
      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-br from-indigo-50 via-white to-blue-50">
        <div className="mx-auto max-w-7xl px-6 py-20 sm:py-28 lg:py-36">
          <div className="mx-auto max-w-3xl text-center">
            <span className="animate-hero inline-block rounded-full bg-indigo-100 px-4 py-1.5 text-sm font-medium text-indigo-700">
              For owners of growing small businesses
            </span>
            <h1 className="animate-hero hero-delay-1 mt-6 text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl lg:text-6xl">
              Know exactly <span className="gradient-text">what to fix next</span> in your business.
            </h1>
            <p className="animate-hero hero-delay-2 mt-6 text-lg leading-relaxed text-gray-600 sm:text-xl">
              Big companies have whole teams studying their numbers. You have us.
              GrowthLabs AI turns the sales history you already have into a short,
              plain-English list of what will make you money — no dashboards to learn,
              no jargon to decode.
            </p>
            <div className="animate-hero hero-delay-3 mt-10 flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
              <Link
                to="/scorecard"
                className="group rounded-lg bg-indigo-600 px-8 py-3.5 text-base font-semibold text-white shadow-lg shadow-indigo-600/25 transition-all hover:bg-indigo-700 hover:shadow-xl hover:shadow-indigo-600/30"
              >
                See Where You Stand — Free{" "}
                <span className="inline-block transition-transform duration-300 group-hover:translate-x-1">→</span>
              </Link>
              <Link
                to="/how-it-works"
                className="group rounded-lg border border-gray-300 bg-white px-8 py-3.5 text-base font-semibold text-gray-700 shadow-sm transition-all hover:border-indigo-300 hover:bg-gray-50 hover:shadow-md"
              >
                How It Works{" "}
                <span className="inline-block transition-transform duration-300 group-hover:translate-x-1">→</span>
              </Link>
            </div>
            <p className="animate-hero hero-delay-4 mt-6 text-sm text-gray-400">
              5-minute scorecard · No credit card · No data science degree required
            </p>
          </div>
        </div>
        <div className="animate-float absolute -top-24 -right-24 h-96 w-96 rounded-full bg-indigo-200/40 blur-3xl" />
        <div className="animate-float-alt absolute -bottom-24 -left-24 h-96 w-96 rounded-full bg-blue-200/40 blur-3xl" />
        <div className="animate-float-alt absolute top-1/3 left-1/2 h-64 w-64 -translate-x-1/2 rounded-full bg-violet-200/30 blur-3xl" />
      </section>

      {/* The questions owners ask */}
      <section className="bg-white py-20 sm:py-28">
        <div className="mx-auto max-w-7xl px-6">
          <Reveal>
            <div className="mx-auto max-w-2xl text-center">
              <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
                The questions that keep owners up at night. <br />
                <span className="text-indigo-600">Your numbers already hold the answers.</span>
              </h2>
              <p className="mt-4 text-lg text-gray-600">
                You don't need another dashboard or a data team. You need clear answers,
                ranked by what they're worth. That's what we deliver.
              </p>
            </div>
          </Reveal>
          <div className="mt-16 grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
            {QUESTIONS.map((item, i) => (
              <Reveal key={item.title} delay={i * 80}>
                <div className="card-lift h-full rounded-xl border border-gray-100 bg-gray-50 p-6 hover:border-indigo-200">
                  {item.icon}
                  <h3 className="mt-4 text-lg font-semibold text-gray-900">{item.title}</h3>
                  <p className="mt-2 text-sm leading-relaxed text-gray-600">{item.desc}</p>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* Who we help */}
      <section className="bg-indigo-50/50 py-16 sm:py-20">
        <div className="mx-auto max-w-7xl px-6 text-center">
          <Reveal>
            <h2 className="text-2xl font-bold tracking-tight text-gray-900 sm:text-3xl">
              Built for businesses like yours
            </h2>
            <p className="mx-auto mt-3 max-w-2xl text-base text-gray-600">
              If you're doing $500K–$10M a year and decisions still come down to gut feel,
              you're exactly who we built this for.
            </p>
          </Reveal>
          <div className="mt-8 flex flex-wrap justify-center gap-3">
            {INDUSTRIES.map((ind, i) => (
              <Reveal key={ind.to} delay={i * 60} className="inline-block">
                <Link
                  to={ind.to}
                  className="inline-block rounded-full border border-indigo-200 bg-white px-5 py-2.5 text-sm font-medium text-indigo-700 transition-all duration-300 hover:-translate-y-0.5 hover:border-indigo-400 hover:bg-indigo-50 hover:shadow-md hover:shadow-indigo-100"
                >
                  {ind.label}
                </Link>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* Process: Audit → Plan → Execute */}
      <section className="bg-gray-50 py-20 sm:py-28">
        <div className="mx-auto max-w-7xl px-6">
          <Reveal>
            <div className="mx-auto max-w-2xl text-center">
              <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
                Audit → Plan → Execute
              </h2>
              <p className="mt-4 text-lg text-gray-600">
                Three steps from "not sure" to a plan you can act on. Your part takes
                about 30 minutes, total.
              </p>
            </div>
          </Reveal>
          <div className="mt-16 grid gap-8 md:grid-cols-3">
            {[
              {
                step: "01",
                phase: "Audit",
                time: "Week 1–2",
                desc: "Share your sales history — we'll do the export with you on a screen-share if you'd like. Our analysis engine studies your customers, prices, and patterns, and finds the opportunities worth the most.",
                deliverable: "Discovery Audit Report",
              },
              {
                step: "02",
                phase: "Plan",
                time: "Week 3",
                desc: "We walk you through what we found, in plain English. Together we pick the highest-impact fixes and turn them into a 90-day roadmap.",
                deliverable: "Growth Plan",
              },
              {
                step: "03",
                phase: "Execute",
                time: "Ongoing",
                desc: "We help you make the changes, then check the numbers every month: what worked, what's next, and what it was worth.",
                deliverable: "Monthly Progress Reports",
              },
            ].map((item, i) => (
              <Reveal key={item.step} delay={i * 120}>
                <div className="card-lift h-full rounded-2xl border border-gray-200 bg-white p-8 shadow-sm">
                  <span className="inline-flex h-12 w-12 items-center justify-center rounded-full bg-indigo-100 text-lg font-bold text-indigo-700">
                    {item.step}
                  </span>
                  <h3 className="mt-4 text-xl font-bold text-gray-900">{item.phase}</h3>
                  <p className="mt-1 text-sm font-medium text-indigo-600">{item.time}</p>
                  <p className="mt-3 text-sm leading-relaxed text-gray-600">{item.desc}</p>
                  <p className="mt-4 text-xs font-semibold uppercase tracking-wider text-gray-400">
                    Deliverable: {item.deliverable}
                  </p>
                </div>
              </Reveal>
            ))}
          </div>
          <div className="mt-12 text-center">
            <Link
              to="/how-it-works"
              className="group font-semibold text-indigo-600 hover:text-indigo-700"
            >
              See the full process{" "}
              <span className="inline-block transition-transform duration-300 group-hover:translate-x-1">→</span>
            </Link>
          </div>
        </div>
      </section>

      {/* Services Overview */}
      <section className="bg-white py-20 sm:py-28">
        <div className="mx-auto max-w-7xl px-6">
          <Reveal>
            <div className="mx-auto max-w-2xl text-center">
              <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
                Simple engagements, honest pricing
              </h2>
              <p className="mt-4 text-lg text-gray-600">
                Start with a one-time audit. Keep us on if it pays for itself —
                the audit fee counts toward your first month.
              </p>
            </div>
          </Reveal>
          <div className="mt-16 grid gap-8 md:grid-cols-3">
            {SERVICES.map((svc, i) => (
              <Reveal key={svc.title} delay={i * 120}>
                <div className="card-lift flex h-full flex-col rounded-2xl border border-gray-200 bg-white p-8 shadow-sm">
                  <span className="text-3xl font-bold text-indigo-600">{svc.price}</span>
                  <h3 className="mt-4 text-xl font-bold text-gray-900">{svc.title}</h3>
                  <p className="mt-3 flex-1 text-sm leading-relaxed text-gray-600">{svc.desc}</p>
                  <Link
                    to="/pricing"
                    className="group mt-8 rounded-lg bg-indigo-600 px-6 py-3 text-center text-sm font-semibold text-white shadow-sm transition-all hover:bg-indigo-700 hover:shadow-md"
                  >
                    {svc.cta}{" "}
                    <span className="inline-block transition-transform duration-300 group-hover:translate-x-1">→</span>
                  </Link>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* Founding Client Offer */}
      <section className="gradient-band relative overflow-hidden py-20 sm:py-28">
        <div className="mx-auto max-w-3xl px-6 text-center">
          <Reveal>
            <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
              Be one of our 10 founding clients
            </h2>
            <p className="mt-6 text-lg leading-relaxed text-indigo-100">
              We're new, and we'd rather earn your trust than claim it. Our first ten
              clients get the full audit free — all we ask in return is an honest case
              study when we're done. If we don't find anything worth acting on, you've
              lost nothing but half an hour.
            </p>
            <div className="mt-8">
              <Link
                to="/contact"
                className="group inline-block rounded-lg bg-white px-8 py-3.5 text-base font-semibold text-indigo-700 shadow-lg transition-all hover:-translate-y-0.5 hover:bg-indigo-50 hover:shadow-xl"
              >
                Claim a Founding Spot{" "}
                <span className="inline-block transition-transform duration-300 group-hover:translate-x-1">→</span>
              </Link>
            </div>
          </Reveal>
        </div>
        <div className="animate-float absolute -top-32 right-0 h-80 w-80 rounded-full bg-white/10 blur-3xl" />
        <div className="animate-float-alt absolute -bottom-32 left-0 h-80 w-80 rounded-full bg-white/10 blur-3xl" />
      </section>

      {/* CTA */}
      <section className="bg-white py-20 sm:py-28">
        <div className="mx-auto max-w-3xl px-6 text-center">
          <Reveal>
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
              Ready to stop guessing?
            </h2>
            <p className="mt-4 text-lg text-gray-600">
              Take the free scorecard. Five minutes, fifteen questions, and you'll know
              where your business stands — and what to look at first.
            </p>
            <div className="mt-10">
              <Link
                to="/scorecard"
                className="group inline-block rounded-lg bg-indigo-600 px-10 py-4 text-lg font-semibold text-white shadow-lg shadow-indigo-600/25 transition-all hover:-translate-y-0.5 hover:bg-indigo-700 hover:shadow-xl hover:shadow-indigo-600/30"
              >
                Take the Free Scorecard{" "}
                <span className="inline-block transition-transform duration-300 group-hover:translate-x-1">→</span>
              </Link>
            </div>
          </Reveal>
        </div>
      </section>
    </>
  );
}
