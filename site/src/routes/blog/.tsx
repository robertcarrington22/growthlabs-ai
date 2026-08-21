import { createFileRoute, Link } from "@tanstack/react-router";

export const Route = createFileRoute("/blog/$slug")({
  component: BlogPost,
});

const POSTS: Record<string, { title: string; content: string[] }> = {
  "5-hidden-revenue-leaks": {
    title: "5 Hidden Revenue Leaks Costing Your Service Business $50K+/Year",
    content: [
      `If you're running a service business — a consultancy, agency, SaaS company, or professional services firm — chances are you've felt the frustration of **inconsistent growth**. One quarter you crush it. The next, you're flat. You keep hiring, adding services, working harder. And somehow revenue doesn't move the way it should.`,
      `Here's what we've found after analyzing revenue data across dozens of businesses: **most are leaking 10–25% of their potential revenue** in predictable, fixable ways. Leaks that manual processes miss because they hide in plain sight — scattered across billing systems, CRMs, and analytics tools that don't talk to each other.`,
      `Here are the five most common revenue leaks we see — and how to plug them.`,
    ],
  },
};

const SECTIONS = [
  {
    title: "Leak #1: Pricing Inconsistency",
    body: "**The problem**: You have different pricing tiers, grandfathered plans, or discount arrangements that have accumulated over the years. Some clients pay 40% less than comparable clients for the same service. You just haven't noticed.\n\n**The cost**: 8–15% of total revenue, on average.\n\n**The fix**: Run a pricing consistency audit — compare what similar clients pay for similar services. Flag outliers. Standardize where possible. And when you raise prices, use data to justify it: \"We've been delivering X% more value than when your rate was set.\"\n\n**AI advantage**: An AI analysis can segment your client base by usage, value received, and pricing tier — then highlight every pricing anomaly in hours, not weeks.",
  },
  {
    title: "Leak #2: Hidden Churn Signals",
    body: "**The problem**: Your churn rate looks fine at the aggregate level — maybe 3–5% a month. But some segments are churning at 15%. You don't see it because you're looking at averages.\n\n**The cost**: Varies wildly, but service businesses that actively monitor segment-level churn reduce it by 30–50%.\n\n**The fix**: Track churn by cohort (industry, acquisition channel, account size, onboarding experience). A 3% average can hide a 12% churn rate among a specific customer type that you're over-investing in acquiring.\n\n**AI advantage**: AI churn prediction models flag at-risk accounts 4–8 weeks before they cancel — based on subtle usage, billing, and engagement patterns a human would never catch.",
  },
  {
    title: "Leak #3: Missed Upsell & Cross-Sell Opportunities",
    body: "**The problem**: You have clients who've been buying the same service for years. They trust you. They need more. You've never asked.\n\n**The cost**: 10–25% revenue lift from existing clients is standard for businesses that systematically pursue upsells.\n\n**The fix**: Map your services to client segments. Who's ready for the next tier? Who's using one service but clearly needs a complementary one? Build a quarterly upsell cadence.\n\n**AI advantage**: An AI engine can correlate service usage, support ticket themes, and growth patterns to recommend exactly which upsell to offer to which client — and when.",
  },
  {
    title: "Leak #4: Underperforming Acquisition Channels",
    body: "**The problem**: You're spending across LinkedIn ads, Google search, referrals, events, and content. But you don't know which channel is producing your best clients — and which is quietly burning budget.\n\n**The cost**: 20–40% of acquisition spend is wasted on low-LTV channels.\n\n**The fix**: Full-funnel attribution. Don't just track what converts. Track what converts *to high-value, retained clients*. A channel that drives cheap leads but high churn is a net negative.\n\n**AI advantage**: Multi-touch attribution models built on your actual customer data reveal the true ROI of every channel — and show you where to double down.",
  },
  {
    title: "Leak #5: Under-optimized Recurring Revenue",
    body: "**The problem**: You offer retainers, subscriptions, or recurring packages. But you're not systematically tracking expansion revenue (upsells, upgrades, add-ons) vs. contraction revenue (downgrades, churn). Net Revenue Retention (NRR) is a blind spot.\n\n**The cost**: Companies that track and optimize NRR grow 2–3x faster than those that don't.\n\n**The fix**: Measure NRR monthly. If it's below 110%, focus on expansion. If it's below 100%, you're shrinking even as you acquire new clients.\n\n**AI advantage**: Automated NRR dashboards with segment-level breakdowns show you exactly which client groups are expanding and which are contracting — so you can intervene before contraction becomes churn.",
  },
];

const slugSchema = {
  parse: (s: string) => s,
};

function BlogPost() {
  const { slug } = Route.useParams();
  const post = POSTS[slug];

  if (!post) {
    return (
      <div className="flex min-h-[50vh] flex-col items-center justify-center gap-4 px-6 text-center">
        <h1 className="text-3xl font-bold text-gray-900">Post not found</h1>
        <p className="text-gray-600">The article you're looking for doesn't exist.</p>
        <Link to="/blog" className="text-indigo-600 font-semibold hover:text-indigo-700">
          ← Back to blog
        </Link>
      </div>
    );
  }

  return (
    <>
      <article className="bg-white py-16 sm:py-24">
        <div className="mx-auto max-w-3xl px-6">
          <div className="flex items-center gap-3 text-sm text-gray-400">
            <Link to="/blog" className="text-indigo-600 hover:text-indigo-700">
              ← Blog
            </Link>
            <span>·</span>
            <span className="rounded-full bg-indigo-100 px-3 py-1 text-xs text-indigo-700">
              Revenue Optimization
            </span>
            <span>·</span>
            <span>6 min read</span>
          </div>
          <h1 className="mt-6 text-3xl font-extrabold text-gray-900 sm:text-4xl">
            {post.title}
          </h1>
          <p className="mt-4 text-base text-gray-500">July 7, 2026</p>

          <div className="mt-10 space-y-6 text-base leading-relaxed text-gray-700">
            {post.content.map((para, i) => (
              <p key={i}>{para}</p>
            ))}
          </div>

          <div className="mt-12 space-y-10">
            {SECTIONS.map((section) => (
              <div key={section.title} className="border-t border-gray-100 pt-8">
                <h2 className="text-xl font-bold text-gray-900">{section.title}</h2>
                <div className="mt-4 space-y-3 text-base leading-relaxed text-gray-700 whitespace-pre-line">
                  {section.body.split('\n\n').map((para, i) => (
                    <p key={i}>{para}</p>
                  ))}
                </div>
              </div>
            ))}
          </div>

          <div className="mt-16 rounded-xl border border-indigo-100 bg-indigo-50 p-8 text-center">
            <h3 className="text-xl font-bold text-gray-900">
              Not sure where you stand?
            </h3>
            <p className="mt-2 text-base text-gray-600">
              Take the Revenue Health Scorecard — a free, 5-minute diagnostic that scores
              your business across these five dimensions and shows you your biggest leak.
            </p>
            <Link
              to="/scorecard"
              className="mt-6 inline-block rounded-lg bg-indigo-600 px-8 py-3.5 text-base font-semibold text-white shadow-sm transition-all hover:bg-indigo-700"
            >
              Get Your Revenue Health Scorecard →
            </Link>
          </div>

          <div className="mt-12 text-center text-sm text-gray-400">
            <p>
              <em>
                About the author: GrowthLabs AI helps service businesses find hidden
                revenue using AI-powered analysis. Our Discovery Audit identifies revenue
                gaps in 2 weeks and delivers a prioritized growth plan.
              </em>
            </p>
          </div>
        </div>
      </article>
    </>
  );
}