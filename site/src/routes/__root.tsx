import {
  HeadContent,
  Outlet,
  Scripts,
  createRootRoute,
  Link,
} from "@tanstack/react-router";
import type { ReactNode } from "react";
import { useState } from "react";

import appCss from "~/styles/app.css?url";

export const Route = createRootRoute({
  head: () => ({
    meta: [
      { charSet: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      { title: "GrowthLabs AI | Know What to Fix Next in Your Business" },
      {
        name: "description",
        content:
          "The growth team small businesses don't have. GrowthLabs AI turns your sales history into a plain-English plan: make more money, free up cash, and know what to fix next.",
      },
      // Link previews (iMessage, Slack, LinkedIn, etc.) read Open Graph, not <title>
      { property: "og:title", content: "GrowthLabs AI" },
      { property: "og:site_name", content: "GrowthLabs AI" },
      {
        property: "og:description",
        content: "Know exactly what to fix next in your business.",
      },
      { property: "og:type", content: "website" },
      { property: "og:url", content: "https://growthlabs-ai.vercel.app" },
      { property: "og:image", content: "https://growthlabs-ai.vercel.app/og-image.png" },
      { property: "og:image:width", content: "1200" },
      { property: "og:image:height", content: "630" },
      { name: "twitter:card", content: "summary_large_image" },
      { name: "twitter:title", content: "GrowthLabs AI" },
      {
        name: "twitter:description",
        content: "Know exactly what to fix next in your business.",
      },
      { name: "twitter:image", content: "https://growthlabs-ai.vercel.app/og-image.png" },
    ],
    links: [
      { rel: "icon", type: "image/svg+xml", href: "/favicon.svg" },
      { rel: "icon", type: "image/png", sizes: "32x32", href: "/favicon-32.png" },
      { rel: "alternate icon", href: "/favicon.ico" },
      { rel: "apple-touch-icon", sizes: "180x180", href: "/apple-touch-icon.png" },
      { rel: "stylesheet", href: appCss },
      { rel: "preconnect", href: "https://fonts.googleapis.com" },
      {
        rel: "preconnect",
        href: "https://fonts.gstatic.com",
        crossOrigin: "anonymous",
      },
      {
        rel: "stylesheet",
        href: "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
      },
    ],
  }),
  notFoundComponent: () => (
    <div className="flex min-h-[60vh] flex-col items-center justify-center gap-4 px-6 text-center">
      <h1 className="text-4xl font-bold">Page not found</h1>
      <p className="text-lg text-gray-600">The page you're looking for doesn't exist.</p>
      <Link
        to="/"
        className="rounded-lg bg-indigo-600 px-6 py-3 font-medium text-white hover:bg-indigo-700 transition-colors"
      >
        Go home
      </Link>
    </div>
  ),
  component: RootComponent,
});

const NAV_LINKS = [
  { to: "/how-it-works", label: "How It Works" },
  { to: "/pricing", label: "Pricing" },
  { to: "/scorecard", label: "Scorecard" },
  { to: "/blog", label: "Blog" },
  { to: "/contact", label: "Get Started" },
];

function RootComponent() {
  return (
    <RootDocument>
      <Outlet />
    </RootDocument>
  );
}

function RootDocument({ children }: { children: ReactNode }) {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <html lang="en" className="scroll-smooth">
      <head>
        <HeadContent />
      </head>
      <body className="font-['Inter',system-ui,sans-serif]">
        <header className="sticky top-0 z-50 border-b border-gray-100 bg-white/90 backdrop-blur-md">
          <nav className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
            <Link to="/" className="flex items-center gap-2 text-xl font-bold text-indigo-700">
              <svg className="h-7 w-7" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect width="28" height="28" rx="6" fill="#4f46e5" />
                <path d="M7 10h3v8H7v-8zm5-3h3v14h-3V7zm5 5h3v6h-3v-6z" fill="white" />
              </svg>
              GrowthLabs AI
            </Link>

            {/* Desktop nav */}
            <div className="hidden items-center gap-8 md:flex">
              {NAV_LINKS.map((link) => (
                <Link
                  key={link.to}
                  to={link.to}
                  className="nav-link text-sm font-medium text-gray-600 transition-colors hover:text-indigo-600 [&.active]:text-indigo-700"
                  activeProps={{ className: "text-indigo-700 font-semibold" }}
                >
                  {link.label}
                </Link>
              ))}
            </div>

            {/* Hamburger button (mobile) */}
            <button
              onClick={() => setMobileOpen(!mobileOpen)}
              className="ml-auto flex h-10 w-10 items-center justify-center rounded-lg md:hidden"
              aria-label={mobileOpen ? "Close menu" : "Open menu"}
            >
              {mobileOpen ? (
                <svg className="h-6 w-6 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              ) : (
                <svg className="h-6 w-6 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              )}
            </button>
          </nav>

          {/* Mobile slide-down panel */}
          {mobileOpen && (
            <div className="border-t border-gray-100 bg-white md:hidden">
              <div className="space-y-1 px-6 pb-6 pt-2">
                {NAV_LINKS.map((link) => (
                  <Link
                    key={link.to}
                    to={link.to}
                    onClick={() => setMobileOpen(false)}
                    className="block rounded-lg px-4 py-3 text-base font-medium text-gray-700 transition-colors hover:bg-indigo-50 hover:text-indigo-700"
                    activeProps={{ className: "text-indigo-700 bg-indigo-50 font-semibold" }}
                  >
                    {link.label}
                  </Link>
                ))}
              </div>
            </div>
          )}
        </header>
        <main>{children}</main>
        <footer className="border-t border-gray-100 bg-gray-50">
          <div className="mx-auto max-w-7xl px-6 py-12">
            <div className="grid gap-8 md:grid-cols-4">
              <div className="md:col-span-2">
                <div className="flex items-center gap-2 text-lg font-bold text-indigo-700">
                  <svg className="h-6 w-6" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect width="28" height="28" rx="6" fill="#4f46e5" />
                    <path d="M7 10h3v8H7v-8zm5-3h3v14h-3V7zm5 5h3v6h-3v-6z" fill="white" />
                  </svg>
                  GrowthLabs AI
                </div>
                <p className="mt-3 max-w-md text-sm text-gray-500">
                  The growth team small businesses don't have. We study your numbers
                  and hand you a plain-English plan: make more money, free up cash,
                  and know what to fix next.
                </p>
              </div>
              <div>
                <h4 className="mb-3 text-sm font-semibold uppercase tracking-wider text-gray-900">
                  Pages
                </h4>
                <ul className="space-y-2 text-sm text-gray-500">
                  <li><Link to="/how-it-works" className="transition-colors hover:text-indigo-600">How It Works</Link></li>
                  <li><Link to="/pricing" className="transition-colors hover:text-indigo-600">Pricing</Link></li>
                  <li><Link to="/scorecard" className="transition-colors hover:text-indigo-600">Scorecard</Link></li>
                  <li><Link to="/blog" className="transition-colors hover:text-indigo-600">Blog</Link></li>
                  <li><Link to="/privacy" className="transition-colors hover:text-indigo-600">Privacy</Link></li>
                </ul>
              </div>
              <div>
                <h4 className="mb-3 text-sm font-semibold uppercase tracking-wider text-gray-900">
                  Contact
                </h4>
                <ul className="space-y-2 text-sm text-gray-500">
                  <li>hello@growthlabs.ai</li>
                  <li>San Francisco, CA</li>
                </ul>
              </div>
            </div>
            <div className="mt-10 border-t border-gray-200 pt-6 text-center text-sm text-gray-400">
              &copy; {new Date().getFullYear()} GrowthLabs AI. All rights reserved.
            </div>
          </div>
        </footer>
        <Scripts />
      </body>
    </html>
  );
}