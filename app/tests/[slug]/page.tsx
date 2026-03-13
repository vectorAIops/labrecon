import type { Metadata } from "next";
import Link from "next/link";
import { labTests, activeProviders } from "../../data/labTests";

// URLs that link to a general catalog rather than a specific product.
const BASE_CATALOG_URLS = new Set([
  "https://www.questhealth.com/shop-tests",
  "https://app.hellogoodlabs.com/book-tests",
]);

function dollars(value: number) {
  return `$${value.toFixed(2)}`;
}

// ── Static generation ──────────────────────────────────────────────────────

export function generateStaticParams() {
  return labTests
    .filter((t) => !t.bundle)
    .map((t) => ({ slug: t.id }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const test = labTests.find((t) => t.id === slug);
  if (!test) return {};
  return {
    title: `${test.displayName} — Compare Self-Pay Prices | LabRecon`,
    description: `Compare self-pay ${test.canonicalName.toLowerCase()} prices from Quest, LabCorp, and GoodLabs. No insurance needed. Prices verified ${test.lastVerified}.`,
  };
}

// ── Page ──────────────────────────────────────────────────────────────────

export default async function TestPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const test = labTests.find((t) => t.id === slug);

  if (!test) {
    return (
      <main className="min-h-screen bg-[#050505] text-[#e7d7b1] px-5 py-16">
        <p className="text-[#6b5535]">Test not found.</p>
        <Link
          href="/"
          className="mt-4 inline-block text-sm text-[#c9ab77] hover:text-[#f4e8ca]"
        >
          ← Back to all tests
        </Link>
      </main>
    );
  }

  // Determine best (lowest) price among providers that have one.
  const validPrices = activeProviders
    .map((p) => test.pricing[p.id])
    .filter((v): v is number => v !== undefined && v !== null);
  const minPrice = validPrices.length > 0 ? Math.min(...validPrices) : null;

  return (
    <main className="min-h-screen bg-[#050505] text-[#e7d7b1]">
      <div className="mx-auto max-w-3xl px-5 py-12 sm:px-8">

        {/* Back link */}
        <Link
          href="/"
          className="mb-8 inline-flex items-center gap-1.5 text-xs uppercase tracking-[0.14em] text-[#5a4930] transition hover:text-[#c9ab77]"
        >
          ← Back to all tests
        </Link>

        {/* Header */}
        <h1 className="mt-2 text-2xl font-bold text-[#f4e8ca] sm:text-3xl">
          {test.displayName}
        </h1>
        <p className="mt-1 text-xs uppercase tracking-[0.14em] text-[#5a4930]">
          {test.category}
        </p>

        {/* Plain description */}
        <p className="mt-5 text-sm leading-7 text-[#cdbd98]">
          {test.plainDescription}
        </p>

        {/* ── Price comparison table ── */}
        <div className="mt-10">
          <p className="mb-4 text-xs uppercase tracking-[0.2em] text-[#5a4930]">
            Self-pay prices
          </p>

          <div className="overflow-hidden rounded-xl border border-[#2a2218]">
            {activeProviders.map((p, i) => {
              const price = test.pricing[p.id];
              const url = test.orderUrls?.[p.id];
              const isBest =
                price !== null && price !== undefined && price === minPrice;
              const isLast = i === activeProviders.length - 1;
              const hasOrder =
                price !== null && price !== undefined && url != null;
              const isBase = url != null && BASE_CATALOG_URLS.has(url);

              return (
                <div
                  key={p.id}
                  className={`flex items-center justify-between gap-4 px-5 py-4 ${
                    !isLast ? "border-b border-[#1e1a14]" : ""
                  } ${i % 2 === 0 ? "bg-[#0d0c0a]" : "bg-[#0b0a08]"}`}
                >
                  {/* Provider name */}
                  <span className="text-sm font-medium text-[#9f8558]">
                    {p.label}
                  </span>

                  {/* Price + button */}
                  <div className="flex items-center gap-4">
                    <span
                      className={`text-sm tabular-nums ${
                        isBest
                          ? "font-semibold text-[#c9ab77]"
                          : price === null
                          ? "text-xs text-[#4a4030]"
                          : "text-[#e6d5ae]"
                      }`}
                    >
                      {price === null
                        ? "Not available"
                        : price !== undefined
                        ? dollars(price)
                        : "—"}
                    </span>

                    {isBest && (
                      <span className="rounded-full border border-[#5a4930] bg-[#1a1510] px-2 py-0.5 text-xs uppercase tracking-[0.1em] text-[#c9ab77]">
                        Best price
                      </span>
                    )}

                    {hasOrder && (
                      <a
                        href={url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="rounded-lg border border-[#4b3d2a] bg-[#11100d] px-3 py-1.5 text-xs font-semibold text-[#cfbe98] transition hover:border-[#c9ab77] hover:text-[#f4e8ca]"
                      >
                        {isBase ? "View catalog" : "Order"}
                      </a>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* ── Biomarkers ── */}
        {test.biomarkers.length > 0 && (
          <div className="mt-10">
            <p className="mb-3 text-xs uppercase tracking-[0.2em] text-[#5a4930]">
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
        )}

        {/* ── Clinical notes ── */}
        {test.medicalDescription && (
          <div className="mt-10">
            <p className="mb-2 text-xs uppercase tracking-[0.16em] text-[#5a4930]">
              Clinical notes
            </p>
            <p className="text-sm leading-7 text-[#8a7a62]">
              {test.medicalDescription}
            </p>
          </div>
        )}

        {/* ── Ordering note ── */}
        {test.notes && (
          <div className="mt-6 rounded-lg border border-[#2a2218] bg-[#0d0c0a] px-4 py-3">
            <p className="mb-1 text-xs uppercase tracking-[0.12em] text-[#5a4930]">
              Ordering note
            </p>
            <p className="text-xs leading-6 text-[#7a6a50]">{test.notes}</p>
          </div>
        )}

        {/* ── Footer ── */}
        <p className="mt-10 text-xs text-[#3a3124]">
          Prices verified: {test.lastVerified}
        </p>
      </div>
    </main>
  );
}
