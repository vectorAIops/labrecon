"use client";

import { useMemo, useState } from "react";

type LabItem = {
  id: string;
  name: string;
  category: string;
  quest: number;
  goodlabs: number;
  labcorp: number;
};

const labTests: LabItem[] = [
  { id: "cbc", name: "Complete Blood Count (CBC)", category: "General", quest: 39, goodlabs: 28, labcorp: 35 },
  { id: "cmp", name: "Comprehensive Metabolic Panel (CMP)", category: "General", quest: 49, goodlabs: 31, labcorp: 42 },
  { id: "lipid", name: "Lipid Panel", category: "Cardio / Metabolic", quest: 42, goodlabs: 26, labcorp: 39 },
  { id: "a1c", name: "Hemoglobin A1C", category: "Cardio / Metabolic", quest: 34, goodlabs: 24, labcorp: 31 },
  { id: "tsh", name: "TSH", category: "Thyroid", quest: 44, goodlabs: 29, labcorp: 41 },
  { id: "ft4", name: "Free T4", category: "Thyroid", quest: 47, goodlabs: 30, labcorp: 44 },
  { id: "vitd", name: "Vitamin D, 25-OH", category: "Vitamins", quest: 69, goodlabs: 45, labcorp: 61 },
  { id: "b12", name: "Vitamin B12", category: "Vitamins", quest: 54, goodlabs: 34, labcorp: 49 },
  { id: "ferritin", name: "Ferritin", category: "Iron", quest: 46, goodlabs: 33, labcorp: 43 },
  { id: "iron", name: "Iron / TIBC Panel", category: "Iron", quest: 62, goodlabs: 39, labcorp: 57 },
  { id: "total-test", name: "Testosterone, Total", category: "Hormones", quest: 69, goodlabs: 45, labcorp: 61 },
  { id: "free-test", name: "Testosterone, Free", category: "Hormones", quest: 79, goodlabs: 51, labcorp: 72 },
  { id: "estradiol", name: "Estradiol", category: "Hormones", quest: 58, goodlabs: 38, labcorp: 53 },
  { id: "shbg", name: "SHBG", category: "Hormones", quest: 67, goodlabs: 44, labcorp: 61 },
  { id: "psa", name: "PSA", category: "Men's Health", quest: 41, goodlabs: 27, labcorp: 38 },
];

function dollars(value: number) {
  return `$${value.toFixed(2)}`;
}

export default function Home() {
  const [selectedTests, setSelectedTests] = useState<string[]>([]);

  const groupedTests = useMemo(() => {
    return labTests.reduce<Record<string, LabItem[]>>((acc, test) => {
      if (!acc[test.category]) acc[test.category] = [];
      acc[test.category].push(test);
      return acc;
    }, {});
  }, []);

  const selectedLabData = useMemo(() => {
    return labTests.filter((test) => selectedTests.includes(test.id));
  }, [selectedTests]);

  const totals = useMemo(() => {
    return selectedLabData.reduce(
      (acc, test) => {
        acc.quest += test.quest;
        acc.goodlabs += test.goodlabs;
        acc.labcorp += test.labcorp;
        return acc;
      },
      { quest: 0, goodlabs: 0, labcorp: 0 }
    );
  }, [selectedLabData]);

  const cheapestProvider = useMemo(() => {
    const entries = [
      { name: "Quest", value: totals.quest },
      { name: "GoodLabs", value: totals.goodlabs },
      { name: "LabCorp", value: totals.labcorp },
    ];

    return entries.sort((a, b) => a.value - b.value)[0];
  }, [totals]);

  const toggleTest = (id: string) => {
    setSelectedTests((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]
    );
  };

  return (
    <main className="min-h-screen bg-[#050505] text-[#e7d7b1]">
      <div className="fixed inset-0 -z-10 bg-[radial-gradient(circle_at_top,rgba(199,168,117,0.14),transparent_28%),radial-gradient(circle_at_bottom,rgba(199,168,117,0.08),transparent_22%)]" />
      <div className="fixed inset-0 -z-10 opacity-[0.08] [background-image:linear-gradient(rgba(231,215,177,0.08)_1px,transparent_1px),linear-gradient(90deg,rgba(231,215,177,0.08)_1px,transparent_1px)] [background-size:44px_44px]" />

      <header className="sticky top-0 z-50 border-b border-[#3a3124] bg-[#070707]/85 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4 md:px-10">
        <a href="#top" className="text-2xl font-bold tracking-[0.18em] text-[#f0dfb8]">
  LABRECON
</a>

          <nav className="hidden gap-6 text-sm font-medium text-[#ceb98e] md:flex">
            <a href="#shop-tests" className="transition hover:text-[#f4e8ca]">Shop Tests</a>
            <a href="#mission" className="transition hover:text-[#f4e8ca]">Mission</a>
            <a href="#about" className="transition hover:text-[#f4e8ca]">About</a>
            <a href="#contact" className="transition hover:text-[#f4e8ca]">Contact</a>
          </nav>
        </div>
      </header>
      <div className="border-b-2 border-[#c9ab77] bg-[#1a140d] px-6 py-4 text-center text-sm font-bold uppercase tracking-[0.22em] text-[#f6ead0]">
  <div className="animate-pulse">
    Work in Progress Test Page • Prototype Only • Pricing and features are still being built
  </div>
</div>
      <section id="top" className="border-b border-[#3a3124]">
        <div className="mx-auto grid max-w-7xl gap-12 px-6 py-20 md:px-10 lg:grid-cols-[1.15fr_0.85fr] lg:py-28">
          <div>
            <div className="mb-5 inline-flex items-center rounded-full border border-[#5a4930] bg-[#11100d] px-4 py-2 text-xs font-semibold uppercase tracking-[0.22em] text-[#c9ab77]">
              Veteran-Owned • No Cost to Consumers
            </div>

            <h1 className="max-w-4xl text-4xl font-bold leading-tight text-[#f6ead0] sm:text-5xl md:text-6xl">
              Compare labwork pricing
              <span className="block text-[#c9ab77]">without the BS.</span>
            </h1>

            <p className="mt-6 max-w-3xl text-base leading-8 text-[#cfbe98] sm:text-lg">
              LabRecon was created to help veterans and everyday Americans find
              lower labwork pricing without the usual headache. This site exists
              because getting timely labwork should not require endless phone
              calls, delays, or unnecessary runaround.
            </p>

            <p className="mt-5 max-w-3xl text-base leading-8 text-[#bda882]">
              Built by a single disabled USAF veteran learning code, web
              development, and AI implementation, LabRecon is meant to be useful,
              direct, and free to the people using it.
            </p>

            <div className="mt-8 flex flex-wrap gap-4">
              <a
                href="#shop-tests"
                className="rounded-xl border border-[#c9ab77] bg-[#c9ab77] px-6 py-3 font-semibold text-[#11100d] transition hover:opacity-90"
              >
                Shop Tests
              </a>
              <a
                href="#mission"
                className="rounded-xl border border-[#5a4930] bg-[#11100d] px-6 py-3 font-semibold text-[#e7d7b1] transition hover:border-[#c9ab77] hover:text-[#f4e8ca]"
              >
                See the Mission
              </a>
            </div>

            <div className="mt-10 grid gap-4 sm:grid-cols-3">
              <div className="rounded-2xl border border-[#3a3124] bg-[#0c0c0b] p-4">
                <p className="text-xs uppercase tracking-[0.18em] text-[#a98a58]">100% Free</p>
                <p className="mt-2 text-lg font-semibold text-[#f4e8ca]">
                  No consumer fee
                </p>
              </div>

              <div className="rounded-2xl border border-[#3a3124] bg-[#0c0c0b] p-4">
                <p className="text-xs uppercase tracking-[0.18em] text-[#a98a58]">Compare</p>
                <p className="mt-2 text-lg font-semibold text-[#f4e8ca]">
                  Quest • GoodLabs • LabCorp
                </p>
              </div>

              <div className="rounded-2xl border border-[#3a3124] bg-[#0c0c0b] p-4">
                <p className="text-xs uppercase tracking-[0.18em] text-[#a98a58]">Built By</p>
                <p className="mt-2 text-lg font-semibold text-[#f4e8ca]">
                  Disabled USAF veteran
                </p>
              </div>
            </div>
          </div>

          <div className="rounded-3xl border border-[#4a3b28] bg-[#090909] p-6 shadow-2xl shadow-black/50">
            <div className="mb-4 flex items-center justify-between border-b border-[#2c2419] pb-4">
              <div>
                <p className="text-xs uppercase tracking-[0.2em] text-[#aa8d5f]">
                  Live comparison concept
                </p>
                <h2 className="mt-2 text-2xl font-semibold text-[#f6ead0]">
                  Running total preview
                </h2>
              </div>
              <span className="rounded-full border border-[#5c4a31] px-3 py-1 text-xs uppercase tracking-[0.18em] text-[#c9ab77]">
                V1
              </span>
            </div>

            <div className="space-y-3">
              {selectedLabData.length === 0 ? (
                <div className="rounded-2xl border border-dashed border-[#4c3d2a] bg-[#10100e] p-5 text-sm leading-7 text-[#c8b48c]">
                  Pick tests below and LabRecon will keep a running total for Quest,
                  GoodLabs, and LabCorp.
                </div>
              ) : (
                selectedLabData.map((test) => (
                  <div
                    key={test.id}
                    className="rounded-2xl border border-[#32281d] bg-[#0f0e0c] p-4"
                  >
                    <div className="mb-3 flex items-center justify-between">
                      <p className="font-semibold text-[#f4e8ca]">{test.name}</p>
                      <span className="text-xs uppercase tracking-[0.18em] text-[#a88c61]">
                        Selected
                      </span>
                    </div>

                    <div className="grid grid-cols-3 gap-3 text-sm">
                      <div className="rounded-xl border border-[#3a3124] bg-[#15120d] p-3">
                        <p className="text-xs uppercase tracking-[0.14em] text-[#9f8558]">Quest</p>
                        <p className="mt-2 text-lg font-bold text-[#f2dfb5]">{dollars(test.quest)}</p>
                      </div>
                      <div className="rounded-xl border border-[#3a3124] bg-[#15120d] p-3">
                        <p className="text-xs uppercase tracking-[0.14em] text-[#9f8558]">GoodLabs</p>
                        <p className="mt-2 text-lg font-bold text-[#f2dfb5]">{dollars(test.goodlabs)}</p>
                      </div>
                      <div className="rounded-xl border border-[#3a3124] bg-[#15120d] p-3">
                        <p className="text-xs uppercase tracking-[0.14em] text-[#9f8558]">LabCorp</p>
                        <p className="mt-2 text-lg font-bold text-[#f2dfb5]">{dollars(test.labcorp)}</p>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>

            <div className="mt-5 rounded-2xl border border-[#5a4930] bg-[#11100d] p-5">
              <p className="text-xs uppercase tracking-[0.18em] text-[#a88c61]">
                Running total
              </p>

              <div className="mt-4 grid gap-3 sm:grid-cols-3">
                <div className="rounded-xl border border-[#3a3124] bg-[#090909] p-4">
                  <p className="text-xs uppercase tracking-[0.14em] text-[#9f8558]">Quest</p>
                  <p className="mt-2 text-2xl font-bold text-[#f6ead0]">{dollars(totals.quest)}</p>
                </div>
                <div className="rounded-xl border border-[#3a3124] bg-[#090909] p-4">
                  <p className="text-xs uppercase tracking-[0.14em] text-[#9f8558]">GoodLabs</p>
                  <p className="mt-2 text-2xl font-bold text-[#f6ead0]">{dollars(totals.goodlabs)}</p>
                </div>
                <div className="rounded-xl border border-[#3a3124] bg-[#090909] p-4">
                  <p className="text-xs uppercase tracking-[0.14em] text-[#9f8558]">LabCorp</p>
                  <p className="mt-2 text-2xl font-bold text-[#f6ead0]">{dollars(totals.labcorp)}</p>
                </div>
              </div>

              <p className="mt-4 text-sm text-[#ccb88f]">
                Cheapest current total:{" "}
                <span className="font-semibold text-[#f4e8ca]">
                  {selectedLabData.length > 0 ? `${cheapestProvider.name} (${dollars(cheapestProvider.value)})` : "Select tests to compare"}
                </span>
              </p>
            </div>
          </div>
        </div>
      </section>

      <section id="shop-tests" className="mx-auto max-w-7xl px-6 py-20 md:px-10">
        <div className="mb-8 max-w-3xl">
          <p className="text-sm uppercase tracking-[0.22em] text-[#b89a67]">Shop Tests</p>
          <h2 className="mt-3 text-3xl font-bold text-[#f6ead0] sm:text-4xl">
            Add tests and compare pricing instantly.
          </h2>
          <p className="mt-4 leading-7 text-[#cdbd98]">
            This concept page shows how users can select labs and watch totals
            update across providers. The goal is simple: lower confusion, lower
            wasted time, and clearer pricing.
          </p>
        </div>

        <div className="overflow-hidden rounded-3xl border border-[#3a3124] bg-[#090909]">
          <div className="grid grid-cols-[1.6fr_0.5fr_0.5fr_0.5fr_0.45fr] border-b border-[#32281d] bg-[#0f0f0d] px-4 py-4 text-sm font-semibold uppercase tracking-[0.14em] text-[#b89a67]">
            <div>Test</div>
            <div>Quest</div>
            <div>GoodLabs</div>
            <div>LabCorp</div>
            <div className="text-right">Add</div>
          </div>

          {Object.entries(groupedTests).map(([category, tests]) => (
            <div key={category}>
              <div className="border-b border-[#2a2218] bg-[#0b0b0a] px-4 py-3 text-xs font-semibold uppercase tracking-[0.18em] text-[#9c845c]">
                {category}
              </div>

              {tests.map((test) => {
                const active = selectedTests.includes(test.id);

                return (
                  <div
                    key={test.id}
                    className="grid grid-cols-[1.6fr_0.5fr_0.5fr_0.5fr_0.45fr] items-center border-b border-[#221c14] px-4 py-4 text-sm text-[#e6d5ae]"
                  >
                    <div>
                      <p className="font-medium text-[#f4e8ca]">{test.name}</p>
                    </div>
                    <div>{dollars(test.quest)}</div>
                    <div>{dollars(test.goodlabs)}</div>
                    <div>{dollars(test.labcorp)}</div>
                    <div className="text-right">
                      <button
                        onClick={() => toggleTest(test.id)}
                        className={`rounded-lg px-4 py-2 text-xs font-semibold uppercase tracking-[0.12em] transition ${
                          active
                            ? "border border-[#7c6743] bg-[#1f1911] text-[#f2dfb5]"
                            : "border border-[#4b3d2a] bg-[#11100d] text-[#cfbe98] hover:border-[#c9ab77] hover:text-[#f4e8ca]"
                        }`}
                      >
                        {active ? "Remove" : "Add"}
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          ))}
        </div>

        <div className="mt-8 rounded-3xl border border-[#4d3e2b] bg-[#0a0a09] p-6">
          <h3 className="text-xl font-semibold text-[#f6ead0]">Selected totals</h3>
          <div className="mt-5 grid gap-4 md:grid-cols-3">
            <div className="rounded-2xl border border-[#3a3124] bg-[#11100d] p-5">
              <p className="text-xs uppercase tracking-[0.14em] text-[#a98a58]">Quest</p>
              <p className="mt-2 text-3xl font-bold text-[#f4e8ca]">{dollars(totals.quest)}</p>
            </div>
            <div className="rounded-2xl border border-[#3a3124] bg-[#11100d] p-5">
              <p className="text-xs uppercase tracking-[0.14em] text-[#a98a58]">GoodLabs</p>
              <p className="mt-2 text-3xl font-bold text-[#f4e8ca]">{dollars(totals.goodlabs)}</p>
            </div>
            <div className="rounded-2xl border border-[#3a3124] bg-[#11100d] p-5">
              <p className="text-xs uppercase tracking-[0.14em] text-[#a98a58]">LabCorp</p>
              <p className="mt-2 text-3xl font-bold text-[#f4e8ca]">{dollars(totals.labcorp)}</p>
            </div>
          </div>

          <p className="mt-5 text-sm leading-7 text-[#c7b58f]">
            Pricing shown here is sample placeholder data for the prototype. You
            can later replace it with your real comparison data from Quest,
            GoodLabs, and LabCorp.
          </p>
        </div>
      </section>

      <section id="mission" className="border-y border-[#3a3124] bg-[#080808]">
        <div className="mx-auto max-w-7xl px-6 py-20 md:px-10">
          <div className="max-w-4xl">
            <p className="text-sm uppercase tracking-[0.22em] text-[#b89a67]">Mission</p>
            <h2 className="mt-3 text-3xl font-bold text-[#f6ead0] sm:text-4xl">
              A straightforward tool built to help people get pricing clarity without the runaround.
            </h2>
          </div>

          <div className="mt-10 grid gap-6 md:grid-cols-3">
            <div className="rounded-3xl border border-[#3a3124] bg-[#0d0d0c] p-6">
              <h3 className="text-xl font-semibold text-[#f4e8ca]">Why this exists</h3>
              <p className="mt-3 leading-7 text-[#cdbd98]">
                Delays, confusion, and broken communication around labwork can
                create unnecessary stress. LabRecon aims to make pricing faster
                to find and easier to compare.
              </p>
            </div>

            <div className="rounded-3xl border border-[#3a3124] bg-[#0d0d0c] p-6">
              <h3 className="text-xl font-semibold text-[#f4e8ca]">Who it is for</h3>
              <p className="mt-3 leading-7 text-[#cdbd98]">
                Veterans, uninsured patients, families paying cash, and anyone
                who wants clearer options before spending money on lab testing.
              </p>
            </div>

            <div className="rounded-3xl border border-[#3a3124] bg-[#0d0d0c] p-6">
              <h3 className="text-xl font-semibold text-[#f4e8ca]">Core goal</h3>
              <p className="mt-3 leading-7 text-[#cdbd98]">
                Give people a no-cost tool that compares pricing cleanly,
                honestly, and in a way that saves time instead of wasting it.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section id="about" className="mx-auto max-w-7xl px-6 py-20 md:px-10">
        <div className="grid gap-10 lg:grid-cols-[0.9fr_1.1fr]">
          <div className="overflow-hidden rounded-3xl border border-[#4a3c29] bg-[#090909]">
            <div className="flex min-h-[420px] items-center justify-center bg-[#0d0d0c] text-center text-[#bda882]">
              <div>
                <p className="text-sm uppercase tracking-[0.2em] text-[#a98a58]">
                  About Photo
                </p>
                <p className="mt-3 text-lg font-semibold text-[#f4e8ca]">
                  Photo coming soon
                </p>
              </div>
            </div>
          </div>

          <div>
            <p className="text-sm uppercase tracking-[0.22em] text-[#b89a67]">About Me</p>
            <h2 className="mt-3 text-3xl font-bold text-[#f6ead0] sm:text-4xl">
              Built by a disabled USAF veteran trying to make one useful thing.
            </h2>

            <div className="mt-6 space-y-5 text-base leading-8 text-[#cdbd98]">
              <p>
                I created LabRecon because I know firsthand how frustrating it
                can be to deal with delays, confusion, and extra headaches when
                trying to get labwork handled in a timely way.
              </p>

              <p>
                This project is being built by one veteran learning to code, web
                development, and AI implementation while trying to create
                something genuinely useful for other people.
              </p>

              <p>
                The goal is not to sell people on fluff. The goal is to build a
                free tool that helps users compare labwork pricing clearly and
                make better decisions faster.
              </p>
            </div>

            <div className="mt-8 rounded-2xl border border-[#4f402b] bg-[#0d0d0c] p-5 text-[#d8c59b]">
              <p className="italic leading-8">
                “LabRecon exists because finding labwork pricing should not feel
                like a side mission full of delays, dead ends, and nonsense.”
              </p>
            </div>
          </div>
        </div>
      </section>

      <section id="contact" className="border-t border-[#3a3124] bg-[#080808]">
        <div className="mx-auto max-w-7xl px-6 py-20 md:px-10">
          <p className="text-sm uppercase tracking-[0.22em] text-[#b89a67]">Contact</p>
          <h2 className="mt-3 text-3xl font-bold text-[#f6ead0] sm:text-4xl">
            Contact LabRecon
          </h2>
          <p className="mt-4 max-w-2xl leading-7 text-[#cdbd98]">
            Questions, ideas, feedback, or partnership conversations can go here.
          </p>

          <div className="mt-8 max-w-xl">
            <a
              href="mailto:quincy@labrecon.io"
              className="rounded-3xl border border-[#3a3124] bg-[#0c0c0b] p-6 transition hover:border-[#c9ab77]"
            >
              <p className="text-xs uppercase tracking-[0.18em] text-[#a98a58]">Email</p>
              <p className="mt-3 text-xl font-semibold text-[#f4e8ca]">
                quincy@labrecon.io
              </p>
            </a>


          </div>

          <p className="mt-10 text-sm text-[#a89268]">
            LabRecon is intended to help users compare pricing and reduce
            friction. It is not a medical provider and does not provide medical advice.
          </p>
        </div>
      </section>
    </main>
  );
}