# GrowthLabs AI

**AI-powered revenue audits for small businesses.** Upload your transaction and customer data, get back a prioritized report on pricing inefficiencies, churn patterns, underperforming channels, and upsell opportunities — the analysis a fractional CFO would charge thousands for, run in minutes.

**Live site:** [growthlabs-ai.vercel.app](https://growthlabs-ai.vercel.app)

This repo contains the whole business, not just code: the analysis engine, the marketing site, and the go-to-market machine behind it.

## The three pieces

### 1. Analysis engine — [`ai-engine/`](ai-engine/)

A Python engine that ingests CSV exports (transactions + customers) and produces a structured audit report. Analysis modules cover revenue trends and seasonality, customer segmentation and cohort retention, pricing and margin analysis, churn indicators, CLV estimation, causal-loop diagnostics, and a full inventory suite (classification, forecasting, KPIs, reorder policy). Industry-specific heuristics tune the analysis for SaaS, e-commerce, manufacturing, local services, and professional services.

Runs three ways: CLI (`python main.py --sample`), a **FastAPI** service with authenticated upload/report endpoints ([`api/server.py`](ai-engine/api/server.py)), or Docker. Ships with a synthetic data generator and a pytest suite covering ingestion and the inventory pipeline. Details in the [engine README](ai-engine/README.md).

### 2. Marketing site — [`site/`](site/)

A full-stack **TanStack Start** app (React + Vite + Tailwind) deployed on Vercel. Beyond the standard pages, it includes interactive lead-capture tools: an [ROI calculator](site/src/routes/roi.tsx), a revenue-health [quiz](site/src/routes/quiz.tsx) and [scorecard](site/src/routes/scorecard.tsx), per-industry landing pages, a data [upload flow](site/src/routes/upload.tsx), and an internal leads dashboard.

### 3. Go-to-market — [`marketing/`](marketing/) and [`research/`](research/)

The operating playbooks: positioning and website copy, a content calendar, LinkedIn and email outreach sequences, target-account research batches with verification passes, lead magnets, a partnership program, and an outbound engine spec. Written to be executed, not admired — the outreach tracker CSV logs actual sends.

## Repo map

```
ai-engine/     Python analysis engine: CLI, FastAPI service, Dockerfile, tests
site/          TanStack Start marketing site (Vercel)
brand/         Logo and asset generation scripts
marketing/     Positioning, content, outreach sequences, campaign briefs
research/      Target-account research and strategy deep dives
```

## Stack

Python + pandas + FastAPI + pytest + Docker · React + TanStack Start + Vite + Tailwind · Vercel

---

Built and run by [Robert Carrington](https://github.com/rob-carri-collab).
