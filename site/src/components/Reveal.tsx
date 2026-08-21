import { useEffect, useRef, useState, type ReactNode } from "react";

/**
 * Fades content up into view the first time it scrolls into the viewport.
 * Pure CSS transition driven by an IntersectionObserver — renders visible
 * immediately when JS or IntersectionObserver is unavailable, and
 * `prefers-reduced-motion` disables the effect entirely (see app.css).
 */
export function Reveal({
  children,
  delay = 0,
  className = "",
}: {
  children: ReactNode;
  delay?: number;
  className?: string;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (typeof IntersectionObserver === "undefined") {
      setVisible(true);
      return;
    }
    // A working IntersectionObserver always delivers an initial report right
    // after observe(). If none arrives, the observer is broken in this
    // environment — fail open so content is never stuck invisible.
    let reported = false;
    const fallback = setTimeout(() => {
      if (!reported) setVisible(true);
    }, 1500);
    const io = new IntersectionObserver(
      ([entry]) => {
        reported = true;
        if (entry.isIntersecting) {
          setVisible(true);
          io.disconnect();
        }
      },
      { threshold: 0.15, rootMargin: "0px 0px -40px 0px" },
    );
    io.observe(el);
    return () => {
      clearTimeout(fallback);
      io.disconnect();
    };
  }, []);

  return (
    <div
      ref={ref}
      className={`reveal ${visible ? "is-visible" : ""} ${className}`}
      style={delay ? { transitionDelay: `${delay}ms` } : undefined}
    >
      {children}
    </div>
  );
}
