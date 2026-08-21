import { createFileRoute, Link } from "@tanstack/react-router";
import { Reveal } from "~/components/Reveal";

export const Route = createFileRoute("/about")({
  component: About,
});

const WHY = [
  {
    title: "Answers, not dashboards",
    desc: "We don't hand you software and wish you luck. You get a short, ranked list of what to fix and what each fix is worth — with the arithmetic shown, so you can check our work.",
    icon: (
      <svg className="h-8 w-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
    ),
  },
  {
    title: "A partner, not a report",
    desc: "The analysis is where we start, not where we stop. We help you put the changes in place, then check the numbers with you every month: what worked, what's next.",
    icon: (
      <svg className="h-8 w-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 2.772m0 0a3 3 0 00-4.681 2.72 8.986 8.986 0 003.74.477m.94-3.197a5.971 5.971 0 00-.94 3.197M15 6.75a3 3 0 11-6 0 3 3 0 016 0zm6 3a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0zm-13.5 0a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0z" />
      </svg>
    ),
  },
  {
    title: "Priced for small business",
    desc: "Audits from $495, retainers published by company size, and the audit fee credits toward your first month. No hourly meters, no mystery quotes, no six-figure engagements.",
    icon: (
      <svg className="h-8 w-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
  },
];

function About() {
  return (
    <>
      <section className="relative overflow-hidden bg-gradient-to-br from-indigo-50 via-white to-blue-50 py-16 sm:py-24">
        <div className="mx-auto max-w-7xl px-6 text-center">
          <span className="animate-hero inline-block rounded-full bg-indigo-100 px-4 py-1.5 text-sm font-medium text-indigo-700">
            Our Mission
          </span>
          <h1 className="animate-hero hero-delay-1 mt-6 text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl">
            Every small business deserves the clarity<br />
            <span className="gradient-text">big companies take for granted.</span>
          </h1>
        </div>
        <div className="animate-float absolute -top-24 -right-24 h-80 w-80 rounded-full bg-indigo-200/40 blur-3xl" />
        <div className="animate-float-alt absolute -bottom-24 -left-24 h-80 w-80 rounded-full bg-blue-200/40 blur-3xl" />
      </section>

      <section className="bg-white py-16 sm:py-20">
        <div className="mx-auto max-w-3xl px-6">
          <h2 className="text-2xl font-bold text-gray-900 sm:text-3xl">Why we exist</h2>
          <p className="mt-6 text-base leading-relaxed text-gray-600">
            A Fortune 500 company has entire floors of analysts telling it what to charge,
            which customers are drifting, and where its cash is stuck. The twelve-person
            agency, the two-location shop, the growing software company? The owner does
            all of that alone — usually at 11pm, usually on gut feel.
          </p>
          <p className="mt-4 text-base leading-relaxed text-gray-600">
            That never sat right with us. The answers owners need are already sitting in
            the sales history they've been collecting for years — nobody's ever looked
            properly. GrowthLabs AI exists to look properly, at a price a small business
            can actually pay, and to explain what we find the way a trusted friend would:
            in plain English, ranked by what it's worth to you.
          </p>
          <p className="mt-4 text-base leading-relaxed text-gray-600">
            You're good at what you do. Our job is to make sure the business side is
            just as good — so growth stops being a guessing game.
          </p>
        </div>
      </section>

      <section className="bg-gray-50 py-16 sm:py-20">
        <div className="mx-auto max-w-7xl px-6">
          <h2 className="text-center text-2xl font-bold text-gray-900 sm:text-3xl">
            How we're different
          </h2>
          <div className="mt-12 grid gap-8 md:grid-cols-3">
            {WHY.map((item, i) => (
              <Reveal key={item.title} delay={i * 120}>
                <div className="card-lift h-full rounded-xl border border-gray-200 bg-white p-8 shadow-sm">
                  {item.icon}
                  <h3 className="mt-4 text-lg font-semibold text-gray-900">{item.title}</h3>
                  <p className="mt-3 text-sm leading-relaxed text-gray-600">{item.desc}</p>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      <section className="bg-white py-16 sm:py-20">
        <div className="mx-auto max-w-3xl px-6 text-center">
          <h2 className="text-2xl font-bold text-gray-900 sm:text-3xl">
            Curious what we'd find in your business?
          </h2>
          <p className="mt-4 text-lg text-gray-600">
            Start with the free five-minute scorecard — you'll get an honest read on
            where you stand, whether or not we ever work together.
          </p>
          <div className="mt-8">
            <Link to="/scorecard" className="inline-block rounded-lg bg-indigo-600 px-8 py-3.5 text-base font-semibold text-white shadow-lg transition-all hover:bg-indigo-700 hover:shadow-xl">
              Take the Free Scorecard →
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}
