# LabRecon.io — Master Reference

**Last updated:** March 12, 2026
**Repo:** github.com/vectorAIops/labrecon
**Live:** labrecon.vercel.app (target: labrecon.io)
**Stack:** Next.js (App Router), TypeScript, Tailwind, Vercel, Cloudflare, GitHub

---

## Table of Contents

1. [Quick Status](#1-quick-status)
2. [To-Do Checklist](#2-to-do-checklist)
3. [MVP Build Steps](#3-mvp-build-steps)
4. [Repo Structure](#4-repo-structure)
5. [Git & Cursor Quick Reference](#5-git--cursor-quick-reference)
6. [Claude Code Prompt Templates](#6-claude-code-prompt-templates)
7. [Key Decisions Pending](#7-key-decisions-pending)
8. [Risks & Flags](#8-risks--flags)
9. [What NOT to Do Yet](#9-what-not-to-do-yet)
10. [Success Metrics](#10-success-metrics)
11. [Learning Path](#11-learning-path)

---

## 1. Quick Status

**What exists today:**
- Single-page app with 21 tests across 7 categories
- 3 providers: Quest, LabCorp, GoodLabs
- Expandable test cards with descriptions, clinical notes, biomarkers
- Add-to-cart system with per-provider price breakdown
- Mobile responsive, medical disclaimer, trust banners
- Scraper codebase with provider modules (Quest, LabCorp, GoodLabs)
- Compliance documentation (robots.txt screenshots)

**What's broken or missing:**
- All prices are placeholder/estimated (CRITICAL)
- No outbound links to providers — all point to `#` (CRITICAL)
- No individual test pages — everything on one URL (HIGH)
- No sitemap.xml, robots.txt, or meta tags (HIGH)
- No analytics (MEDIUM)
- ZIP code field does nothing (LOW)
- Domain config (labrecon.io) unverified (UNKNOWN)

---

## 2. To-Do Checklist

Check these off as you complete them. Ordered by dependency — don't skip ahead.

### Pre-Launch (Must Do)
- [ ] Run repo security audit (secrets scan, .gitignore fix)
- [ ] Move compliance screenshots to `scraper/compliance/`
- [ ] Move loose Python scripts to `scripts/`
- [ ] Remove tracked `__pycache__/` and `.git.zip` from Git
- [ ] Verify all 63 prices (21 tests × 3 providers) — record in spreadsheet
- [ ] Update data file with real prices + provider URLs + verification dates
- [ ] Replace "placeholder data" banner with "Prices last verified: [date]"

### Week 1–2: Pages & Links
- [ ] Create `app/tests/[slug]/page.tsx` dynamic route
- [ ] Generate 21 individual test pages with unique URLs
- [ ] Add `generateStaticParams()` for static generation
- [ ] Add `generateMetadata()` for per-page SEO tags
- [ ] Replace all `href="#"` with real provider order page URLs
- [ ] All outbound links: `target="_blank" rel="noopener noreferrer"`

### Week 2: SEO & Analytics
- [ ] Add `app/robots.ts`
- [ ] Add `app/sitemap.ts`
- [ ] Verify labrecon.io domain config (Cloudflare DNS → Vercel)
- [ ] Verify HTTPS and redirect from labrecon.vercel.app → labrecon.io
- [ ] Add Open Graph tags to all pages
- [ ] Submit sitemap to Google Search Console
- [ ] Enable Vercel Analytics (or Plausible/Umami)

### Week 3: Polish
- [ ] Update or remove "Prototype Only" banner
- [ ] Handle ZIP code field (remove or label "coming soon")
- [ ] Add "How this works" FAQ section
- [ ] Run Lighthouse audit — fix red/orange items
- [ ] Verify medical disclaimer is visible but not overbearing

### Week 3–4: Expand
- [ ] Research 2–3 additional providers (Walk-In Lab, Ulta Lab Tests, HealthLabs.com)
- [ ] Add best-match providers to data file and comparison tables
- [ ] Check each provider for affiliate programs

### Week 4+: Monetize & Grow
- [ ] Apply to affiliate programs (start with whichever providers respond)
- [ ] Replace standard outbound links with affiliate tracking links
- [ ] Begin expanding test catalog toward 30–50 tests
- [ ] Prioritize new tests by search volume (Google Keyword Planner / Ubersuggest)

### Ongoing
- [ ] Monthly price verification (set calendar reminder)
- [ ] Monitor Google Search Console for indexing issues
- [ ] Track outbound link clicks in analytics
- [ ] Follow up with GoodLabs if no response within 2 weeks

---

## 3. MVP Build Steps

### Step 1: Verify Real Pricing (Week 1)

63 prices to verify: 21 tests × 3 providers.

**Where to look:**
- GoodLabs: app.hellogoodlabs.com/book-tests
- Quest: questhealth.com (DTC consumer site)
- LabCorp: labcorp.com/tests or OnDemand site

Record for each: test name, provider, price, order page URL, date verified.

If a provider doesn't offer a test → show "Not available" (don't omit the row).
Quest/LabCorp DTC prices may differ from GoodLabs prices — that's expected, show all three.

### Step 2: Individual Test Pages (Week 1–2)

Create `app/tests/[slug]/page.tsx`. Each page gets:
- Test name as H1
- Plain-English description
- Clinical notes (collapsible)
- Biomarkers included
- Price comparison table with "Order from [Provider]" buttons
- Fasting/prep requirements
- "Last verified" date
- Link back to full test list

SEO tags per page:
- Title: `CBC Blood Test — Compare Prices | LabRecon`
- Description: `Compare self-pay CBC prices from Quest ($X), LabCorp ($X), and GoodLabs ($X). No insurance needed.`

Key Next.js concepts: `generateStaticParams()`, `generateMetadata()`, dynamic `[slug]` routes.

### Step 3: Working Outbound Links (Week 2)

Replace every `href="#"` with real provider order page URLs. Store URLs in data file alongside prices. All outbound links open in new tab.

GoodLabs-specific: use tracked/affiliate links if confirmed, standard links if not yet.

### Step 4: SEO Foundation (Week 2)

- `app/robots.ts` — allow all crawling, reference sitemap
- `app/sitemap.ts` — include `/`, all `/tests/[slug]` pages
- Verify domain config: Cloudflare → Vercel → HTTPS → redirect .vercel.app to .io
- Open Graph tags on all pages
- Submit sitemap to Google Search Console

### Step 5: Analytics (Week 2)

Enable Vercel Analytics (free tier). Track page views, test page traffic, outbound clicks. Needed to prove traffic to future affiliate partners.

### Step 6: Trust & UX Cleanup (Week 3)

Update/remove prototype banner. Handle ZIP field. Add FAQ. Run Lighthouse audit.

### Step 7: More Providers (Week 3–4)

Target 5–6 total. Research: Walk-In Lab, Ulta Lab Tests, HealthLabs.com, Request A Test, Direct Labs. Most are DTC resellers using Quest/LabCorp — same fulfillment, different prices. That's exactly the value LabRecon provides.

### Step 8: Expand Test Coverage (Week 4+)

Target 30–50 tests. Priority additions:
- Metabolic: Glucose (fasting), Uric Acid, Magnesium (RBC)
- Liver: Hepatic Function Panel, GGT
- Kidney: Cystatin C, Microalbumin/Creatinine Ratio
- Hormones: DHEA-S, Cortisol, Progesterone, LH, FSH, Prolactin
- Thyroid: Free T3, Reverse T3, TPO, TgAb
- STI: HIV, Hepatitis B/C, Chlamydia/Gonorrhea, Syphilis
- Inflammation: ESR, Homocysteine
- Nutrients: Folate, Zinc, Vitamin A
- Allergy/Immune: ANA, IgE Total
- Men's: Free PSA

Prioritize by search volume — don't add everything at once.

### Step 9: Monetization (Week 4–6)

Wait for GoodLabs response. Then:

| GoodLabs says... | You do... |
|---|---|
| Has/will create affiliate program | Apply immediately (76 referrals = proof of value) |
| Allows tracked links or coupons | Use on all GoodLabs links, track conversion |
| Doesn't want prices displayed | Show "Check price at GoodLabs" link instead |
| No restrictions | Continue as-is |
| No response | Follow up in 2 weeks. Apply to other provider affiliate programs. |

Also apply to affiliate programs at all other listed providers.

### Step 10: Content & SEO Growth (Ongoing)

Add `/blog` or `/guides`:
- "What blood tests should I get annually?"
- "CBC vs CMP — what's the difference?"
- "How to get blood work without insurance"
- "Testosterone testing guide for men"

Target long-tail keywords. Add JSON-LD structured data to test pages.

---

## 4. Repo Structure

### Current (as of March 12, 2026)

```
LABRECON/
├── app/
│   ├── data/              ← test/provider data consumed by the site
│   ├── globals.css
│   ├── layout.tsx
│   ├── page.tsx           ← main single-page app
│   ├── favicon.ico
│   └── (other static assets)
├── scraper/
│   ├── compliance/        ← provider ToS/robots compliance docs
│   ├── debug/             ← temporary scraper debug output
│   ├── providers/
│   │   ├── goodlabs.py
│   │   ├── labcorp.py
│   │   └── quest.py
│   ├── utils/
│   ├── main.py
│   ├── tests_catalog.py
│   └── README.md
├── public/
├── docs/                  ← project docs (this file lives here)
├── scripts/               ← utility Python scripts
│   ├── patch_quest.py
│   ├── patch_urls.py
│   └── write_files.py
├── .gitignore
├── package.json
├── next.config.ts
├── tsconfig.json
├── tailwind config files
└── README.md
```

### Target (after SEO expansion)

```
app/
├── data/
├── tests/
│   └── [slug]/
│       └── page.tsx       ← individual test pages
├── sitemap.ts             ← auto-generated sitemap
├── robots.ts              ← crawler rules
├── layout.tsx
└── page.tsx               ← homepage with full comparison table
```

---

## 5. Git & Cursor Quick Reference

### The Mental Model

```
Your Computer (local)  →  GitHub (remote)  →  Vercel (live site)
       ↑                       ↑                     ↑
  git commit              git push            auto-deploys from main
  (save point)         (send to GitHub)       (you don't control this)
```

Nothing goes live until changes reach the `main` branch on GitHub.

### Branches

| What you want to do | Command |
|---|---|
| Create new branch and switch to it | `git checkout -b fix/my-description` |
| See what branch you're on | `git branch` |
| Switch back to main | `git checkout main` |
| Switch to existing branch | `git checkout branch-name` |
| Delete a branch (local) | `git branch -d branch-name` |

**Naming convention:** `fix/` for fixes, `feat/` for new features, `chore/` for cleanup.

### Saving Work (Commits)

| What you want to do | Command |
|---|---|
| See what changed | `git status` |
| See changes line by line | `git diff` |
| Stage all changes | `git add -A` |
| Stage one file | `git add path/to/file.ts` |
| Commit with message | `git commit -m "short description"` |
| Undo last commit (keep files) | `git reset --soft HEAD~1` |

### Push / Pull

| What you want to do | Command |
|---|---|
| Push branch to GitHub | `git push origin branch-name` |
| Push main | `git push origin main` |
| Pull latest from GitHub | `git pull origin main` |
| First push of new branch | `git push -u origin branch-name` |

### The Safe Workflow (Use for Every Structural Change)

```
1.  git checkout main                   ← start from main
2.  git pull origin main                ← get latest
3.  git checkout -b feat/my-feature     ← create branch
4.  ... make changes ...
5.  git add -A                          ← stage
6.  git commit -m "feat: description"   ← save checkpoint
7.  git push -u origin feat/my-feature  ← send to GitHub
8.  Open Pull Request on GitHub         ← review changes
9.  Merge on GitHub                     ← this makes it live
10. git checkout main                   ← back to main locally
11. git pull origin main                ← sync
```

### Emergency Commands

| Situation | Command |
|---|---|
| Undo everything uncommitted | `git checkout -- .` |
| Undo last commit (not pushed) | `git reset --soft HEAD~1` |
| See recent history | `git log --oneline -10` |
| Throw away a branch | `git checkout main` then `git branch -D branch-name` |

### Cursor / Terminal Basics

| What you want to do | Command |
|---|---|
| Open terminal in Cursor | `Ctrl + backtick` (or `Cmd + backtick` on Mac) |
| Run dev server | `npm run dev` |
| Build (check for errors) | `npm run build` |
| Install dependencies | `npm install` |
| Stop a running process | `Ctrl + C` |
| Clear terminal | `clear` |
| List files in folder | `ls` |
| Move into folder | `cd folder-name` |
| Go up one folder | `cd ..` |
| Show current location | `pwd` |

### When to Branch vs Work on Main

**Work on main:** Fixing a typo, updating a single price, editing copy.
**Use a branch:** Moving files, adding pages, changing components, anything structural.

### Rules of Thumb

1. One branch per task. Don't mix unrelated changes.
2. Commit often. Small commits are easier to undo.
3. Never `git push --force` unless you fully understand it.
4. Pull before you branch. Always start from latest main.
5. Read the diff on GitHub before merging.

---

## 6. Claude Code Prompt Templates

### Always Include These Safety Lines

Put these at the top of any Claude Code prompt for structural changes:

```
- Create a new branch called [name] before making any changes
- Do NOT delete any files unless I explicitly say to
- Do NOT modify business logic, styling, or content
- Commit when done but do NOT push
- If the build fails, stop and report the error — do not try to fix it without telling me
```

### Template: Repo Audit & Security Scan

```
Create branch: fix/gitignore-and-secrets-audit

1. Search entire repo for exposed secrets:
   - Check for .env files tracked by Git: git ls-files | grep -i env
   - Search all .ts, .tsx, .js, .py files for: api_key, apiKey, API_KEY,
     secret, SECRET, token, TOKEN, password, sk-, pk-, Bearer
   - Check git history: git log -p --all -S "api_key" -- (last 20 commits)
   - If found: report file and line, mask value (first 4 chars only)

2. Audit .gitignore — ensure it includes:
   node_modules/, .next/, out/, __pycache__/, *.py[cod], .venv/, venv/,
   .env, .env.local, .env.*.local, .DS_Store, Thumbs.db, .vscode/, .idea/,
   tsconfig.tsbuildinfo, scraper/debug/, scraper/output/, .git.zip

3. Remove tracked junk: git rm -r --cached __pycache__/ etc.

4. Run npm run build to verify nothing broke

5. Commit but do NOT push. Print summary of findings.
```

### Template: Add New Test Pages

```
Create branch: feat/individual-test-pages

1. Create app/tests/[slug]/page.tsx
2. Use generateStaticParams() to generate pages for all tests in the data file
3. Use generateMetadata() for per-page title and description
4. Each page: H1 test name, description, clinical notes, biomarkers,
   price comparison table, "Order from [Provider]" buttons, last verified date
5. Link test names on homepage to their individual pages
6. Do NOT change homepage layout or styling
7. Run npm run build
8. Commit but do NOT push
```

### Template: Add Sitemap & Robots

```
Create branch: feat/seo-foundation

1. Create app/robots.ts:
   - Allow all crawling
   - Reference sitemap at https://www.labrecon.io/sitemap.xml

2. Create app/sitemap.ts:
   - Include / and all /tests/[slug] pages
   - Set lastModified to most recent price verification date

3. Add Open Graph meta tags to layout.tsx (og:title, og:description, og:url, og:type)

4. Run npm run build
5. Commit but do NOT push
```

### Template: Move/Rename Files

```
Create branch: chore/[description]

Use git mv for all file moves (so Git tracks the rename properly).
After all moves, check for broken imports:
- grep -r "old/path" app/ lib/ components/
If any imports reference old paths, update them.
Run npm run build to verify.
Commit but do NOT push.
```

---

## 7. Key Decisions Pending

| Decision | Depends On | When |
|---|---|---|
| GoodLabs pricing display permissions | Their response | Within 2 weeks |
| GoodLabs affiliate/partner structure | Their response | Within 2 weeks |
| Which additional providers to add | Price research | Week 3 |
| Whether to add a database | When manual updates get painful (50+ tests × 6+ providers) | Month 2–3 |
| Scraping vs manual vs API | Provider relationships + scale | Month 3+ |
| Blog / content strategy | After core product is solid | Week 4+ |

---

## 8. Risks & Flags

| Risk | Severity | Mitigation |
|---|---|---|
| Placeholder prices destroy trust | CRITICAL | Verify all prices first. Show "last verified" dates. |
| GoodLabs says no to price display | HIGH | Fallback: "Check price at GoodLabs" with outbound link |
| Stale prices over time | HIGH | Monthly manual checks. Calendar reminder. Automate later. |
| Provider ToS restrictions | MEDIUM | Read each provider's ToS before displaying prices |
| No organic traffic | HIGH | SEO foundation takes months to compound. Start now. |
| Single-page kills SEO | HIGH | Individual test pages fix this |
| Over-engineering | MEDIUM | Follow steps in order. No database, scraping, or auth yet. |
| Accidental secret exposure | MEDIUM | Run security audit. Fix .gitignore. Don't hardcode keys. |

---

## 9. What NOT to Do Yet

- Database (TypeScript data file is fine for 50 tests × 6 providers)
- Scraping infrastructure (manual updates work at this scale)
- User accounts or login
- CMS
- Display ads (wait for 10k+ monthly visits)
- ZIP code / location-based pricing (complex, low ROI now)
- Cloudflare Workers, D1, or R2
- Notion for task tracking (use GitHub Issues)

---

## 10. Success Metrics

**MVP is "done" when:**
- All prices are real and verified with dates shown
- Every price links to the actual provider order page
- Individual test pages exist with unique URLs
- Google Search Console shows pages being indexed
- At least 1 affiliate program is active
- Analytics are tracking traffic

**Post-MVP targets:**
- 30+ tests listed
- 5+ providers compared
- 1,000+ monthly organic visitors (3–6 months)
- First affiliate revenue (even $1 proves the model)

---

## 11. Learning Path

| Skill | When | Why | Where to Learn |
|---|---|---|---|
| Next.js dynamic routes (`[slug]`) | Week 1 | Individual test pages | Next.js docs → Routing → Dynamic Routes |
| `generateStaticParams()` | Week 1 | Static generation for SEO | Next.js docs → Data Fetching |
| `generateMetadata()` | Week 1 | Per-page SEO tags | Next.js docs → Metadata |
| Next.js `sitemap.ts` | Week 2 | Auto-generated sitemap | Next.js docs → sitemap.xml |
| Google Search Console | Week 2 | Submit sitemap, monitor indexing | Google's setup guide |
| Lighthouse audit | Week 3 | Performance/accessibility | Chrome DevTools → Lighthouse tab |
| Affiliate link setup | Week 4 | Monetization | Provider-specific docs |
| Keyword research | Week 4+ | Content strategy | Ubersuggest or Google Keyword Planner |
| Git branching workflow | Ongoing | Safe code changes | This document, section 5 |

---

## GoodLabs Relationship (Key Asset)

- Real DTC lab provider (goodlabs.com), fulfills through Quest and LabCorp
- CLIA-certified, CAP-accredited labs
- Offers free labs with blood donation + paid à la carte tests
- You have 76 personal referrals
- You've contacted their Head of Operations with partnership questions
- Pending: affiliate program, tracked links, pricing display permissions
- **This is your most important business relationship right now.**
