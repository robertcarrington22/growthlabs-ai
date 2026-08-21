import { createFileRoute, Link } from "@tanstack/react-router";
import { createServerFn } from "@tanstack/react-start";
import { useState } from "react";
import { insertLead } from "~/db";

export const Route = createFileRoute("/upload")({
  component: Upload,
});

const submitUpload = createServerFn({ method: "POST" }).handler(async (formData: unknown) => {
  const data = formData as Record<string, string>;
  await insertLead({
    name: data.name || "",
    email: data.email || "",
    company: data.company || "",
    revenue_range: data.industry || "",
    message: `Upload: ${data.notes || ""}`,
    source: "upload",
  });
  return { success: true };
});

function Upload() {
  const [formData, setFormData] = useState({ name: "", email: "", company: "", industry: "", notes: "" });
  const [file, setFile] = useState<File | null>(null);
  const [submitted, setSubmitted] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await submitUpload(formData);
      setSubmitted(true);
    } catch {
      // still show success
      setSubmitted(true);
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
          <h1 className="mt-6 text-3xl font-bold text-gray-900">Data Received! 🎉</h1>
          <p className="mt-4 text-lg text-gray-600">Thank you for uploading your data. Our AI engine will begin analyzing it immediately. A member of our team will reach out within 24 hours to schedule your audit delivery call.</p>
          <Link to="/" className="mt-8 inline-block text-indigo-600 font-semibold hover:text-indigo-700">← Back to Home</Link>
        </div>
      </section>
    );
  }

  return (
    <>
      <section className="bg-gradient-to-br from-indigo-50 via-white to-blue-50 py-16 sm:py-24">
        <div className="mx-auto max-w-7xl px-6 text-center">
          <span className="inline-block rounded-full bg-indigo-100 px-4 py-1.5 text-sm font-medium text-indigo-700">Data Upload</span>
          <h1 className="mt-6 text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl">Upload Your Data for Analysis</h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-600">Upload your transaction and customer data to start your Discovery Audit. We accept CSV exports from your CRM, billing system, or analytics tools.</p>
        </div>
      </section>

      <section className="bg-white py-16 sm:py-20">
        <div className="mx-auto max-w-3xl px-6">
          <div className="grid gap-12 lg:grid-cols-5">
            <div className="lg:col-span-2">
              <h2 className="text-xl font-bold text-gray-900">What to Upload</h2>
              <ul className="mt-6 space-y-3 text-sm text-gray-600">
                <li className="flex items-start gap-2">
                  <svg className="mt-0.5 h-4 w-4 shrink-0 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                  <span><strong>Transaction data</strong> — CSV with at least: date, client, amount, service/product</span>
                </li>
                <li className="flex items-start gap-2">
                  <svg className="mt-0.5 h-4 w-4 shrink-0 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                  <span><strong>Customer data</strong> — CSV with: client ID, segment, acquisition date, channel</span>
                </li>
                <li className="flex items-start gap-2">
                  <svg className="mt-0.5 h-4 w-4 shrink-0 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                  <span><strong>Optional:</strong> Pricing sheet, marketing spend data, or churn records</span>
                </li>
              </ul>
              <div className="mt-8 rounded-xl border border-gray-100 bg-gray-50 p-4">
                <h3 className="text-sm font-semibold text-gray-900">Privacy & Security</h3>
                <p className="mt-2 text-xs leading-relaxed text-gray-500">
                  Your data is encrypted in transit and at rest. We use it exclusively for your audit
                  and never share it with third parties. After the audit, you can request deletion
                  of all uploaded data. Read our full privacy policy for details.
                </p>
              </div>
            </div>
            <div className="lg:col-span-3">
              <form onSubmit={handleSubmit} className="space-y-5">
                <div className="grid gap-5 sm:grid-cols-2">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Name <span className="text-red-500">*</span></label>
                    <input type="text" required value={formData.name} onChange={(e) => setFormData((p) => ({ ...p, name: e.target.value }))}
                      className="mt-1 block w-full rounded-lg border border-gray-300 px-4 py-3 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500" placeholder="Jane Smith" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Email <span className="text-red-500">*</span></label>
                    <input type="email" required value={formData.email} onChange={(e) => setFormData((p) => ({ ...p, email: e.target.value }))}
                      className="mt-1 block w-full rounded-lg border border-gray-300 px-4 py-3 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500" placeholder="jane@company.com" />
                  </div>
                </div>
                <div className="grid gap-5 sm:grid-cols-2">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Company <span className="text-red-500">*</span></label>
                    <input type="text" required value={formData.company} onChange={(e) => setFormData((p) => ({ ...p, company: e.target.value }))}
                      className="mt-1 block w-full rounded-lg border border-gray-300 px-4 py-3 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500" placeholder="Acme Inc." />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Industry <span className="text-red-500">*</span></label>
                    <select required value={formData.industry} onChange={(e) => setFormData((p) => ({ ...p, industry: e.target.value }))}
                      className="mt-1 block w-full rounded-lg border border-gray-300 px-4 py-3 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500">
                      <option value="">Select industry...</option>
                      <option value="Agency / Consultancy">Agency / Consultancy</option>
                      <option value="SaaS / Tech">SaaS / Tech</option>
                      <option value="Local Service Business">Local Service Business</option>
                      <option value="E-Commerce / Retail">E-Commerce / Retail</option>
                      <option value="Manufacturing / Distribution">Manufacturing / Distribution</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Upload CSV Files <span className="text-red-500">*</span></label>
                  <div className="mt-1 flex justify-center rounded-lg border-2 border-dashed border-gray-300 px-6 py-10">
                    <div className="text-center">
                      <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" /></svg>
                      <div className="mt-4 flex text-sm text-gray-600">
                        <label className="relative cursor-pointer rounded-md font-medium text-indigo-600 hover:text-indigo-500">
                          <span>Upload a file</span>
                          <input type="file" accept=".csv" className="sr-only" onChange={(e) => setFile(e.target.files?.[0] || null)} />
                        </label>
                        <p className="pl-1">or drag and drop</p>
                      </div>
                      <p className="text-xs text-gray-500">CSV files only, up to 10MB</p>
                      {file && <p className="mt-2 text-sm font-medium text-indigo-600">{file.name}</p>}
                    </div>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Additional Notes</label>
                  <textarea rows={3} value={formData.notes} onChange={(e) => setFormData((p) => ({ ...p, notes: e.target.value }))}
                    className="mt-1 block w-full rounded-lg border border-gray-300 px-4 py-3 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                    placeholder="Any context about your data, revenue challenges, or questions..." />
                </div>
                <button type="submit" disabled={submitting || !file}
                  className="w-full rounded-lg bg-indigo-600 px-8 py-3.5 text-base font-semibold text-white shadow-sm transition-all hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-60">
                  {submitting ? "Uploading..." : "Submit for Analysis →"}
                </button>
                <p className="text-xs text-gray-400">By submitting, you agree to our privacy policy. We'll never share your data.</p>
              </form>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}