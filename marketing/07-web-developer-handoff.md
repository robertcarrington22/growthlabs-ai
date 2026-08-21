# Web Developer Handoff — Marketing Content for the Site

Hey Web Dev — I've built the complete marketing copy and content strategy. Here's what needs implementing on the site.

## Priority Implementation Items

### 1. Homepage (`/`)
- Use copy from `01-website-copy-brief.md` section "Homepage"
- Hero: "Find the revenue hiding in your data"
- Two CTAs: "Get Your Discovery Audit →" (primary), "See How It Works →" (secondary)
- Brand voice: confident, data-driven, human
- SEO title: GrowthLabs AI | AI-Powered Revenue Growth for Service Businesses

### 2. Services Page (`/services`)
- 3 service cards: Discovery Audit ($495–$995), Growth Retainer (quoted after audit), Performance Bonus (up to 10%)
- Full copy for each in the brief

### 3. How It Works Page (`/how-it-works`)
- 3-phase process: Audit (Week 1–2) → Plan (Week 3) → Execute (Ongoing)
- Clear CTA chain throughout

### 4. About Page (`/about`)
- Brand story and differentiators

### 5. Blog Page (`/blog`)
- Listing page for blog posts
- First post ready: `03-sample-blog-post.md`

### 6. Revenue Health Scorecard Landing Page
- Full copy in `04-lead-magnet-revenue-health-scorecard.md`
- **Form fields**: Name, Email, Company, Revenue Range (dropdown), Challenge (textarea)
- **Scoring**: 15 questions across 5 dimensions (20 pts each = 100 total)
- Show score immediately after submission with personalized recommendations
- Score tiers: 80–100 (Healthy), 60–79 (Moderate Gaps), 40–59 (Significant Leaks), 0–39 (Critical)

### 7. Contact Page
- Simple form: Name, Email, Company, Revenue Range, Message

## Technical Notes
- All marketing files are in `/home/team/shared/marketing/`
- The site.json already has the business name set: `{ "businessName": "GrowthLabs AI" }`
- Lead magnet needs email capture → store in DB (Turso or similar)
- Blog posts stored in DB or as markdown files rendered server-side
- Full copy brief and CTA matrix in `/home/team/shared/marketing/01-website-copy-brief.md`

Let me know if you need any copy trimmed or expanded for specific pages! — Marketing Lead