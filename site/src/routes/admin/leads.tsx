import { createFileRoute, Link } from "@tanstack/react-router";
import { createServerFn } from "@tanstack/react-start";
import { useState } from "react";
import { getRecentLeads } from "~/db";

export const Route = createFileRoute("/admin/leads")({
  component: AdminLeads,
});

type Lead = Record<string, unknown>;

// Requires ADMIN_KEY to be set in the server environment. Fails closed: if the
// env var is missing or the key doesn't match, no data leaves the server.
const fetchLeads = createServerFn({ method: "POST" }).handler(
  async (input: unknown) => {
    const { key } = (input ?? {}) as { key?: string };
    const adminKey = process.env.ADMIN_KEY;
    if (!adminKey || !key || key !== adminKey) {
      return { ok: false as const, leads: [] as Lead[] };
    }
    const leads = (await getRecentLeads(100)) as Lead[];
    return { ok: true as const, leads };
  }
);

function AdminLeads() {
  const [key, setKey] = useState("");
  const [unlocked, setUnlocked] = useState(false);
  const [leads, setLeads] = useState<Lead[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleUnlock = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const result = await fetchLeads({ key });
      if (result.ok) {
        setLeads(result.leads);
        setUnlocked(true);
      } else {
        setError("Invalid access key.");
      }
    } catch {
      setError("Could not load leads — is the database connected?");
    } finally {
      setLoading(false);
    }
  };

  if (!unlocked) {
    return (
      <div className="mx-auto max-w-md px-6 py-24">
        <Link to="/" className="text-sm text-indigo-600 hover:text-indigo-700">← Back to site</Link>
        <h1 className="mt-4 text-2xl font-bold text-gray-900">Admin — Lead Management</h1>
        <p className="mt-2 text-sm text-gray-600">Enter the admin access key to view captured leads.</p>
        <form onSubmit={handleUnlock} className="mt-6 space-y-4">
          <input
            type="password"
            value={key}
            onChange={(e) => setKey(e.target.value)}
            placeholder="Access key"
            className="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
            autoFocus
          />
          {error && <p className="text-sm text-red-600">{error}</p>}
          <button
            type="submit"
            disabled={loading || !key}
            className="w-full rounded-lg bg-indigo-600 px-6 py-2.5 text-sm font-semibold text-white transition-all hover:bg-indigo-700 disabled:opacity-50"
          >
            {loading ? "Checking…" : "Unlock"}
          </button>
        </form>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-6xl px-6 py-12">
      <div className="mb-8">
        <Link to="/" className="text-sm text-indigo-600 hover:text-indigo-700">← Back to site</Link>
        <h1 className="mt-4 text-3xl font-bold text-gray-900">Lead Management</h1>
        <p className="mt-2 text-gray-600">{leads.length} lead(s) captured</p>
      </div>
      {leads.length === 0 ? (
        <div className="rounded-xl border border-gray-200 bg-gray-50 p-12 text-center">
          <p className="text-gray-400">No leads yet. Forms are configured and ready to capture.</p>
        </div>
      ) : (
        <div className="overflow-x-auto rounded-xl border border-gray-200">
          <table className="min-w-full divide-y divide-gray-200 text-sm">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left font-semibold text-gray-700">ID</th>
                <th className="px-4 py-3 text-left font-semibold text-gray-700">Name</th>
                <th className="px-4 py-3 text-left font-semibold text-gray-700">Email</th>
                <th className="px-4 py-3 text-left font-semibold text-gray-700">Company</th>
                <th className="px-4 py-3 text-left font-semibold text-gray-700">Revenue</th>
                <th className="px-4 py-3 text-left font-semibold text-gray-700">Source</th>
                <th className="px-4 py-3 text-left font-semibold text-gray-700">Score</th>
                <th className="px-4 py-3 text-left font-semibold text-gray-700">Date</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {leads.map((lead) => (
                <tr key={String(lead.id)} className="hover:bg-gray-50">
                  <td className="px-4 py-3 text-gray-500">{String(lead.id)}</td>
                  <td className="px-4 py-3 font-medium text-gray-900">{String(lead.name)}</td>
                  <td className="px-4 py-3 text-gray-700">{String(lead.email)}</td>
                  <td className="px-4 py-3 text-gray-700">{String(lead.company || "-")}</td>
                  <td className="px-4 py-3 text-gray-700">{String(lead.revenue_range || "-")}</td>
                  <td className="px-4 py-3">
                    <span className={`inline-block rounded-full px-2 py-0.5 text-xs font-medium ${
                      lead.source === "scorecard" ? "bg-purple-100 text-purple-700" : "bg-blue-100 text-blue-700"
                    }`}>
                      {String(lead.source)}
                    </span>
                  </td>
                  <td className="px-4 py-3 font-medium">{lead.score ? String(lead.score) : "-"}</td>
                  <td className="px-4 py-3 text-gray-500 text-xs">{String(lead.created_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
