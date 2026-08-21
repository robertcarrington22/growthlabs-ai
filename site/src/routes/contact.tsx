import { createFileRoute } from "@tanstack/react-router";
import { createServerFn } from "@tanstack/react-start";
import { useState } from "react";
import { insertLead } from "~/db";

export const Route = createFileRoute("/contact")({
  component: Contact,
});

const submitLead = createServerFn({ method: "POST" }).handler(
  async (formData: unknown) => {
    const data = formData as Record<string, string>;
    await insertLead({
      name: data.name || "",
      email: data.email || "",
      company: data.company || "",
      revenue_range: data.revenue || "",
      message: data.message || "",
      source: "contact",
    });
    return { success: true };
  }
);

const REVENUE_OPTIONS = ["$500K–$2M", "$2M–$5M", "$5M–$10M", "$10M+"];

function Contact() {
  const [formData, setFormData] = useState({ name: "", email: "", company: "", revenue: "", message: "" });
  const [submitted, setSubmitted] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError("");
    try {
      const result = await submitLead(formData);
      if (result.success) setSubmitted(true);
    } catch {
      setError("Something went wrong. Please try again or email us directly.");
    } finally {
      setSubmitting(false);
    }
  };

  if (submitted) {
    return (
      <section className="bg-gradient-to-br from-indigo-50 via-white to-blue-50 py-16 sm:py-24">
        <div className="mx-auto max-w-2xl px-6 text-center">
          <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-green-100">
            <svg className="h-10 w-10 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
          </div>
          <h1 className="mt-6 text-3xl font-bold text-gray-900 sm:text-4xl">Thank You! 🎉</h1>
          <p className="mt-4 text-lg text-gray-600">Your message has been received. A member of our team will reach out within 24 hours to schedule your free discovery call.</p>
        </div>
      </section>
    );
  }

  return (
    <>
      <section className="bg-gradient-to-br from-indigo-50 via-white to-blue-50 py-16 sm:py-24">
        <div className="mx-auto max-w-7xl px-6 text-center">
          <span className="inline-block rounded-full bg-indigo-100 px-4 py-1.5 text-sm font-medium text-indigo-700">Get Started</span>
          <h1 className="mt-6 text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl">Ready to Find Your Hidden Revenue?</h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-600">Tell us a bit about your business and we'll schedule a free 30-minute discovery call — no strings attached.</p>
        </div>
      </section>

      <section className="bg-white py-16 sm:py-20">
        <div className="mx-auto max-w-3xl px-6">
          <div className="grid gap-12 lg:grid-cols-5">
            <div className="lg:col-span-2">
              <h2 className="text-2xl font-bold text-gray-900">Get in Touch</h2>
              <p className="mt-3 text-sm leading-relaxed text-gray-600">Prefer a more direct route? We'll get back to you within 24 hours.</p>
              <div className="mt-8 space-y-4 text-sm">
                <p><strong>Email:</strong> hello@growthlabs.ai</p>
                <p><strong>Phone:</strong> +1 (800) GROWTH</p>
                <p><strong>Location:</strong> San Francisco, CA</p>
              </div>
              <div className="mt-10 rounded-xl border border-gray-100 bg-gray-50 p-6">
                <h3 className="font-semibold text-gray-900">What happens next?</h3>
                <ol className="mt-4 space-y-3 text-sm text-gray-600">
                  <li className="flex items-start gap-2"><span className="font-bold text-indigo-600">1.</span> We review your info and match you with the right growth advisor</li>
                  <li className="flex items-start gap-2"><span className="font-bold text-indigo-600">2.</span> We schedule a 30-minute discovery call at your convenience</li>
                  <li className="flex items-start gap-2"><span className="font-bold text-indigo-600">3.</span> After the call, we'll share our initial assessment and recommendations</li>
                </ol>
              </div>
            </div>
            <div className="lg:col-span-3">
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid gap-6 sm:grid-cols-2">
                  <div>
                    <label htmlFor="name" className="block text-sm font-medium text-gray-700">Full name <span className="text-red-500">*</span></label>
                    <input type="text" id="name" name="name" required value={formData.name} onChange={handleChange}
                      className="mt-1 block w-full rounded-lg border border-gray-300 px-4 py-3 text-sm shadow-sm placeholder:text-gray-400 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500" placeholder="Jane Smith" />
                  </div>
                  <div>
                    <label htmlFor="email" className="block text-sm font-medium text-gray-700">Email address <span className="text-red-500">*</span></label>
                    <input type="email" id="email" name="email" required value={formData.email} onChange={handleChange}
                      className="mt-1 block w-full rounded-lg border border-gray-300 px-4 py-3 text-sm shadow-sm placeholder:text-gray-400 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500" placeholder="jane@company.com" />
                  </div>
                </div>
                <div className="grid gap-6 sm:grid-cols-2">
                  <div>
                    <label htmlFor="company" className="block text-sm font-medium text-gray-700">Company name <span className="text-red-500">*</span></label>
                    <input type="text" id="company" name="company" required value={formData.company} onChange={handleChange}
                      className="mt-1 block w-full rounded-lg border border-gray-300 px-4 py-3 text-sm shadow-sm placeholder:text-gray-400 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500" placeholder="Acme Inc." />
                  </div>
                  <div>
                    <label htmlFor="revenue" className="block text-sm font-medium text-gray-700">Revenue Range</label>
                    <select id="revenue" name="revenue" value={formData.revenue} onChange={handleChange}
                      className="mt-1 block w-full rounded-lg border border-gray-300 px-4 py-3 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500">
                      <option value="">Select revenue range...</option>
                      {REVENUE_OPTIONS.map((opt) => (<option key={opt} value={opt}>{opt}</option>))}
                    </select>
                  </div>
                </div>
                <div>
                  <label htmlFor="message" className="block text-sm font-medium text-gray-700">What's your biggest growth challenge? <span className="text-red-500">*</span></label>
                  <textarea id="message" name="message" rows={4} required value={formData.message} onChange={handleChange}
                    className="mt-1 block w-full rounded-lg border border-gray-300 px-4 py-3 text-sm shadow-sm placeholder:text-gray-400 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                    placeholder="Tell us about your revenue, growth challenges, and what you're hoping to achieve..." />
                </div>
                {error && <div className="rounded-lg bg-red-50 p-4 text-sm text-red-700">{error}</div>}
                <button type="submit" disabled={submitting}
                  className="w-full rounded-lg bg-indigo-600 px-8 py-3.5 text-base font-semibold text-white shadow-sm transition-all hover:bg-indigo-700 hover:shadow-md disabled:cursor-not-allowed disabled:opacity-60">
                  {submitting ? "Sending..." : "Send Message"}
                </button>
                <p className="text-xs text-gray-400">By submitting, you agree to our privacy policy. We'll never share your information with third parties.</p>
              </form>
            </div>
          </div>
        </div>
      </section>

      <section className="bg-gray-50 py-16 sm:py-20">
        <div className="mx-auto max-w-3xl px-6 text-center">
          <h2 className="text-2xl font-bold text-gray-900 sm:text-3xl">Prefer to Start with Self-Service?</h2>
          <p className="mt-4 text-base text-gray-600">Take our free Revenue Health Scorecard first.</p>
          <div className="mt-8 flex flex-wrap justify-center gap-4">
            <a href="/scorecard" className="rounded-lg bg-indigo-600 px-6 py-3 font-semibold text-white transition-all hover:bg-indigo-700">Take the Scorecard →</a>
            <a href="/services" className="rounded-lg border border-gray-300 bg-white px-6 py-3 font-semibold text-gray-700 transition-all hover:bg-gray-50">View Services</a>
          </div>
        </div>
      </section>
    </>
  );
}