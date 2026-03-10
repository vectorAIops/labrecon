"use client";

import { useMemo, useState } from "react";
import Image from "next/image";
import {
  labTests,
  activeProviders,
  type LabTest,
  type Provider,
} from "./data/labTests";

// ── Types ────────────────────────────────────────────────────────

type Totals = Record<string, number>;

// ── Helpers ──────────────────────────────────────────────────────

function dollars(value: number) {
  return `$${value.toFixed(2)}`;
}

// Grid template for the comparison table.
// Computed once — stays in sync if activeProviders count ever changes.
const shopColTemplate = `1.6fr ${activeProviders.map(() => "0.5fr").join(" ")} 0.45fr`;

// ── Icons ────────────────────────────────────────────────────────

function ChevronIcon({ className }: { className?: string }) {
  return (
    <svg
      width="16"
      height="16"
      viewBox="0 0 16 16"
      fill="none"
      aria-hidden="true"
      className={className}
    >
      <path
        d="M3 5.5L8 10.5L13 5.5"
        stroke="currentColor"
        strokeWidth="1.75"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

// ── TestRow ───────────────────────────────────────────────────────
// Renders one test in the Shop Tests table.
// Clicking the test name expands an accordion with biomarkers,
// plain/clinical descriptions, and ordering notes.

function TestRow({
  test,
  isSelected,
  onToggle,
}: {
  test: LabTest;
  isSelected: boolean;
  onToggle: () => void;
}) {
  const [isOpen, setIsOpen] = useState(false);

  const validPrices = activeProviders
    .map((p) => test.pricing[p.id])
    .filter((p): p is number => p !== undefined);
  const minPrice = validPrices.length > 0 ? Math.min(...validPrices) : null;

  return (
    <div
      className={`border-b border-[#221c14] border-l-[3px] transition-colors duration-300 ${
        isOpen ? "border-l-[#c9ab77] bg-[#0c0b09]" : "border-l-transparent"
      }`}
    >
      {/* ── Main row ── */}
      <div
        className="grid items-center px-4 py-4 text-sm text-[#e6d5ae]"
        style={{ gridTemplateColumns: shopColTemplate }}
      >
        {/* Test name — expand toggle */}
        <button
          onClick={() => setIsOpen((v) => !v)}
          className="flex items-center gap-2 text-left"
          aria-expanded={isOpen}
        >
          <span
            className={`font-medium transition-colors duration-150 ${
              isOpen ? "text-[#c9ab77]" : "text-[#f4e8ca] hover:text-[#c9ab77]"
            }`}
          >
            {test.displayName}
          </span>
          <ChevronIcon
            className={`shrink-0 transition-transform duration-200 ${
              isOpen ? "text-[#c9ab77] rotate-180" : "text-[#5a4930]"
            }`}
          />
        </button>

        {/* Provider price columns */}
        {activeProviders.map((p: Provider) => {
          const price = test.pricing[p.id];
          const isBest = price !== undefined && price === minPrice;
          return (
            <div
              key={p.id}
              className={isBest ? "font-semibold text-[#c9ab77]" : ""}
            >
              {price !== undefined ? dollars(price) : "—"}
            </div>
          );
        })}

        {/* Add / Remove button */}
        <div className="text-right">
          <button
            onClick={onToggle}
            className={`rounded-lg px-4 py-2 text-xs font-semibold uppercase tracking-[0.12em] transition ${
              isSelected
                ? "border border-[#7c6743] bg-[#1f1911] text-[#f2dfb5]"
                : "border border-[#4b3d2a] bg-[#11100d] text-[#cfbe98] hover:border-[#c9ab77] hover:text-[#f4e8ca]"
            }`}
          >
            {isSelected ? "Remove" : "Add"}
          </button>
        </div>
      </div>

      {/* ── Accordion detail ── */}
      <div
        className="grid transition-all duration-300 ease-in-out"
        style={{ gridTemplateRows: isOpen ? "1fr" : "0fr" }}
      >
        <div className="overflow-hidden">
          <div className="border-t border-[#1e1a14] bg-[#0b0a08] px-5 py-5">
            <div className="grid gap-6 sm:grid-cols-2">
              {/* Descriptions */}
              <div className="space-y-4">
                <div>
                  <p className="mb-2 text-xs uppercase tracking-[0.16em] text-[#6b5535]">
                    What it measures
                  </p>
                  <p className="text-sm leading-7 text-[#cdbd98]">
                    {test.plainDescription}
                  </p>
                </div>
                <div>
                  <p className="mb-2 text-xs uppercase tracking-[0.16em] text-[#6b5535]">
                    Clinical notes
                  </p>
                  <p className="text-sm leading-7 text-[#8a7a62]">
                    {test.medicalDescription}
                  </p>
                </div>
              </div>

              {/* Biomarkers */}
              <div>
                <p className="mb-3 text-xs uppercase tracking-[0.16em] text-[#6b5535]">
                  Biomarkers included
                </p>
                <div className="flex flex-wrap gap-2">
                  {test.biomarkers.map((marker) => (
                    <span
                      key={marker}
                      className="rounded-md border border-[#3a3124] bg-[#0f0e0c] px-2.5 py-1 text-xs text-[#c9ab77]"
                    >
                      {marker}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            {/* Ordering note */}
            {test.notes && (
              <div className="mt-5 rounded-lg border border-[#2a2218] bg-[#0d0c0a] px-4 py-3">
                <p className="mb-1 text-xs uppercase tracking-[0.12em] text-[#5a4930]">
                  Ordering note
                </p>
                <p className="text-xs leading-6 text-[#7a6a50]">{test.notes}</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function EmailIcon() {
  return (
    <svg
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      aria-hidden="true"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75"
      />
    </svg>
  );
}

function LinkedInIcon() {
  return (
    <svg
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="currentColor"
      aria-hidden="true"
    >
      <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" />
    </svg>
  );
}

function RedditIcon() {
  return (
    <svg
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="currentColor"
      aria-hidden="true"
    >
      <path d="M12 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0zm5.01 4.744c.688 0 1.25.561 1.25 1.249a1.25 1.25 0 0 1-2.498.056l-2.597-.547-.8 3.747c1.824.07 3.48.632 4.674 1.488.308-.309.73-.491 1.207-.491.968 0 1.754.786 1.754 1.754 0 .716-.435 1.333-1.01 1.614a3.111 3.111 0 0 1 .042.52c0 2.694-3.13 4.87-7.004 4.87-3.874 0-7.004-2.176-7.004-4.87 0-.183.015-.366.043-.534A1.748 1.748 0 0 1 4.028 12c0-.968.786-1.754 1.754-1.754.463 0 .898.196 1.207.49 1.207-.883 2.878-1.43 4.744-1.487l.885-4.182a.342.342 0 0 1 .14-.197.35.35 0 0 1 .238-.042l2.906.617a1.214 1.214 0 0 1 1.108-.701zM9.25 12C8.561 12 8 12.562 8 13.25c0 .687.561 1.248 1.25 1.248.687 0 1.248-.561 1.248-1.249 0-.688-.561-1.249-1.249-1.249zm5.5 0c-.687 0-1.248.561-1.248 1.25 0 .687.561 1.248 1.249 1.248.688 0 1.249-.561 1.249-1.249 0-.687-.562-1.249-1.25-1.249zm-5.466 3.99a.327.327 0 0 0-.231.094.33.33 0 0 0 0 .463c.842.842 2.484.913 2.961.913.477 0 2.105-.056 2.961-.913a.361.361 0 0 0 .029-.463.33.33 0 0 0-.464 0c-.547.533-1.684.73-2.512.73-.828 0-1.979-.196-2.512-.73a.326.326 0 0 0-.232-.095z" />
    </svg>
  );
}

// ── Placeholder affiliate URLs ────────────────────────────────────
// Replace these with real affiliate links when available.
// Keyed by provider ID from activeProviders.
const PROVIDER_AFFILIATE_URLS: Record<string, string> = {
  quest: "#", // TODO: replace with Quest affiliate link
  labcorp: "#", // TODO: replace with LabCorp affiliate link
  goodlabs: "#", // TODO: replace with GoodLabs affiliate link
};

// ── Running Total Panel ───────────────────────────────────────────
// Fixed bottom drawer — slides up when tests are selected.
// Collapsed bar: shows cheapest total prominently + test count.
// Expanded: Section 1 — totals by provider. Section 2 — per-test breakdown.

function RunningTotalPanel({
  selectedLabData,
  totals,
  cheapestProvider,
  hasSelection,
}: {
  selectedLabData: LabTest[];
  totals: Totals;
  cheapestProvider: { name: string; value: number };
  hasSelection: boolean;
}) {
  const [isExpanded, setIsExpanded] = useState(false);

  const highestTotal = hasSelection
    ? Math.max(...activeProviders.map((p) => totals[p.id] ?? 0))
    : 0;
  const savings = highestTotal - cheapestProvider.value;

  return (
    <div
      className="fixed bottom-0 left-0 right-0 z-50"
      style={{
        transform: hasSelection ? "translateY(0)" : "translateY(100%)",
        pointerEvents: hasSelection ? "auto" : "none",
        transition: "transform 0.3s ease-out",
      }}
      role="complementary"
      aria-label="Running price comparison"
    >
      <div className="mx-auto max-w-5xl overflow-hidden rounded-t-2xl border-t border-x border-[#4a3b28] bg-[#0d0c0a]/96 shadow-[0_-8px_40px_rgba(0,0,0,0.55)] backdrop-blur-sm">
        {/* ── Collapsed bar ── */}
        {/* Layout: [count pill] [cheapest total — dominant] [Breakdown ▼] */}
        <button
          onClick={() => setIsExpanded((v) => !v)}
          className="grid w-full grid-cols-[auto_1fr_auto] items-center gap-4 px-5 py-4 text-left transition-colors hover:bg-[#141210] focus:outline-none focus-visible:ring-2 focus-visible:ring-[#c9ab77] focus-visible:ring-inset sm:px-6"
          aria-expanded={isExpanded}
        >
          {/* Left: test count pill */}
          <span className="shrink-0 rounded-full border border-[#5a4930] bg-[#1a1510] px-3 py-1 text-xs font-semibold uppercase tracking-[0.16em] text-[#c9ab77]">
            {selectedLabData.length}&nbsp;
            {selectedLabData.length === 1 ? "test" : "tests"}
          </span>

          {/* Center: cheapest total — visually dominant */}
          <span className="flex min-w-0 items-baseline gap-2">
            <span className="text-xl font-bold tabular-nums text-[#c9ab77] sm:text-2xl">
              {dollars(cheapestProvider.value)}
            </span>
            <span className="truncate text-xs text-[#7a6540]">
              cheapest &middot; {cheapestProvider.name}
            </span>
          </span>

          {/* Right: expand label + chevron */}
          <div className="flex shrink-0 items-center gap-2">
            <span className="hidden text-xs uppercase tracking-[0.14em] text-[#7a6540] sm:block">
              {isExpanded ? "Collapse" : "Breakdown"}
            </span>
            <ChevronIcon
              className={`text-[#c9ab77] transition-transform duration-200 ${
                isExpanded ? "rotate-180" : ""
              }`}
            />
          </div>
        </button>

        {/* ── Expandable body ── */}
        <div
          className="grid transition-all duration-300 ease-in-out"
          style={{ gridTemplateRows: isExpanded ? "1fr" : "0fr" }}
        >
          <div className="overflow-hidden">
            <div className="max-h-[66vh] overflow-y-auto border-t border-[#2a2218]">
              {/* Section 1 — Total by Provider */}
              <div className="border-b border-[#2a2218] px-5 py-5 sm:px-6">
                <p className="mb-4 text-xs uppercase tracking-[0.2em] text-[#5a4930]">
                  Total by provider
                </p>

                <div className="grid grid-cols-3 gap-3">
                  {activeProviders.map((p) => {
                    const value = totals[p.id] ?? 0;
                    const isCheapest = p.label === cheapestProvider.name;
                    return (
                      <div
                        key={p.id}
                        className={`rounded-xl border p-4 transition-colors ${
                          isCheapest
                            ? "border-[#c9ab77] bg-[#15120d]"
                            : "border-[#3a3124] bg-[#0c0b09]"
                        }`}
                      >
                        <p className="text-xs uppercase tracking-[0.12em] text-[#9f8558]">
                          {p.label}
                        </p>
                        <p
                          className={`mt-2 text-xl font-bold tabular-nums sm:text-2xl ${
                            isCheapest ? "text-[#c9ab77]" : "text-[#f6ead0]"
                          }`}
                        >
                          {dollars(value)}
                        </p>
                        {isCheapest && (
                          <p className="mt-1 text-xs uppercase tracking-[0.1em] text-[#c9ab77]">
                            Best Price
                          </p>
                        )}
                        <a
                          href={PROVIDER_AFFILIATE_URLS[p.id] ?? "#"}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="mt-3 inline-block rounded-lg border border-[#5a4930] bg-[#11100d] px-3 py-1.5 text-xs font-semibold text-[#e7d7b1] transition hover:border-[#c9ab77] hover:text-[#f4e8ca]"
                        >
                          View at {p.label}
                        </a>
                      </div>
                    );
                  })}
                </div>

                {savings > 0.01 && (
                  <div className="mt-4 rounded-lg border border-[#3a3124] bg-[#0c0b09] px-4 py-3">
                    <p className="text-sm text-[#a98a58]">
                      Choosing{" "}
                      <span className="font-semibold text-[#c9ab77]">
                        {cheapestProvider.name}
                      </span>{" "}
                      saves you{" "}
                      <span className="font-semibold text-[#c9ab77]">
                        {dollars(savings)}
                      </span>{" "}
                      compared to the highest option.
                    </p>
                  </div>
                )}

                {/* View Cheapest Option — links to the cheapest provider */}
                {hasSelection &&
                  (() => {
                    const cheapestId =
                      activeProviders.find(
                        (p) => p.label === cheapestProvider.name,
                      )?.id ?? "";
                    return (
                      <a
                        href={PROVIDER_AFFILIATE_URLS[cheapestId] ?? "#"}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="mt-4 inline-block rounded-xl border border-[#5a4930] bg-[#11100d] px-5 py-2.5 text-sm font-semibold text-[#e7d7b1] transition hover:border-[#c9ab77] hover:text-[#f4e8ca]"
                      >
                        View Cheapest Option &rarr;
                      </a>
                    );
                  })()}
              </div>

              {/* Section 2 — Per-Test Breakdown */}
              <div className="px-5 py-5 sm:px-6">
                <p className="mb-4 text-xs uppercase tracking-[0.2em] text-[#5a4930]">
                  Price per test{" "}
                  <span className="text-[#3a3124]">
                    ({selectedLabData.length})
                  </span>
                </p>

                <div className="overflow-hidden rounded-xl border border-[#2a2218]">
                  {/* Column header */}
                  <div
                    className="grid bg-[#0b0a08] px-4 py-3 border-b border-[#2a2218]"
                    style={{
                      gridTemplateColumns: `1fr ${activeProviders.map(() => "90px").join(" ")}`,
                    }}
                  >
                    <p className="text-xs uppercase tracking-[0.1em] text-[#5a4930]">
                      Test
                    </p>
                    {activeProviders.map((p) => (
                      <p
                        key={p.id}
                        className="text-right text-xs uppercase tracking-[0.1em] text-[#5a4930]"
                      >
                        {p.label}
                      </p>
                    ))}
                  </div>

                  {/* Test rows */}
                  {selectedLabData.map((test, i) => {
                    const validPrices = activeProviders
                      .map((p) => test.pricing[p.id])
                      .filter((v): v is number => v !== undefined);
                    const minPrice =
                      validPrices.length > 0 ? Math.min(...validPrices) : null;
                    const isLast = i === selectedLabData.length - 1;

                    return (
                      <div
                        key={test.id}
                        className={`grid items-center px-4 py-3 ${
                          !isLast ? "border-b border-[#1c1813]" : ""
                        } ${i % 2 === 0 ? "bg-[#0d0c0a]" : "bg-[#0b0a08]"}`}
                        style={{
                          gridTemplateColumns: `1fr ${activeProviders.map(() => "90px").join(" ")}`,
                        }}
                      >
                        <p className="truncate pr-3 text-sm text-[#e6d5ae]">
                          {test.displayName}
                        </p>
                        {activeProviders.map((p) => {
                          const price = test.pricing[p.id];
                          const isBest =
                            price !== undefined && price === minPrice;
                          return (
                            <p
                              key={p.id}
                              className={`text-right text-sm tabular-nums ${
                                isBest
                                  ? "font-semibold text-[#c9ab77]"
                                  : "text-[#8a7a62]"
                              }`}
                            >
                              {price !== undefined ? dollars(price) : "—"}
                            </p>
                          );
                        })}
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// ── Page ─────────────────────────────────────────────────────────

export default function Home() {
  const [selectedTests, setSelectedTests] = useState<string[]>([]);

  const groupedTests = useMemo(() => {
    return labTests.reduce<Record<string, LabTest[]>>((acc, test) => {
      if (!acc[test.category]) acc[test.category] = [];
      acc[test.category].push(test);
      return acc;
    }, {});
  }, []);

  const selectedLabData = useMemo(
    () => labTests.filter((t) => selectedTests.includes(t.id)),
    [selectedTests],
  );

  const totals = useMemo<Totals>(() => {
    const acc: Totals = Object.fromEntries(
      activeProviders.map((p) => [p.id, 0]),
    );
    for (const test of selectedLabData) {
      for (const p of activeProviders) {
        const price = test.pricing[p.id];
        if (price !== undefined) acc[p.id] += price;
      }
    }
    return acc;
  }, [selectedLabData]);

  const cheapestProvider = useMemo(() => {
    return activeProviders
      .map((p) => ({ name: p.label, value: totals[p.id] ?? 0 }))
      .sort((a, b) => a.value - b.value)[0];
  }, [totals]);

  const hasSelection = selectedLabData.length > 0;

  const toggleTest = (id: string) => {
    setSelectedTests((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id],
    );
  };

  return (
    // pb-20 gives clearance for the fixed panel's collapsed bar
    <main className="min-h-screen bg-[#050505] text-[#e7d7b1] pb-20">
      <div className="fixed inset-0 -z-10 bg-[radial-gradient(circle_at_top,rgba(199,168,117,0.14),transparent_28%),radial-gradient(circle_at_bottom,rgba(199,168,117,0.08),transparent_22%)]" />
      <div className="fixed inset-0 -z-10 opacity-[0.08] [background-image:linear-gradient(rgba(231,215,177,0.08)_1px,transparent_1px),linear-gradient(90deg,rgba(231,215,177,0.08)_1px,transparent_1px)] [background-size:44px_44px]" />

      {/* ── Header ── */}
      <header className="sticky top-0 z-50 border-b border-[#3a3124] bg-[#070707]/85 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4 md:px-10">
          <a
            href="#top"
            className="text-2xl font-bold tracking-[0.18em] text-[#f0dfb8]"
          >
            LABRECON
          </a>
          <nav className="hidden gap-6 text-sm font-medium text-[#ceb98e] md:flex">
            <a href="#shop-tests" className="transition hover:text-[#f4e8ca]">
              Shop Tests
            </a>
            <a href="#mission" className="transition hover:text-[#f4e8ca]">
              Mission
            </a>
            <a href="#about" className="transition hover:text-[#f4e8ca]">
              About
            </a>
            <a href="#contact" className="transition hover:text-[#f4e8ca]">
              Contact
            </a>
          </nav>
        </div>
      </header>

      <div className="border-b-2 border-[#c9ab77] bg-[#1a140d] px-6 py-4 text-center text-sm font-bold uppercase tracking-[0.22em] text-[#f6ead0]">
        Work in Progress • Prototype Only • Pricing and features are still being
        built
      </div>

      {/* ── Hero ── */}
      <section id="top" className="border-b border-[#3a3124]">
        <div className="mx-auto grid max-w-7xl gap-12 px-6 py-20 md:px-10 lg:grid-cols-[1.15fr_0.85fr] lg:py-28">
          {/* Left: Copy */}
          <div>
            <div className="mb-5 inline-flex items-center rounded-full border border-[#5a4930] bg-[#11100d] px-4 py-2 text-xs font-semibold uppercase tracking-[0.22em] text-[#c9ab77]">
              Veteran-Owned • No Cost to Consumers
            </div>

            <h1 className="max-w-4xl text-4xl font-bold leading-tight text-[#f6ead0] sm:text-5xl md:text-6xl">
              Compare labwork pricing
              <span className="block text-[#c9ab77]">without the BS.</span>
            </h1>

            <p className="mt-6 max-w-xl text-base leading-8 text-[#cfbe98] sm:text-lg">
              Real self-pay prices from Quest, Labcorp, GoodLabs, and more
              compared side by side in seconds. Free to use. No account
              required.
            </p>

            <div className="mt-8 flex flex-wrap gap-4">
              <a
                href="#shop-tests"
                className="rounded-xl border border-[#c9ab77] bg-[#c9ab77] px-6 py-3 font-semibold text-[#11100d] transition hover:opacity-90"
              >
                Compare Prices
              </a>
              <a
                href="#about"
                className="rounded-xl border border-[#5a4930] bg-[#11100d] px-6 py-3 font-semibold text-[#e7d7b1] transition hover:border-[#c9ab77] hover:text-[#f4e8ca]"
              >
                About the Project
              </a>
            </div>

            <div className="mt-10 grid gap-4 sm:grid-cols-3">
              <div className="rounded-2xl border border-[#3a3124] bg-[#0c0c0b] p-4">
                <p className="text-xs uppercase tracking-[0.18em] text-[#a98a58]">
                  100% Free
                </p>
                <p className="mt-2 text-lg font-semibold text-[#f4e8ca]">
                  No consumer fee
                </p>
              </div>
              <div className="rounded-2xl border border-[#3a3124] bg-[#0c0c0b] p-4">
                <p className="text-xs uppercase tracking-[0.18em] text-[#a98a58]">
                  Compare
                </p>
                <p className="mt-2 text-lg font-semibold text-[#f4e8ca]">
                  Quest • GoodLabs • LabCorp • and more
                </p>
              </div>
              <div className="rounded-2xl border border-[#3a3124] bg-[#0c0c0b] p-4">
                <p className="text-xs uppercase tracking-[0.18em] text-[#a98a58]">
                  No Account
                </p>
                <p className="mt-2 text-lg font-semibold text-[#f4e8ca]">
                  Sign-up for notifications when prices
                </p>
              </div>
            </div>
          </div>

          {/* Right: Static sample preview */}
          <div className="rounded-3xl border border-[#4a3b28] bg-[#090909] p-6 shadow-2xl shadow-black/50">
            <div className="mb-5 border-b border-[#2c2419] pb-4">
              <p className="text-xs uppercase tracking-[0.2em] text-[#aa8d5f]">
                Sample Comparison
              </p>
              <h2 className="mt-2 text-xl font-semibold text-[#f6ead0]">
                See prices side by side
              </h2>
            </div>

            <div className="overflow-hidden rounded-xl border border-[#2c2419]">
              <div className="grid grid-cols-[1fr_64px_76px_68px] border-b border-[#2c2419] bg-[#0c0b09] px-4 py-3">
                <p className="text-xs uppercase tracking-[0.1em] text-[#5a4930]">
                  Test
                </p>
                <p className="text-right text-xs uppercase tracking-[0.1em] text-[#5a4930]">
                  Quest
                </p>
                <p className="text-right text-xs uppercase tracking-[0.1em] text-[#5a4930]">
                  GoodLabs
                </p>
                <p className="text-right text-xs uppercase tracking-[0.1em] text-[#5a4930]">
                  LabCorp
                </p>
              </div>
              {[
                { name: "CBC", quest: 39, goodlabs: 28, labcorp: 35 },
                { name: "Lipid Panel", quest: 42, goodlabs: 26, labcorp: 39 },
                { name: "Testosterone", quest: 69, goodlabs: 45, labcorp: 61 },
              ].map((row, i) => {
                const min = Math.min(row.quest, row.goodlabs, row.labcorp);
                return (
                  <div
                    key={row.name}
                    className={`grid grid-cols-[1fr_64px_76px_68px] items-center px-4 py-3 ${
                      i % 2 === 0 ? "bg-[#0d0c0a]" : "bg-[#0b0a08]"
                    } ${i < 2 ? "border-b border-[#1e1a14]" : ""}`}
                  >
                    <p className="text-sm text-[#e6d5ae]">{row.name}</p>
                    <p
                      className={`text-right text-sm tabular-nums ${row.quest === min ? "font-semibold text-[#c9ab77]" : "text-[#8a7a62]"}`}
                    >
                      ${row.quest}
                    </p>
                    <p
                      className={`text-right text-sm tabular-nums ${row.goodlabs === min ? "font-semibold text-[#c9ab77]" : "text-[#8a7a62]"}`}
                    >
                      ${row.goodlabs}
                    </p>
                    <p
                      className={`text-right text-sm tabular-nums ${row.labcorp === min ? "font-semibold text-[#c9ab77]" : "text-[#8a7a62]"}`}
                    >
                      ${row.labcorp}
                    </p>
                  </div>
                );
              })}
            </div>

            <div className="mt-5 rounded-xl border border-[#2c2419] bg-[#0c0b09] px-4 py-4">
              <p className="text-xs uppercase tracking-[0.14em] text-[#5a4930]">
                Your selection
              </p>
              <p className="mt-2 text-sm leading-7 text-[#7a6a50]">
                Select tests below. Your running total appears at the bottom of
                the screen — collapsed by default, expandable for the full
                breakdown.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ── Shop Tests ── */}
      <section
        id="shop-tests"
        className="mx-auto max-w-7xl px-6 py-20 md:px-10"
      >
        <div className="mb-8 max-w-3xl">
          <p className="text-sm uppercase tracking-[0.22em] text-[#b89a67]">
            Shop Tests
          </p>
          <h2 className="mt-3 text-3xl font-bold text-[#f6ead0] sm:text-4xl">
            Add tests and compare pricing instantly.
          </h2>
          <p className="mt-4 leading-7 text-[#cdbd98]">
            Click any test name to expand details. Select what you need — your
            running total updates at the bottom of the screen.
          </p>
        </div>

        <div className="overflow-hidden rounded-3xl border border-[#3a3124] bg-[#090909]">
          {/* Table header */}
          <div
            className="grid border-b border-[#32281d] bg-[#0f0f0d] px-4 py-4 text-sm font-semibold uppercase tracking-[0.14em] text-[#b89a67]"
            style={{ gridTemplateColumns: shopColTemplate }}
          >
            <div>Test</div>
            {activeProviders.map((p) => (
              <div key={p.id}>{p.label}</div>
            ))}
            <div className="text-right">Add</div>
          </div>

          {/* Category groups */}
          {Object.entries(groupedTests).map(([category, tests]) => (
            <div key={category}>
              <div className="border-b border-[#2a2218] bg-[#0b0b0a] px-4 py-3 text-xs font-semibold uppercase tracking-[0.18em] text-[#9c845c]">
                {category}
              </div>

              {tests.map((test) => (
                <TestRow
                  key={test.id}
                  test={test}
                  isSelected={selectedTests.includes(test.id)}
                  onToggle={() => toggleTest(test.id)}
                />
              ))}
            </div>
          ))}
        </div>

        <p className="mt-6 text-sm text-[#7a6540]">
          Pricing shown is estimated placeholder data for the prototype.
        </p>
      </section>

      {/* ── Mission ── */}
      <section id="mission" className="border-y border-[#3a3124] bg-[#080808]">
        <div className="mx-auto max-w-7xl px-6 py-20 md:px-10">
          <div className="max-w-4xl">
            <p className="text-sm uppercase tracking-[0.22em] text-[#b89a67]">
              Mission
            </p>
            <h2 className="mt-3 text-3xl font-bold text-[#f6ead0] sm:text-4xl">
              Pricing clarity without the runaround.
            </h2>
          </div>

          <div className="mt-10 grid gap-6 md:grid-cols-3">
            <div className="rounded-3xl border border-[#3a3124] bg-[#0d0d0c] p-6">
              <h3 className="text-xl font-semibold text-[#f4e8ca]">
                Why this exists
              </h3>
              <p className="mt-3 leading-7 text-[#cdbd98]">
                Delays, confusion, and opaque pricing around labwork create
                unnecessary stress. LabRecon makes pricing faster to find and
                easier to compare.
              </p>
            </div>
            <div className="rounded-3xl border border-[#3a3124] bg-[#0d0d0c] p-6">
              <h3 className="text-xl font-semibold text-[#f4e8ca]">
                Who it is for
              </h3>
              <p className="mt-3 leading-7 text-[#cdbd98]">
                Veterans, uninsured patients, families paying cash, TRT/HRT
                users, and anyone who wants clearer options before spending
                money on lab testing.
              </p>
            </div>
            <div className="rounded-3xl border border-[#3a3124] bg-[#0d0d0c] p-6">
              <h3 className="text-xl font-semibold text-[#f4e8ca]">
                Core goal
              </h3>
              <p className="mt-3 leading-7 text-[#cdbd98]">
                A free tool that compares pricing honestly, saves time, and
                keeps more money in your pocket.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ── About ── */}
      <section id="about" className="mx-auto max-w-7xl px-6 py-20 md:px-10">
        <div className="grid gap-10 lg:grid-cols-[0.9fr_1.1fr]">
          <div className="relative min-h-[420px] overflow-hidden rounded-3xl border border-[#4a3c29] bg-[#090909]">
            <Image
              src="/about-me.jpg"
              alt="Photo of Quincy"
              fill
              className="object-cover object-top"
              sizes="(max-width: 1024px) 100vw, 45vw"
            />
          </div>

          <div>
            <p className="text-sm uppercase tracking-[0.22em] text-[#b89a67]">
              About Me
            </p>
            <h2 className="mt-3 text-3xl font-bold text-[#f6ead0] sm:text-4xl">
              Built by a disabled USAF veteran trying to make one useful thing.
            </h2>

            <div className="mt-6 space-y-5 text-base leading-8 text-[#cdbd98]">
              <p>
                I created LabRecon because I know firsthand how frustrating it
                is to deal with delays, confusion, and runaround when trying to
                get labwork handled.
              </p>
              <p>
                This is a bootstrap project built by one veteran learning to
                code, learning web development, and learning AI implementation —
                while trying to build something genuinely useful for other
                people.
              </p>
              <p>
                The goal is simple: a free tool that helps users compare labwork
                pricing clearly and make better decisions faster.
              </p>
            </div>

            <div className="mt-8 rounded-2xl border border-[#4f402b] bg-[#0d0d0c] p-5 text-[#d8c59b]">
              <p className="italic leading-8">
                "LabRecon exists because finding labwork pricing should not feel
                like a side mission full of delays, dead ends, and nonsense."
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ── Contact ── */}
      <section id="contact" className="border-t border-[#3a3124] bg-[#080808]">
        <div className="mx-auto max-w-7xl px-6 py-20 md:px-10">
          <p className="text-sm uppercase tracking-[0.22em] text-[#b89a67]">
            Contact
          </p>
          <h2 className="mt-3 text-3xl font-bold text-[#f6ead0] sm:text-4xl">
            Contact LabRecon
          </h2>
          <p className="mt-4 max-w-2xl leading-7 text-[#cdbd98]">
            Questions, feedback, ideas, or partnership conversations.
          </p>

          <div className="mt-8 flex max-w-sm flex-col gap-3">
            {/* Email */}
            <a
              href="mailto:quincy@labrecon.io"
              className="group flex items-center gap-4 rounded-2xl border border-[#3a3124] bg-[#0c0c0b] px-5 py-4 transition hover:border-[#c9ab77]"
            >
              <span className="shrink-0 text-[#a98a58] transition-colors group-hover:text-[#c9ab77]">
                <EmailIcon />
              </span>
              <div className="min-w-0">
                <p className="text-xs uppercase tracking-[0.16em] text-[#a98a58]">
                  Email
                </p>
                <p className="mt-0.5 truncate font-semibold text-[#f4e8ca]">
                  quincy@labrecon.io
                </p>
              </div>
            </a>

            {/* LinkedIn */}
            <a
              href="https://www.linkedin.com/in/quincywestbrook"
              target="_blank"
              rel="noopener noreferrer"
              className="group flex items-center gap-4 rounded-2xl border border-[#3a3124] bg-[#0c0c0b] px-5 py-4 transition hover:border-[#c9ab77]"
            >
              <span className="shrink-0 text-[#a98a58] transition-colors group-hover:text-[#c9ab77]">
                <LinkedInIcon />
              </span>
              <p className="font-semibold text-[#f4e8ca]">LinkedIn</p>
            </a>

            {/* Reddit */}
            <a
              href="https://www.reddit.com/r/LabRecon"
              target="_blank"
              rel="noopener noreferrer"
              className="group flex items-center gap-4 rounded-2xl border border-[#3a3124] bg-[#0c0c0b] px-5 py-4 transition hover:border-[#c9ab77]"
            >
              <span className="shrink-0 text-[#a98a58] transition-colors group-hover:text-[#c9ab77]">
                <RedditIcon />
              </span>
              <p className="font-semibold text-[#f4e8ca]">Reddit</p>
            </a>
          </div>

          <p className="mt-10 text-sm text-[#a89268]">
            LabRecon is intended to help users compare pricing and reduce
            friction. It is not a medical provider and does not provide medical
            advice.
          </p>
        </div>
      </section>

      {/* ── Fixed Running Total Panel ── */}
      <RunningTotalPanel
        selectedLabData={selectedLabData}
        totals={totals}
        cheapestProvider={cheapestProvider}
        hasSelection={hasSelection}
      />
    </main>
  );
}
