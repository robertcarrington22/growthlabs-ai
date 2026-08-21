# Blog Page & Demo Landing Page Copy

## Blog Page (`/blog`)

**Current state**: Need to add the sample blog post and make it easy to publish.

**Blog listing page copy**:

```
# Revenue Insights for Growing Businesses

Practical, data-backed advice on pricing, churn, upsells, and growth strategy — written for service business owners who want to grow smarter.

[Subscribe to our newsletter →] [Get the Revenue Health Scorecard →]
```

**Blog post display**: Title, excerpt (2–3 sentences), read time, category tag, date.

---

## Sample Blog Post — Web-Ready Version

The full blog post content lives in `03-sample-blog-post.md`. For the website, it should be rendered as a page at `/blog/5-hidden-revenue-leaks`. 

**For now**, here's a downloadable PDF concept:

### "Download as PDF" Concept

Create a simple PDF that contains:
1. Cover page: "5 Hidden Revenue Leaks Costing Your Service Business $50K+/Year — GrowthLabs AI"
2. Full article content (from `03-sample-blog-post.md`)
3. Back page: CTA for Revenue Health Scorecard + Discovery Audit offer

**How to implement on the site**:
1. Create a route: `src/routes/blog/5-hidden-revenue-leaks.tsx`
2. Render the blog post HTML with proper formatting
3. Add a "Download PDF" button that generates a print-friendly version
4. Add bottom-of-post CTA: "Discover your biggest revenue leak — take the free Revenue Health Scorecard →" (link to /scorecard)

**SEO metadata**:
- Title: "5 Hidden Revenue Leaks Costing Your Service Business $50K+/Year | GrowthLabs AI"
- Description: "Most service businesses are unknowingly losing revenue in predictable ways. Here's how to find—and fix—the five biggest leaks."
- Keywords: revenue leaks, service business growth, pricing optimization, churn reduction

---

## Request a Demo Page (`/demo`)

### Headline
**See GrowthLabs AI in action.**

### Subheadline
Book a 30-minute demo where we'll run a sample analysis on your data (or a demo dataset) and show you exactly what you'd discover in a full Discovery Audit.

### What You'll See in the Demo

- **AI-powered revenue analysis**: Watch our engine analyze pricing, churn, and upsell patterns in real time
- **Your personalized findings**: We'll use your CRM/billing data (or a demo dataset) to show real opportunities
- **Sample report walkthrough**: See what a Discovery Audit report looks like, with prioritized recommendations
- **Q&A**: Ask anything about how it works, pricing, and what you'd get

### Form Fields

| Field | Type | Required |
|-------|------|----------|
| Full Name | Text | Yes |
| Email | Text | Yes |
| Company Name | Text | Yes |
| Revenue Range | Dropdown ($500K–$2M / $2M–$5M / $5M–$10M / $10M+) | Yes |
| Company Size | Dropdown (1–10 / 10–50 / 50–200 / 200+) | Yes |
| What's your biggest revenue challenge? | Textarea | No |
| Preferred Date | Date picker | Yes |
| Preferred Time | Dropdown (Morning / Afternoon / Evening) | Yes |

### CTA
**"Book Your Demo →"**

### Trust Signals (below form)
- "No commitment. No pitch. Just a live walkthrough of what we'd find in your data."
- "Most demos uncover at least 3 revenue opportunities worth $20K+."
- "We've helped 50+ service businesses identify hidden revenue."

### Thank You Page (after booking)
**Headline**: Thanks, [Name]! We'll be in touch shortly.

**Body**: We've received your demo request. Someone from our team will confirm your slot within 24 hours.

In the meantime:
- 👉 Take the free [Revenue Health Scorecard](link)
- 👉 Read our blog post on [5 Hidden Revenue Leaks](link)

---

## Implementation Notes for Web Developer

### New routes needed:
- `src/routes/blog/index.tsx` — blog listing page
- `src/routes/blog/5-hidden-revenue-leaks.tsx` — first blog post
- `src/routes/demo.tsx` — Request a Demo page
- `src/routes/demo/thank-you.tsx` — thank you / confirmation

### Lead capture:
- Demo form submissions should go to a database (use Turso or connect via `createServerFn`)
- Blog newsletter signup can use the same DB

### Scoring logic for Revenue Health Scorecard:
- Build at `/scorecard` — see `04-lead-magnet-revenue-health-scorecard.md` for full spec
- 15 questions across 5 dimensions (20 pts each = 100)
- Show result immediately after submission