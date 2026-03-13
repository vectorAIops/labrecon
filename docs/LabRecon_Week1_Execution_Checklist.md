# LabRecon.io — Week 1 Execution Checklist

A focused, no-BS checklist for the next 7 days.

---

## Core Rule for This Week

Do **not** expand scope.

The goal is **not** “build everything.” The goal is to get the MVP into a cleaner, testable, indexable state without burning all Claude/Cursor credits like a maniac.

**Priority order this week:**
1. Finish GoodLabs data integration
2. Stabilize scraper/data structure for 3 providers only
3. Fix lab catalog/design problem (19 vs 120+)
4. Define SEO page structure
5. Verify ZIP-code pricing assumptions before coding anything complex
6. Set up tracking + project dashboard

---

# Week 1 Checklist

## 1) Finish GoodLabs Data Integration First
- [ ] Locate where Claude stopped in the Python script
- [ ] Clean and normalize the manually scraped GoodLabs dataset
- [ ] Add remaining GoodLabs records into the Python pipeline
- [ ] Standardize field names across providers
- [ ] Create/confirm canonical schema for all providers
- [ ] Export one clean combined sample dataset for testing
- [ ] Document edge cases and missing values

### Recommended schema
Use one canonical structure now so future providers do not wreck the project:

```json
{
  "provider": "GoodLabs",
  "canonical_test_name": "Complete Blood Count (CBC)",
  "provider_test_name": "CBC",
  "category": "General Health",
  "is_panel": false,
  "biomarkers_count": null,
  "description_short": "Basic blood cell count test.",
  "sample_type": "Blood",
  "fasting_required": false,
  "price": 29.00,
  "currency": "USD",
  "zip_code": null,
  "location_scope": "national",
  "source_url": "",
  "last_checked_at": "",
  "availability_status": "active"
}
```

### Notes
- Do **not** let each provider keep its own messy structure long-term.
- Split `canonical_test_name` from `provider_test_name` now.
- Add `location_scope` and `zip_code` now, even if ZIP pricing ends up not mattering.

---

## 2) Stop Burning Claude/Cursor Credits Like a Pyromaniac

### Best model usage rule
Use **Sonnet for most coding and iteration**. Use **Opus only for hard architectural/debug/refactor passes**.

That is the practical move. Opus is stronger, but it chews through usage faster and is usually overkill for:
- simple edits
- repetitive code cleanup
- data mapping
- UI tweaks
- content formatting
- small bug fixes

Anthropic’s current official pricing shows Sonnet 4.6 cheaper than Opus 4.6 ($3/$15 per million input/output tokens vs. $5/$25), so using Sonnet as your default is the sane budget move. Anthropic also says Claude and Claude Code usage limits are shared across the same plan limits, and usage bars can be monitored in Settings > Usage. [Anthropic pricing](https://www.anthropic.com/pricing) | [Anthropic usage limits](https://support.anthropic.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan) | [Usage best practices](https://support.anthropic.com/en/articles/9797557-usage-limit-best-practices)

### Recommended split
- **Sonnet:** day-to-day coding, scraper edits, schema updates, page scaffolding, refactors, test-page generation
- **Opus:** one-shot “review this architecture,” “find failure points,” “rewrite scraper strategy,” “audit SEO structure,” “fix a nasty bug”
- **ChatGPT:** planning, prioritization, content structure, product strategy, SEO page planning, markdown/docs/prompts, sanity checks
- **Local model/Qwen if needed:** rough drafting or bulk low-stakes transforms only

### Prompting rules to reduce cap usage
- [ ] Ask for **one file at a time**
- [ ] Ask for **diff-style changes**, not full rewrites
- [ ] Paste only the relevant code block, not entire files unless necessary
- [ ] Tell the model: “Do not rewrite unrelated code”
- [ ] Tell the model: “Return only changed sections” when possible
- [ ] Start with Sonnet first; escalate to Opus only if Sonnet fails twice
- [ ] Keep a scratchpad of reusable prompts in Cursor/Notion
- [ ] Avoid long back-and-forth debugging in one giant thread
- [ ] Start a fresh thread when context gets bloated or sloppy

### Best workflow for your current cap situation
Until Friday 3 PM reset:
- [ ] Use ChatGPT for planning and task packaging
- [ ] Use Sonnet only for the exact code blocks that need to change
- [ ] Do **not** waste Opus on “what do you think” or exploratory chatter
- [ ] Queue up all code tasks in order before spending more credits
- [ ] Batch similar edits into one clean request

### Example efficient coding prompt
```md
You are editing an existing Next.js/Python project.
Only modify the file(s) necessary.
Do not rewrite unrelated code.
Preserve current styling and structure unless explicitly required.
Return:
1. What changed
2. The exact code diff or replacement block
3. Any follow-up step I need to run locally
```

---

## 3) Lock the MVP Scope to 3 Providers
- [ ] Keep MVP limited to GoodLabs, Quest, and Labcorp
- [ ] Do not add more providers this week
- [ ] Add a backlog section for future providers instead
- [ ] Define what “MVP complete” actually means

### MVP completion definition
The MVP is “done enough” when:
- [ ] Users can browse/search a meaningful test set
- [ ] Prices display clearly across the 3 providers
- [ ] Test names are normalized enough to compare
- [ ] Main index pages exist and are crawlable
- [ ] Basic analytics are installed
- [ ] Site explains what it is and what it is not

### Provider expansion decision
**Do not start new provider outreach yet** unless:
- the 3-provider flow works,
- data updates are repeatable,
- the comparison UI is clean,
- and pages are indexable.

More providers right now mostly equals more maintenance, more scraping pain, more normalization pain, and more chances to look half-finished.

---

## 4) Fix the “19 Labs vs 120+ Labs” Website Design Problem
- [ ] Stop trying to force all tests onto the homepage
- [ ] Keep homepage focused on value proposition + simple search/start flow
- [ ] Create dedicated browse architecture for the larger catalog
- [ ] Decide which tests appear as “Most Popular” on homepage
- [ ] Create separate index pages for full catalog access

### Recommended information architecture
**Homepage**
- Hero
- Quick test search
- ZIP input placeholder or optional location prompt
- Most Popular Tests
- Popular Categories
- Why LabRecon exists
- Trust/explanation section
- CTA to browse all tests

**Browse structure**
- `/tests`
- `/tests/[slug]`
- `/categories`
- `/categories/[slug]`
- `/popular-tests`
- `/panels`
- `/providers`
- `/about`
- `/how-it-works`

### Most Popular Tests starter set
- [ ] CBC
- [ ] CMP
- [ ] BMP
- [ ] Lipid Panel
- [ ] A1C
- [ ] Testosterone
- [ ] TSH
- [ ] Vitamin D
- [ ] PSA
- [ ] Ferritin
- [ ] Iron Panel
- [ ] Estradiol
- [ ] CRP
- [ ] ApoB
- [ ] Insulin

That gives users a usable front door without burying them in a spreadsheet cosplay disaster.

---

## 5) Verify ZIP Code Pricing Before Building ZIP Logic
- [ ] Manually test the same tests across multiple ZIP codes for each provider
- [ ] Record whether prices change by ZIP, state, or location availability only
- [ ] Check if provider pricing is national, regional, or lab-location-specific
- [ ] Document findings before coding ZIP-dependent indexing

### Suggested ZIP test sample
Use at least:
- [ ] 76086
- [ ] 10001
- [ ] 30301
- [ ] 60601
- [ ] 85001
- [ ] 94103

### Decision rules
If pricing does **not** materially change:
- [ ] Keep ZIP as availability/location UX only
- [ ] Do not create ZIP-based SEO pages

If pricing **does** change materially:
- [ ] Build a provider/location pricing layer separate from canonical test data
- [ ] Do not duplicate full test records per ZIP unless absolutely necessary

### Better data model if ZIP matters
Use:
- canonical tests table
- provider test mapping table
- price records table
- location table

Not:
- one giant duplicate row per ZIP per test per provider

That bloated garbage will come back later and punch you in the throat.

---

## 6) Build the SEO Page Structure Before “Doing SEO”
- [ ] Create a crawlable site architecture
- [ ] Create internal linking plan
- [ ] Build index pages before chasing keywords
- [ ] Define URL slugs and naming rules
- [ ] Create metadata template for all page types

### Required indexable page groups
- [ ] Homepage
- [ ] Tests hub
- [ ] Individual test pages
- [ ] Categories hub
- [ ] Category pages
- [ ] Popular tests page
- [ ] Panels page
- [ ] Providers page
- [ ] About page
- [ ] How it works page
- [ ] FAQ page

### Per-test page should include
- [ ] Test name
- [ ] Alternate/common names
- [ ] Plain-English explanation
- [ ] What biomarkers are included
- [ ] Why people commonly order it
- [ ] Prep notes if applicable
- [ ] Comparison pricing table
- [ ] “Not medical advice” boundary language
- [ ] Related tests
- [ ] Category links
- [ ] Last updated note

### Important content rule
Explain tests in plain English without diagnosing.
Use language like:
- “This test is commonly used to measure...”
- “People often order this test when...”
- “This biomarker may help monitor...”

Avoid language like:
- “This means you have...”
- “You likely suffer from...”
- “This result confirms...”

You are building education + price comparison, not playing doctor on the internet.

---

## 7) SEO Research Tasks
- [ ] Research competitor keyword structure
- [ ] Identify highest-intent lab search terms
- [ ] Group keywords by page type
- [ ] Build content plan around user intent, not fluff
- [ ] Add metadata, sitemap, robots, canonicals
- [ ] Set up Google Search Console
- [ ] Set up Bing Webmaster Tools

### Keyword buckets to research
- [ ] test name + price
- [ ] where to order [test]
- [ ] [test] cost without insurance
- [ ] affordable blood work
- [ ] self-pay labs
- [ ] online lab test order
- [ ] [test] near me
- [ ] [category] blood tests
- [ ] men’s health labs / women’s health labs / metabolic labs / hormone labs

### What to dig into
- title tags
- meta descriptions
- heading structure
- internal linking
- schema markup opportunities
- image alt text
- page speed / Core Web Vitals
- duplicate content control
- crawl depth

### Useful references
- Google SEO Starter Guide: https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- Search Console Getting Started: https://search.google.com/search-console/about
- Core Web Vitals overview: https://web.dev/articles/vitals
- Next.js SEO basics: https://nextjs.org/learn/seo/introduction-to-seo

---

## 8) Decide Affiliate / Independence Strategy
- [ ] Wait for Jeff at GoodLabs before making a major positioning decision
- [ ] Do not lock LabRecon into one-provider optics too early
- [ ] Keep public positioning comparison-first and consumer-first
- [ ] Define monetization options in writing

### Best current stance
For now:
- stay **independent in branding**
- allow **future affiliate monetization**
- avoid making the site feel like a disguised GoodLabs landing page

Why:
- trust matters more than short-term affiliate optimization
- users need to believe comparisons are real
- future partners will respect leverage more if you already have traffic and user trust

### Monetization paths to keep open
- [ ] affiliate links
- [ ] featured provider placements later
- [ ] API/data licensing later
- [ ] provider lead-gen deals later
- [ ] premium user alerts or saved comparisons later
- [ ] sponsored educational content later, clearly labeled

### Current recommendation
- **Do not reach out to Quest/Labcorp affiliate/partnership teams yet** unless you already have meaningful site structure and proof of traffic plan.
- **Do hear back from Jeff first** and keep that conversation warm.

---

## 9) Scraper Strategy
- [ ] Define scraper scope per provider
- [ ] Separate scraper logic from normalized output layer
- [ ] Create logs/error handling/retry handling
- [ ] Decide whether proxies are needed based on actual failures
- [ ] Store raw snapshots before normalization

### Recommended scraper architecture
- `/scraper/providers/goodlabs.py`
- `/scraper/providers/quest.py`
- `/scraper/providers/labcorp.py`
- `/scraper/normalize.py`
- `/scraper/output/`
- `/data/raw/`
- `/data/normalized/`
- `/data/final/`

### Proxy advice
Do **not** start with proxies unless:
- requests are blocked,
- rate limits are obvious,
- or pages are heavily bot-protected.

Start simple:
- [ ] polite request timing
- [ ] caching
- [ ] local snapshots
- [ ] retries with backoff
- [ ] user-agent rotation only if needed

Only escalate to proxies if the site forces your hand.
Otherwise you are adding complexity, cost, and more failure points for fun. Very cool hobby. Bad MVP choice.

---

## 10) Notion + Dashboard + Traffic Tracking
- [ ] Finish Notion HQ setup enough to manage execution
- [ ] Create one usable dashboard, not 14 fancy dead pages
- [ ] Add build tracker
- [ ] Add SEO/content tracker
- [ ] Add provider outreach tracker
- [ ] Add issues/bugs tracker
- [ ] Add analytics snapshot section

### Traffic stack to add
- [ ] Google Search Console
- [ ] Vercel Analytics
- [ ] Cloudflare Web Analytics
- [ ] Optional: Plausible later if needed

### Dashboard widgets/sections
- [ ] This Week priorities
- [ ] Blockers
- [ ] Scraper status
- [ ] Traffic snapshot
- [ ] SEO pages published
- [ ] Provider opportunities
- [ ] Content backlog
- [ ] Decisions log

---

## 11) Light Mode Version
- [ ] Do not redesign the entire site
- [ ] Create token-based theming if not already in place
- [ ] Reuse same palette family with adjusted surfaces/contrast
- [ ] Test legibility first, aesthetics second

### Light mode rule
Keep the brand identity the same.
This should feel like “LabRecon light mode,” not “some random SaaS template wearing your badge.”

Minimum checks:
- [ ] button contrast
- [ ] border visibility
- [ ] table legibility
- [ ] link contrast
- [ ] hover states
- [ ] mobile readability

---

## 12) Veterans Growth Plan
- [ ] Build a dedicated veterans-facing explanation page later
- [ ] Clarify self-pay lab comparison use case for veterans
- [ ] Explain practical value without attacking VA care directly
- [ ] Collect future real user stories/testimonials carefully

### Smart veteran angle
Position around:
- faster price clarity
- easier self-pay comparison
- less confusion
- educational guidance on common tests
- supplemental consumer tool, not medical care replacement

### Distribution channels to explore later
- [ ] veteran subreddits where allowed
- [ ] veteran Facebook groups where allowed
- [ ] veteran health/benefits communities
- [ ] LinkedIn veteran founder posts
- [ ] direct educational content targeted to veterans

Do not spam this. Build useful content first.
Veterans smell bullshit fast.

---

## 13) Grow the LabRecon Subreddit
- [ ] Write a strong pinned welcome post
- [ ] Add clear rules
- [ ] Add recurring discussion threads
- [ ] Add useful wiki/resource links
- [ ] Clarify “not medical advice” boundary
- [ ] Make it useful even before it is large

### What to add first
- [ ] Welcome / what LabRecon is
- [ ] Rules / what is allowed
- [ ] Price comparison thread
- [ ] “What test are you trying to find?” thread
- [ ] “How to read lab names without losing your mind” thread
- [ ] resource links to trusted educational sources

### Best growth strategy
- be useful
- be searchable
- answer recurring questions cleanly
- cross-reference the website where relevant
- do not turn it into nonstop self-promo

The subreddit grows when it becomes a reference point, not when it becomes your billboard.

---

## 14) Week 1 Deliverables
By the end of this week, the win condition should be:

- [ ] GoodLabs dataset fully integrated into script
- [ ] Canonical schema defined
- [ ] 3-provider MVP scope locked
- [ ] ZIP pricing test completed and documented
- [ ] Final site architecture decided for Tests / Categories / Popular Tests / About / How It Works
- [ ] SEO action list documented
- [ ] Analytics stack chosen
- [ ] Notion dashboard minimally functional
- [ ] Claude/Cursor usage plan in place

---

# Backlog — Not This Week
- [ ] additional lab providers
- [ ] affiliate expansion beyond GoodLabs conversation
- [ ] deeper structured data/schema rollout
- [ ] advanced user accounts/saved comparisons
- [ ] heavy subreddit growth campaigns
- [ ] paid acquisition/ads
- [ ] advanced monetization experiments
- [ ] location-specific scaling if ZIP does not matter yet

---

# Best Immediate Next 5 Actions
1. Finish GoodLabs integration in the script
2. Standardize schema across all 3 providers
3. Test ZIP pricing manually before building logic
4. Define final page architecture for tests/categories/popular pages
5. Use Sonnet for execution and save Opus for hard problems only

---

# One-Sentence Reality Check
You do **not** need more ideas right now. You need one clean data pipeline, one clean site structure, and one clean path to publishable MVP pages.
