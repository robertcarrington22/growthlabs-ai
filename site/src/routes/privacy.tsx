import { createFileRoute, Link } from "@tanstack/react-router";

export const Route = createFileRoute("/privacy")({
  component: Privacy,
});

function Privacy() {
  return (
    <>
      <section className="bg-gradient-to-br from-indigo-50 via-white to-blue-50 py-16 sm:py-24">
        <div className="mx-auto max-w-7xl px-6 text-center">
          <span className="inline-block rounded-full bg-indigo-100 px-4 py-1.5 text-sm font-medium text-indigo-700">
            Privacy Policy
          </span>
          <h1 className="mt-6 text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl">
            Your Data, Your Control
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-600">
            We take data privacy seriously. Here's exactly what we collect, why we collect it,
            and how you can control it.
          </p>
        </div>
      </section>

      <section className="bg-white py-16 sm:py-24">
        <div className="mx-auto max-w-3xl px-6 space-y-12">
          {/* Scope */}
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Scope of This Policy</h2>
            <p className="mt-4 text-sm leading-relaxed text-gray-600">
              This policy applies to all information collected through the GrowthLabs AI website,
              the Revenue Health Scorecard, Discovery Audit submissions, and any related
              communications. It covers US users and is designed with awareness of California
              Consumer Privacy Act (CCPA/CPRA) requirements.
            </p>
          </div>

          {/* What we collect */}
          <div>
            <h2 className="text-2xl font-bold text-gray-900">What Data We Receive</h2>
            <div className="mt-4 space-y-4 text-sm leading-relaxed text-gray-600">
              <p><strong>From the Scorecard and Contact Form:</strong> Your name, email address, company name, revenue range, and any message you send us. This helps us qualify leads and tailor our response.</p>
              <p><strong>From the Discovery Audit:</strong> Transaction and customer data (CSV files or direct integrations) you provide for analysis. This includes customer IDs, transaction amounts, service types, dates, and related business data needed to identify revenue gaps.</p>
              <p><strong>From website browsing:</strong> Standard analytics data (page views, referrer, browser type) through our analytics provider. We do not sell this data.</p>
            </div>
          </div>

          {/* How we use it */}
          <div>
            <h2 className="text-2xl font-bold text-gray-900">How We Use Your Data</h2>
            <ul className="mt-4 space-y-3 text-sm text-gray-600">
              {[
                "To run the Revenue Health Scorecard and deliver your results",
                "To perform the Discovery Audit and generate your revenue growth report",
                "To communicate with you about your audit, retainer, or inquiries",
                "To improve our AI analysis engine (using aggregated, anonymized patterns)",
                "To send occasional relevant content (you can opt out anytime)",
              ].map((item) => (
                <li key={item} className="flex items-start gap-3">
                  <svg className="mt-0.5 h-4 w-4 shrink-0 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                  {item}
                </li>
              ))}
            </ul>
          </div>

          {/* Who sees it */}
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Who Sees Your Data</h2>
            <p className="mt-4 text-sm leading-relaxed text-gray-600">
              Your data is accessible only to the GrowthLabs AI team members directly involved
              in your audit. We use third-party services for cloud storage and analytics, but
              we never share your raw business data with third parties for their own purposes.
              We do not sell your personal information or business data.
            </p>
            <p className="mt-3 text-sm leading-relaxed text-gray-600">
              If you're a California resident, you have the right to request disclosure of
              what personal information we collect, request deletion, and opt out of any
              "sale" of data (we do not sell data).
            </p>
          </div>

          {/* Retention */}
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Retention Policy</h2>
            <p className="mt-4 text-sm leading-relaxed text-gray-600">
              We retain your audit data (transaction records, customer data) for the duration
              of your engagement plus 12 months, to support ongoing analysis and follow-ups.
              After that, raw data is deleted. Aggregated, anonymized patterns may be retained
              to improve our analysis engine for future clients.
            </p>
            <p className="mt-3 text-sm leading-relaxed text-gray-600">
              Contact information and lead data are retained until you request deletion or
              opt out of communications.
            </p>
          </div>

          {/* Deletion */}
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Deletion on Request</h2>
            <p className="mt-4 text-sm leading-relaxed text-gray-600">
              You can request deletion of your data at any time. To do so, email us at
              <strong> privacy@growthlabs.ai</strong> from the email address associated
              with your account. We will confirm receipt within 48 hours and complete
              deletion within 14 days. This includes all raw transaction and customer data
              you uploaded, as well as your contact information.
            </p>
          </div>

          {/* Security */}
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Data Security</h2>
            <p className="mt-4 text-sm leading-relaxed text-gray-600">
              All data is encrypted in transit (TLS 1.3) and at rest (AES-256). Access to
              your audit data is restricted to team members with a direct need. We use
              industry-standard cloud infrastructure with SOC 2 compliance. For the Discovery
              Audit, we offer a white-glove data pull option where we guide you through a
              20-minute screen share to export data directly — no files need to be emailed
              or uploaded through unsecured channels.
            </p>
          </div>

          {/* Updates */}
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Updates to This Policy</h2>
            <p className="mt-4 text-sm leading-relaxed text-gray-600">
              We may update this policy as our practices evolve. If we make material changes,
              we'll notify you by email or through a notice on our website. The effective
              date at the top of this page will reflect the most recent update.
            </p>
          </div>

          {/* Contact */}
          <div className="rounded-xl border border-indigo-100 bg-indigo-50 p-6">
            <h2 className="text-lg font-bold text-gray-900">Have Questions?</h2>
            <p className="mt-2 text-sm text-gray-600">
              Email us at <strong>privacy@growthlabs.ai</strong> or use our <Link to="/contact" className="text-indigo-600 underline hover:text-indigo-700">contact form</Link>.
              We typically respond within 24 hours.
            </p>
          </div>
        </div>
      </section>
    </>
  );
}