import { createFileRoute, Link } from "@tanstack/react-router";
import { createServerFn } from "@tanstack/react-start";
import { useState } from "react";
import { insertLead } from "~/db";

export const Route = createFileRoute("/scorecard")({
  component: Scorecard,
});

const submitScorecard = createServerFn({ method: "POST" }).handler(
  async (formData: unknown) => {
    const data = formData as Record<string, string>;
    await insertLead({
      name: data.name || "",
      email: data.email || "",
      company: data.company || "",
      revenue_range: data.revenue || "",
      message: data.answers || "",
      score: data.score || "",
      source: "scorecard",
    });
    return { success: true };
  }
);

interface Question {
  id: string;
  dimension: string;
  text: string;
  options: { label: string; value: number }[];
}

const QUESTIONS: Question[] = [
  // Dimension 1: Pricing Health (20 pts)
  { id: "p1", dimension: "Pricing Health", text: "When did you last conduct a pricing review?", options: [
    { label: "Within the last 6 months", value: 4 },
    { label: "6–12 months ago", value: 2 },
    { label: "More than 12 months ago", value: 0 },
  ]},
  { id: "p2", dimension: "Pricing Health", text: "How many distinct pricing tiers or plans do you have?", options: [
    { label: "2–4 tiers", value: 3 },
    { label: "1 tier", value: 4 },
    { label: "5+ tiers", value: 1 },
    { label: "I don't know", value: 0 },
  ]},
  { id: "p3", dimension: "Pricing Health", text: "Do you know what % of your clients are on discounted or grandfathered rates?", options: [
    { label: "Yes", value: 4 },
    { label: "No", value: 0 },
  ]},
  // Dimension 2: Churn Risk (20 pts)
  { id: "c1", dimension: "Churn Risk", text: "What is your monthly churn rate?", options: [
    { label: "Less than 2%", value: 4 },
    { label: "2–5%", value: 2 },
    { label: "More than 5%", value: 0 },
    { label: "I don't know", value: 1 },
  ]},
  { id: "c2", dimension: "Churn Risk", text: "Do you track churn by client segment?", options: [
    { label: "Yes", value: 4 },
    { label: "Partially", value: 2 },
    { label: "No", value: 0 },
  ]},
  { id: "c3", dimension: "Churn Risk", text: "What's your average client lifetime (months)?", options: [
    { label: "More than 24 months", value: 4 },
    { label: "12–24 months", value: 2 },
    { label: "Less than 12 months", value: 0 },
  ]},
  // Dimension 3: Upsell/Expansion (20 pts)
  { id: "u1", dimension: "Upsell & Expansion", text: "Do you have a systematic upsell program?", options: [
    { label: "Yes, a formal program", value: 5 },
    { label: "Occasionally, but not systematic", value: 2 },
    { label: "No", value: 0 },
  ]},
  { id: "u2", dimension: "Upsell & Expansion", text: "What is your Net Revenue Retention (NRR) rate?", options: [
    { label: "More than 110%", value: 5 },
    { label: "100–110%", value: 3 },
    { label: "Less than 100%", value: 1 },
    { label: "I don't know", value: 1 },
  ]},
  { id: "u3", dimension: "Upsell & Expansion", text: "How many of your clients buy more than one service?", options: [
    { label: "More than 60%", value: 5 },
    { label: "30–60%", value: 3 },
    { label: "Less than 30%", value: 1 },
  ]},
  // Dimension 4: Channel Effectiveness (20 pts)
  { id: "ch1", dimension: "Channel Effectiveness", text: "Do you know your CAC by acquisition channel?", options: [
    { label: "Yes, for all channels", value: 5 },
    { label: "For some channels", value: 3 },
    { label: "No", value: 0 },
  ]},
  { id: "ch2", dimension: "Channel Effectiveness", text: "Do you track LTV by acquisition channel?", options: [
    { label: "Yes", value: 5 },
    { label: "No", value: 0 },
  ]},
  { id: "ch3", dimension: "Channel Effectiveness", text: "How many channels drive predictable, profitable growth?", options: [
    { label: "3 or more", value: 5 },
    { label: "1–2", value: 3 },
    { label: "None", value: 1 },
  ]},
  // Dimension 5: Data Maturity (20 pts)
  { id: "d1", dimension: "Data Maturity", text: "How integrated are your CRM, billing, and analytics tools?", options: [
    { label: "Fully integrated", value: 5 },
    { label: "Partially integrated", value: 3 },
    { label: "Not at all integrated", value: 0 },
  ]},
  { id: "d2", dimension: "Data Maturity", text: "How often do you review revenue data outside of standard monthly reports?", options: [
    { label: "Weekly", value: 5 },
    { label: "Monthly", value: 3 },
    { label: "Quarterly or less", value: 1 },
  ]},
  { id: "d3", dimension: "Data Maturity", text: "Do you currently use any AI/ML tools for revenue analysis?", options: [
    { label: "Yes", value: 5 },
    { label: "No", value: 0 },
  ]},
];

const DIMENSION_NAMES = ["Pricing Health", "Churn Risk", "Upsell & Expansion", "Channel Effectiveness", "Data Maturity"];

function getRecommendation(score: number): { tier: string; color: string; description: string } {
  if (score >= 80) return { tier: "Revenue Healthy", color: "text-green-600 bg-green-50 border-green-200", description: "You're in great shape! We have fine-tuning recommendations to optimize further." };
  if (score >= 60) return { tier: "Moderate Gaps", color: "text-yellow-600 bg-yellow-50 border-yellow-200", description: "2–3 high-impact opportunities to pursue. A focused effort can move the needle significantly." };
  if (score >= 40) return { tier: "Significant Leaks", color: "text-orange-600 bg-orange-50 border-orange-200", description: "Priority audit recommended. Our Discovery Audit can identify and quantify the biggest gaps." };
  return { tier: "Critical", color: "text-red-600 bg-red-50 border-red-200", description: "Full revenue transformation needed. Let's start with a Discovery Audit to build your roadmap." };
}

const MATURITY_STAGES = [
  { name: "Predictability", minScore: 80, icon: "🔮", desc: "Data-driven revenue operations. Fine-tuning for maximum efficiency." },
  { name: "Optimization", minScore: 60, icon: "📈", desc: "Good systems with optimization opportunities. Upsells and channel mix are the next frontier." },
  { name: "Efficiency", minScore: 40, icon: "⚙️", desc: "Systems in place but underoptimized. This is our sweet spot — deep analysis will unlock significant gains." },
  { name: "Growth", minScore: 20, icon: "🌱", desc: "Growing but chaotically. Need to build data foundation and fix the biggest leaks first." },
  { name: "Survival", minScore: 0, icon: "🔥", desc: "Early stage. Revenue is unpredictable. Need to establish basic pricing frameworks and data tracking." },
];

function getMaturityStage(score: number) {
  return MATURITY_STAGES.find((s) => score >= s.minScore) || MATURITY_STAGES[MATURITY_STAGES.length - 1];
}

function Scorecard() {
  const [step, setStep] = useState<"form" | "questions" | "results">("form");
  const [leadInfo, setLeadInfo] = useState({ name: "", email: "", company: "", revenue: "" });
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [submitting, setSubmitting] = useState(false);

  const currentQuestionIndex = Object.keys(answers).length;
  const totalQuestions = QUESTIONS.length;
  const allAnswered = currentQuestionIndex >= totalQuestions;

  const handleAnswer = (qId: string, value: number) => {
    setAnswers((prev) => ({ ...prev, [qId]: value }));
  };

  const handleSubmitForm = async () => {
    setSubmitting(true);
    const totalScore = Object.values(answers).reduce((sum, v) => sum + v, 0);
    try {
      await submitScorecard({ ...leadInfo, answers: JSON.stringify(answers), score: String(totalScore) });
      setStep("results");
    } catch {
      setStep("results");
    } finally {
      setSubmitting(false);
    }
  };

  // Results
  const totalScore = Object.values(answers).reduce((sum, v) => sum + v, 0);
  const rec = getRecommendation(totalScore);

  const dimensionScores = DIMENSION_NAMES.map((name) => {
    const dimQuestions = QUESTIONS.filter((q) => q.dimension === name);
    const score = dimQuestions.reduce((sum, q) => sum + (answers[q.id] || 0), 0);
    const max = dimQuestions.reduce((sum, q) => sum + Math.max(...q.options.map((o) => o.value)), 0);
    return { name, score, max, pct: Math.round((score / max) * 100) };
  });

  if (step === "results") {
    return (
      <>
        <section className="bg-gradient-to-br from-indigo-50 via-white to-blue-50 py-16 sm:py-24">
          <div className="mx-auto max-w-3xl px-6 text-center">
            <div className={`mx-auto inline-block rounded-full border-2 px-6 py-2 text-lg font-bold ${rec.color}`}>
              {rec.tier}
            </div>
            <h1 className="mt-6 text-5xl font-extrabold text-gray-900">{totalScore}/100</h1>
            <p className="mt-4 text-lg text-gray-600">{rec.description}</p>
          </div>
        </section>

        <section className="bg-white py-16">
          <div className="mx-auto max-w-3xl px-6">
            <h2 className="text-2xl font-bold text-gray-900">Your Dimension Scores</h2>
            <div className="mt-8 space-y-6">
              {dimensionScores.map((dim) => (
                <div key={dim.name}>
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-medium text-gray-900">{dim.name}</span>
                    <span className="text-sm text-gray-500">{dim.score}/{dim.max}</span>
                  </div>
                  <div className="h-3 rounded-full bg-gray-100 overflow-hidden">
                    <div
                      className="h-full rounded-full bg-indigo-600 transition-all duration-700"
                      style={{ width: `${dim.pct}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>

            {/* Maturity Stage */}
            <div className="mt-12 rounded-xl border border-indigo-100 bg-indigo-50 p-6">
              <h3 className="text-lg font-bold text-gray-900">Your Revenue Health Stage</h3>
              <div className="mt-4 flex items-center gap-4">
                <span className="text-4xl">{getMaturityStage(totalScore).icon}</span>
                <div>
                  <p className="text-xl font-bold text-indigo-700">{getMaturityStage(totalScore).name}</p>
                  <p className="text-sm text-gray-600">{getMaturityStage(totalScore).desc}</p>
                </div>
              </div>
              <div className="mt-4 flex gap-2">
                {MATURITY_STAGES.map((s) => (
                  <div key={s.name} className={`flex-1 h-2 rounded-full ${totalScore >= s.minScore ? 'bg-indigo-600' : 'bg-gray-200'}`} />
                ))}
              </div>
              <div className="mt-1 flex justify-between text-[10px] text-gray-400">
                {MATURITY_STAGES.map((s) => <span key={s.name}>{s.name}</span>).reverse()}
              </div>
            </div>

            <div className="mt-12 rounded-xl border border-indigo-100 bg-indigo-50 p-8 text-center">
              <h3 className="text-xl font-bold text-gray-900">Want a deeper analysis?</h3>
              <p className="mt-2 text-gray-600">
                Your scorecard gives you the headlines. Our Discovery Audit gives you the
                full picture — every revenue gap, quantified and prioritized.
              </p>
              <Link
                to="/contact"
                className="mt-6 inline-block rounded-lg bg-indigo-600 px-8 py-3.5 text-base font-semibold text-white shadow-sm transition-all hover:bg-indigo-700"
              >
                Book a Free 15-Minute Call →
              </Link>
            </div>
          </div>
        </section>
      </>
    );
  }

  if (step === "questions") {
    const currentQ = QUESTIONS[currentQuestionIndex];

    if (allAnswered) {
      return (
        <section className="bg-white py-16 sm:py-24">
          <div className="mx-auto max-w-xl px-6 text-center">
            <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-green-100">
              <svg className="h-8 w-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h2 className="mt-6 text-2xl font-bold text-gray-900">All questions answered!</h2>
            <p className="mt-3 text-gray-600">
              We've scored your {totalQuestions} answers. Ready to see your results?
            </p>
            <button
              onClick={handleSubmitForm}
              disabled={submitting}
              className="mt-8 rounded-lg bg-indigo-600 px-10 py-4 text-lg font-semibold text-white shadow-sm transition-all hover:bg-indigo-700 disabled:opacity-60"
            >
              {submitting ? "Calculating..." : "Get My Score →"}
            </button>
          </div>
        </section>
      );
    }

    return (
      <section className="bg-white py-16 sm:py-24">
        <div className="mx-auto max-w-xl px-6">
          {/* Progress */}
          <div className="mb-8">
            <div className="flex items-center justify-between text-sm text-gray-500 mb-2">
              <span>Question {currentQuestionIndex + 1} of {totalQuestions}</span>
              <span>{Math.round((currentQuestionIndex / totalQuestions) * 100)}%</span>
            </div>
            <div className="h-2 rounded-full bg-gray-100 overflow-hidden">
              <div
                className="h-full rounded-full bg-indigo-600 transition-all duration-300"
                style={{ width: `${(currentQuestionIndex / totalQuestions) * 100}%` }}
              />
            </div>
          </div>

          <span className="text-xs font-semibold uppercase tracking-wider text-indigo-600">
            {currentQ.dimension}
          </span>
          <h2 className="mt-2 text-xl font-bold text-gray-900">{currentQ.text}</h2>

          <div className="mt-8 space-y-3">
            {currentQ.options.map((opt) => (
              <button
                key={opt.label}
                onClick={() => handleAnswer(currentQ.id, opt.value)}
                className="w-full rounded-xl border border-gray-200 bg-white p-4 text-left text-sm font-medium text-gray-700 shadow-sm transition-all hover:border-indigo-300 hover:bg-indigo-50 hover:shadow-md"
              >
                {opt.label}
              </button>
            ))}
          </div>
        </div>
      </section>
    );
  }

  // Form step
  return (
    <>
      <section className="bg-gradient-to-br from-indigo-50 via-white to-blue-50 py-16 sm:py-24">
        <div className="mx-auto max-w-3xl px-6 text-center">
          <span className="inline-block rounded-full bg-indigo-100 px-4 py-1.5 text-sm font-medium text-indigo-700">
            Free Diagnostic
          </span>
          <h1 className="mt-6 text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl">
            How Healthy Is Your Revenue?
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-600">
            Find out in 5 minutes. Get your personalized Revenue Health Score — and a
            clear, data-backed picture of where your business is leaving money on the table.
          </p>
        </div>
      </section>

      <section className="bg-white py-16 sm:py-20">
        <div className="mx-auto max-w-3xl px-6">
          <div className="grid gap-12 lg:grid-cols-5">
            <div className="lg:col-span-2">
              <h2 className="text-2xl font-bold text-gray-900">What You'll Get</h2>
              <ul className="mt-6 space-y-4">
                {[
                  "5-minute self-assessment",
                  "Score across pricing, churn, upsell, channels & data maturity",
                  "Personalized priority list of revenue gaps",
                  "Benchmark your business against peers",
                  "No commitment, no sales pitch (until you want one)",
                ].map((item) => (
                  <li key={item} className="flex items-start gap-3 text-sm text-gray-700">
                    <svg className="mt-0.5 h-5 w-5 shrink-0 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    {item}
                  </li>
                ))}
              </ul>
              <p className="mt-8 text-xs text-gray-400">
                Join 50+ service businesses that have used our Revenue Health Scorecard
                to uncover hidden growth.
              </p>
            </div>
            <div className="lg:col-span-3">
              <form onSubmit={(e) => { e.preventDefault(); setStep("questions"); }} className="space-y-5">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Name <span className="text-red-500">*</span></label>
                  <input type="text" required value={leadInfo.name} onChange={(e) => setLeadInfo((p) => ({ ...p, name: e.target.value }))}
                    className="mt-1 block w-full rounded-lg border border-gray-300 px-4 py-3 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500" placeholder="Jane Smith" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Email <span className="text-red-500">*</span></label>
                  <input type="email" required value={leadInfo.email} onChange={(e) => setLeadInfo((p) => ({ ...p, email: e.target.value }))}
                    className="mt-1 block w-full rounded-lg border border-gray-300 px-4 py-3 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500" placeholder="jane@company.com" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Company <span className="text-red-500">*</span></label>
                  <input type="text" required value={leadInfo.company} onChange={(e) => setLeadInfo((p) => ({ ...p, company: e.target.value }))}
                    className="mt-1 block w-full rounded-lg border border-gray-300 px-4 py-3 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500" placeholder="Acme Inc." />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Revenue Range</label>
                  <select value={leadInfo.revenue} onChange={(e) => setLeadInfo((p) => ({ ...p, revenue: e.target.value }))}
                    className="mt-1 block w-full rounded-lg border border-gray-300 px-4 py-3 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500">
                    <option value="">Select...</option>
                    <option value="$500K–$2M">$500K–$2M</option>
                    <option value="$2M–$5M">$2M–$5M</option>
                    <option value="$5M–$10M">$5M–$10M</option>
                    <option value="$10M+">$10M+</option>
                  </select>
                </div>
                <button type="submit" className="w-full rounded-lg bg-indigo-600 px-8 py-3.5 text-base font-semibold text-white shadow-sm transition-all hover:bg-indigo-700 hover:shadow-md">
                  Get My Score →
                </button>
                <p className="text-xs text-gray-400">We'll never share your information. Response time is typically within 24 hours.</p>
              </form>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}