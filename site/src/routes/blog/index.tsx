import { createFileRoute, Link } from "@tanstack/react-router";

export const Route = createFileRoute("/blog/")({
  component: Blog,
});

const POSTS = [
  {
    slug: "5-hidden-revenue-leaks",
    title: "5 Hidden Revenue Leaks Costing Your Service Business $50K+/Year",
    excerpt:
      "Most service businesses are unknowingly losing revenue in predictable ways. Here's how to find — and fix — the five biggest leaks.",
    date: "July 7, 2026",
    category: "Revenue Optimization",
    readTime: "6 min",
  },
];

function Blog() {
  return (
    <>
      <section className="bg-gradient-to-br from-indigo-50 via-white to-blue-50 py-16 sm:py-24">
        <div className="mx-auto max-w-7xl px-6 text-center">
          <span className="inline-block rounded-full bg-indigo-100 px-4 py-1.5 text-sm font-medium text-indigo-700">
            Blog
          </span>
          <h1 className="mt-6 text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl">
            Revenue insights for growing businesses.
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-600">
            Practical advice on pricing, churn, upsells, and revenue growth — grounded
            in data, delivered without the fluff.
          </p>
        </div>
      </section>

      <section className="bg-white py-16 sm:py-24">
        <div className="mx-auto max-w-4xl px-6">
          {POSTS.length === 0 ? (
            <div className="text-center py-20">
              <p className="text-gray-400">No posts yet. Check back soon.</p>
            </div>
          ) : (
            <div className="space-y-10">
              {POSTS.map((post) => (
                <article
                  key={post.slug}
                  className="group rounded-2xl border border-gray-100 bg-white p-8 shadow-sm transition-all hover:shadow-lg"
                >
                  <div className="flex items-center gap-3 text-xs font-medium text-gray-400">
                    <span className="rounded-full bg-indigo-100 px-3 py-1 text-indigo-700">
                      {post.category}
                    </span>
                    <span>{post.date}</span>
                    <span>·</span>
                    <span>{post.readTime} read</span>
                  </div>
                  <h2 className="mt-4 text-2xl font-bold text-gray-900 group-hover:text-indigo-600 transition-colors">
                    <Link to={`/blog/${post.slug}`}>{post.title}</Link>
                  </h2>
                  <p className="mt-3 text-base leading-relaxed text-gray-600">
                    {post.excerpt}
                  </p>
                  <Link
                    to={`/blog/${post.slug}`}
                    className="mt-4 inline-flex items-center gap-1 text-sm font-semibold text-indigo-600 hover:text-indigo-700"
                  >
                    Read article →
                  </Link>
                </article>
              ))}
            </div>
          )}
        </div>
      </section>

      <section className="bg-indigo-600 py-16 sm:py-20">
        <div className="mx-auto max-w-3xl px-6 text-center">
          <h2 className="text-3xl font-bold text-white sm:text-4xl">
            Not Sure Where You Stand?
          </h2>
          <p className="mt-4 text-lg text-indigo-200">
            Take the Revenue Health Scorecard — a free, 5-minute diagnostic that scores
            your business across 5 dimensions and shows you your biggest revenue leak.
          </p>
          <div className="mt-8">
            <Link
              to="/scorecard"
              className="inline-block rounded-lg bg-white px-8 py-3.5 text-base font-semibold text-indigo-700 shadow-lg transition-all hover:bg-indigo-50 hover:shadow-xl"
            >
              Get the Revenue Health Scorecard →
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}