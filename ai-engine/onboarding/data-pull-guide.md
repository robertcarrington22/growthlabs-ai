# GrowthLabs AI — White-Glove Data Pull Guide

**Goal:** Collect 3 years of transaction and customer data from the client in ≤ 20 minutes.
**Who does this:** GrowthLabs AI analyst (screen share with client).
**Client effort:** Zero — just share your screen and click where we say.

---

## Before the Call

1. Schedule a 30-minute screen-share call (we only need 20 min).
2. Send the client one link: **no prep needed.**
3. Open this guide and prepare to walk through the relevant section below.

---

## Option A: QuickBooks Online (most common — ~60% of US SMBs)

1. **Log in** to QuickBooks Online at [qbo.intuit.com](https://qbo.intuit.com).
2. Go to **Reports** → **Profit and Loss** (or search "Profit and Loss").
3. Set the date range to **last 3 full calendar years** (e.g., Jan 1, 2023 – Dec 31, 2025).
4. Click **Export** → **Export to Excel**.
5. Save the file as `qb_profit_loss_<client-name>.csv`.
6. **Next:** Go to **Reports** → **Transaction List by Customer**.
7. Set the same 3-year date range.
8. Click **Export** → **Export to Excel**.
9. Save as `qb_transactions_<client-name>.csv`.
10. Upload both files to the secure upload link we provided.

**What we receive:** All transactions with customer names, dates, amounts, and categories.

---

## Option B: Stripe (for SaaS, e-commerce, subscription businesses)

1. **Log in** to [dashboard.stripe.com](https://dashboard.stripe.com).
2. Go to **Reports** → **Payouts** or **Balance** → **Transaction list**.
3. Set date range to **last 3 full calendar years**.
4. Click **Export** → choose **CSV** format.
5. Save as `stripe_transactions_<client-name>.csv`.
6. **If available:** Go to **Customers** → **Export customers** → **CSV**.
7. Save as `stripe_customers_<client-name>.csv`.
8. Upload to the secure upload link.

**Pro tip:** For SaaS clients, also export a **Subscriptions** report (shows MRR changes, upgrades, downgrades).
Go to: **Reports** → **Subscription report** → **Export**.

---

## Option C: Xero (for accounting firms and NZ/UK/AU clients)

1. **Log in** to [xero.com](https://xero.com).
2. Go to **Accounting** → **Reports** → **Profit and Loss**.
3. Set date range to **last 3 full calendar years**.
4. Click **Export** → **CSV**.
5. Save as `xero_pnl_<client-name>.csv`.
6. **Next:** Go to **Reports** → **Transaction Detail by Contact**.
7. Set same date range.
8. Export as CSV.
9. Upload to the secure upload link.

---

## Option D: Manual CSV Upload (catch-all for other systems)

If the client uses a different system (FreshBooks, Wave, Zoho, custom):
1. Ask them to export transactions from their system.
2. **Required columns**: `transaction_id`, `customer_id`, `date`, `amount`
3. **Nice-to-have columns**: `service_name`, `quantity`, `margin_pct`
4. **Optional**: A separate customer file with: `customer_id`, `industry`, `acquisition_channel`, `acquisition_date`

We accept any CSV that has at minimum: **transaction ID, customer ID, date, and amount**.

---

## After the Call

1. Confirm both CSVs were uploaded successfully.
2. Send client a brief "Got it, thank you!" email.
3. Run the data through our ingestion validator to check for issues.
4. If data looks good, proceed to the analysis pipeline.
5. Schedule the audit delivery call within 5 business days.

---

## Fallback: If the client can't do the call

1. Send them this guide as a PDF or Notion page.
2. Ask them to follow the appropriate option (A/B/C/D).
3. Offer a 10-minute "quick help" call if they get stuck.
4. **Worst case:** We accept a manual data entry via a Google Sheet template (15 min to fill in).

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "I only have 1 year of data" | Accept it — we work with what we have |
| "My QuickBooks is a mess" | We clean it on our end — send it raw |
| "I'm worried about security" | Reference our data-security policy (see `data-security.md`) |
| "Can my bookkeeper do this?" | Yes — forward them this guide |
| "I use [unknown system]" | Export whatever CSV you can; we'll map it |

---

*Last updated: July 2026*