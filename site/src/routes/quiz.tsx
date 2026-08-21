import { createFileRoute, Link } from "@tanstack/react-router";
import { useState } from "react";

export const Route = createFileRoute("/quiz")({
  component: Quiz,
});

const STAGES = [
  { id: "survival", name: "Survival", range: "0–25", color: "text-red-600 bg-red-50 border-red-200", desc: "You're in the early stages. Revenue is unpredictable, and you're doing everything yourself. The priority is building a data foundation and finding your first pricing gaps." },
  { id: "growth", name: "Growth", range: "26–45", color: "text-orange-600 bg-orange-50 border-orange-200", desc: "You're growing but chaotically. Some systems are emerging, but you have significant revenue leaks. A full audit will identify the biggest gaps and build your data foundation." },
  { id: "efficiency", name: "Efficiency", range: "46–65", color: "text-yellow-600 bg-yellow-50 border-yellow-200", desc: "Systems are in place but underoptimized. This is our sweet spot — you have enough data to analyze but aren't using it for decisions. Deep analysis of pricing, churn, and channels will unlock significant growth." },
  { id: "optimization", name: "Optimization", range: "66–85", color: "text-green-600 bg-green-50 border-green-200", desc: "Good systems, multiple revenue streams, some data-driven decisions. But you're leaving money on the table — fine-tuning pricing, upsells, and channel mix will get you to the next level." },
  { id: "predictability", name: "Predictability", range: "86–100", color: "text-indigo-600 bg-indigo-50 border-indigo-200", desc: "You have strong revenue operations. Our advanced optimization and fine-tuning services can help push you further, or you may be ready for enterprise-level tools." },
];

const QUESTIONS = [
  {
    q: "How would you describe your current revenue trajectory?",
    options: [
      { label: "Unpredictable — month to month is a rollercoaster", value: 1 },
      { label: "Growing, but I'm not sure why or if it's sustainable", value: 2 },
      { label: "Steady growth — systems are working but I sense gaps", value: 3 },
      { label: "Consistent growth with good visibility into drivers", value: 4 },
      { label: "Highly predictable — we forecast accurately quarter over quarter", value: 5 },
    ],
  },
  {
    q: "How do you set your prices?",
    options: [
      { label: "By instinct or matching competitors", value: 1 },
      { label: "Cost-plus — we know our costs and add margin", value: 2 },
      { label: "We have tiers, but I'm not sure they're optimized", value: 3 },
      { label: "Segment-based pricing — different prices for different client types", value: 4 },
      { label: "Value-based — prices are set by the value we deliver", value: 5 },
    ],
  },
  {
    q: "How well do you understand your customer churn?",
    options: [
      { label: "I don't track churn systematically", value: 1 },
      { label: "I know my overall churn rate but not by segment", value: 2 },
      { label: "I track churn by segment and can see trends", value: 3 },
      { label: "I have leading indicators — I can predict at-risk accounts", value: 4 },
      { label: "Churn is below 5% and I have proactive retention programs", value: 5 },
    ],
  },
  {
    q: "How do you know which marketing/sales channels are working?",
    options: [
      { label: "I don't track channel performance systematically", value: 1 },
      { label: "I know where leads come from but not which channels are profitable", value: 2 },
      { label: "I track CAC by channel but not LTV by channel", value: 3 },
      { label: "I have multi-touch attribution for most channels", value: 4 },
      { label: "Full-funnel attribution — I know LTV by channel and optimize accordingly", value: 5 },
    ],
  },
  {
    q: "How integrated are your data systems?",
    options: [
      { label: "Spreadsheets — everything is manual", value: 1 },
      { label: "Some tools connected, but data lives in silos", value: 2 },
      { label: "CRM, billing, and analytics are partially integrated", value: 3 },
      { label: "Most systems talk to each other — I can pull cross-system reports", value: 4 },
      { label: "Fully integrated — real-time dashboards across all revenue data", value: 5 },
    ],
  },
];

function Quiz() {
  const [step, setStep] = useState<"intro" | "questions" | "result">("intro");
  const [currentQ, setCurrentQ] = useState(0);
  const [answers, setAnswers] = useState<number[]>([]);

  const handleAnswer = (value: number) => {
    const newAnswers = [...answers, value];
    setAnswers(newAnswers);
    if (currentQ < QUESTIONS.length - 1) {
      setCurrentQ(currentQ + 1);
    } else {
      setStep("result");
    }
  };

  const totalScore = answers.reduce((s, v) => s + v, 0);
  const maxScore = QUESTIONS.length * 5;
  const pct = Math.round((totalScore / maxScore) * 100);

  let stage = STAGES[0];
  if (pct >= 86) stage = STAGES[4];
  else if (pct >= 66) stage = STAGES[3];
  else if (pct >= 46) stage = STAGES[2];
  else if (pct >= 26) stage = STAGES[1];

  return (
    <>
      <section className="bg-gradient-to-br from-indigo-50 via-white to-blue-50 py-16 sm:py-24">
        <div className="mx-auto max-w-3xl px-6 text-center">
          <span className="inline-block rounded-full bg-indigo-100 px-4 py-1.5 text-sm font-medium text-indigo-700">Free Diagnostic</span>
          <h1 className="mt-6 text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl">What Revenue Health Stage Are You In?</h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-600">5 quick questions to identify your stage — and what to do next.</p>
        </div>
      </section>

      {step === "intro" && (
        <section className="bg-white py-16 sm:py-20">
          <div className="mx-auto max-w-xl px-6 text-center">
            <p className="text-gray-600">This quiz maps your business to the 5-stage Revenue Health Maturity Model. It takes 2 minutes.</p>
            <div className="mt-8 grid grid-cols-5 gap-2">
              {["Survival", "Growth", "Efficiency", "Optimization", "Predictability"].map((s, i) => (
                <div key={s} className="rounded-lg bg-gray-100 p-2 text-center">
                  <div className="text-lg font-bold text-gray-400">{i + 1}</div>
                  <div className="text-[10px] font-medium text-gray-500">{s}</div>
                </div>
              ))}
            </div>
            <button onClick={() => setStep("questions")} className="mt-10 rounded-lg bg-indigo-600 px-10 py-4 text-lg font-semibold text-white shadow-sm hover:bg-indigo-700">
              Start the Quiz →
            </button>
          </div>
        </section>
      )}

      {step === "questions" && (
        <section className="bg-white py-16 sm:py-20">
          <div className="mx-auto max-w-xl px-6">
            <div className="mb-8">
              <div className="flex items-center justify-between text-sm text-gray-500 mb-2">
                <span>Question {currentQ + 1} of {QUESTIONS.length}</span>
                <span>{Math.round((currentQ / QUESTIONS.length) * 100)}%</span>
              </div>
              <div className="h-2 rounded-full bg-gray-100 overflow-hidden">
                <div className="h-full rounded-full bg-indigo-600 transition-all duration-300" style={{ width: `${(currentQ / QUESTIONS.length) * 100}%` }} />
              </div>
            </div>
            <h2 className="text-xl font-bold text-gray-900">{QUESTIONS[currentQ].q}</h2>
            <div className="mt-8 space-y-3">
              {QUESTIONS[currentQ].options.map((opt) => (
                <button key={opt.label} onClick={() => handleAnswer(opt.value)}
                  className="w-full rounded-xl border border-gray-200 bg-white p-4 text-left text-sm font-medium text-gray-700 shadow-sm transition-all hover:border-indigo-300 hover:bg-indigo-50 hover:shadow-md">
                  {opt.label}
                </button>
              ))}
            </div>
          </div>
        </section>
      )}

      {step === "result" && (
        <section className="bg-white py-16 sm:py-20">
          <div className="mx-auto max-w-xl px-6 text-center">
            <div className={`mx-auto inline-block rounded-full border-2 px-6 py-2 text-lg font-bold ${stage.color}`}>
              {stage.name}
            </div>
            <p className="mt-4 text-5xl font-extrabold text-gray-900">{pct}/100</p>
            <p className="mt-4 text-base leading-relaxed text-gray-600">{stage.desc}</p>
            <div className="mt-8 flex flex-wrap justify-center gap-4">
              <Link to="/contact" className="rounded-lg bg-indigo-600 px-8 py-3.5 text-base font-semibold text-white shadow-sm hover:bg-indigo-700">
                {pct < 66 ? "Get Your Discovery Audit →" : "Book a Free Consult →"}
              </Link>
              <Link to="/scorecard" className="rounded-lg border border-gray-300 bg-white px-8 py-3.5 text-base font-semibold text-gray-700 hover:bg-gray-50">
                Full Revenue Health Scorecard →
              </Link>
            </div>
          </div>
        </section>
      )}
    </>
  );
}