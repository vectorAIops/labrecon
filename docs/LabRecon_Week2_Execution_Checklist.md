# LabRecon.io — Week 2 Execution Checklist

A focused checklist for the 7 days after Week 1.

---

## Core Rule for This Week

Turn the MVP from “barely assembled” into “usable, indexable, and believable.”

Week 2 is about tightening the product, not inventing new side quests because your brain saw a shiny object.

**Priority order this week:**
1. Finalize normalized dataset and comparison logic
2. Build crawlable test/category pages
3. Add useful non-diagnostic test content
4. Set up analytics, Search Console, and technical SEO basics
5. Create trust, legal, and site-explainer pages
6. Build the first repeatable content/distribution loop

---

# Week 2 Checklist

## 1) Finalize Data Structure and Comparison Logic
- [ ] Confirm canonical schema works across GoodLabs, Quest, and Labcorp
- [ ] Finish mapping provider-specific names to canonical test names
- [ ] Create clear rules for exact match vs close match vs no-match
- [ ] Flag tests that should not be directly compared
- [ ] Separate single tests from bundles/panels cleanly
- [ ] Add `last_checked_at` and source tracking to all records
- [ ] Create a "needs review" flag for messy mappings
- [ ] Export a clean production-ready JSON or database seed file

### Matching rules to implement
- Exact same test = direct compare
- Same intent but different naming = compare only if biomarkers/specs align
- Different panel composition = do not fake equivalence
- Unknown equivalence = show as "not directly comparable"

### Notes
- Fake precision will wreck trust fast.
- If two tests are not truly equivalent, say so. Do not do price-comparison cosplay.

---

## 2) Build the Core Browse Architecture
- [ ] Launch or finish `/tests` page
- [ ] Launch or finish `/tests/[slug]` dynamic pages
- [ ] Launch or finish `/categories` page
- [ ] Launch or finish `/categories/[slug]` pages
- [ ] Launch or finish `/popular-tests` page
- [ ] Launch or finish `/panels` page
- [ ] Add pagination or lazy loading if needed
- [ ] Add internal links between related tests/categories/panels
- [ ] Make sure every page is reachable by normal crawl paths

### Required UX for `/tests`
- [ ] Search bar
- [ ] Sort/filter options
- [ ] Category filter
- [ ] Single test vs panel filter
- [ ] Clear label for unavailable pricing
- [ ] CTA to open the individual test page

### Notes
- Homepage is not the whole website.
- The catalog pages should do the heavy lifting for both users and SEO.

---

## 3) Build the Test Page Template Properly
- [ ] Create one strong template for all individual test pages
- [ ] Add simple medical definition
- [ ] Add plain-English explanation
- [ ] Add what biomarkers are included when known
- [ ] Add common reasons people order the test
- [ ] Add fasting/sample/prep notes when known
- [ ] Add provider comparison box
- [ ] Add last-updated note
- [ ] Add “not medical advice / not diagnosis” language in a non-annoying way
- [ ] Add links to related tests and related categories

### Recommended page sections
1. Test name
2. What this test is
3. Plain-English explanation
4. What it usually measures
5. Common biomarkers included
6. Who typically orders it and why
7. Prep notes
8. Provider price comparison
9. Related tests
10. FAQ

### End-user content guidance
Include:
- Layman wording
- Medical term wording
- Biomarker list if available
- What the test is commonly used to evaluate
- What it does **not** tell you by itself

Do **not** include:
- diagnosis language
- treatment recommendations
- “you probably have X” nonsense

---

## 4) Build Category and Popular-Test Hubs
- [ ] Define your main categories
- [ ] Assign every test to one primary category
- [ ] Build category pages with short intros and test links
- [ ] Build popular-test pages with stronger educational content
- [ ] Add internal links from homepage to these hubs
- [ ] Add internal links from test pages back to hubs

### Suggested starter categories
- General Health
- Hormones
- Heart Health
- Diabetes / Metabolic
- Vitamins / Nutrients
- Inflammation
- Iron / Anemia
- Liver / Kidney
- Thyroid
- Men’s Health
- Women’s Health

### Best “popular test” pages to prioritize first
- CBC
- CMP
- BMP
- Lipid Panel
- Hemoglobin A1c
- Testosterone
- TSH
- Vitamin D
- Ferritin
- Iron Panel

---

## 5) Install the Real SEO Foundation
- [ ] Set up Google Search Console
- [ ] Submit sitemap
- [ ] Verify robots.txt is correct
- [ ] Add canonical tags
- [ ] Confirm page titles and meta descriptions are unique
- [ ] Generate clean slugs for tests/categories
- [ ] Add Open Graph/Twitter meta tags
- [ ] Add schema markup where appropriate
- [ ] Make sure pages are server-rendered or statically generated where useful
- [ ] Check indexability with live inspection tools

### Schema ideas worth testing
- [ ] BreadcrumbList
- [ ] FAQPage
- [ ] WebSite
- [ ] Organization
- [ ] ItemList for hubs

### Keyword research tasks
- [ ] Build a seed keyword list by test name
- [ ] Add plain-English variants
- [ ] Add “cost,” “price,” “near me,” and “what is” variants
- [ ] Group keywords by search intent
- [ ] Match each keyword group to a page type

### Notes
SEO is not “jam keywords everywhere and pray.”
It is page structure, crawlability, useful content, internal linking, and consistency.

---

## 6) Add Analytics and Dashboard Tracking
- [ ] Install Vercel Analytics or confirm it is working
- [ ] Install Cloudflare Web Analytics or confirm it is working
- [ ] Connect Google Search Console
- [ ] Decide what metrics matter for MVP stage
- [ ] Build a simple Notion dashboard for weekly metrics
- [ ] Track search clicks, pageviews, top pages, exit pages, and conversions

### MVP metrics to track
- [ ] Total sessions
- [ ] Top landing pages
- [ ] Search impressions
- [ ] Search clicks
- [ ] Avg position for core pages
- [ ] Clicks to provider links
- [ ] Most viewed tests
- [ ] Most searched tests
- [ ] Bounce/engagement trend

### Notion dashboard blocks
- [ ] Weekly KPI summary
- [ ] SEO tasks
- [ ] Scraper status
- [ ] Bug backlog
- [ ] Content backlog
- [ ] Affiliate/provider outreach tracker

---

## 7) Create Trust and Site-Explainer Pages
- [ ] Finish `/about`
- [ ] Finish `/how-it-works`
- [ ] Add `/providers` overview page
- [ ] Add `/faq`
- [ ] Add privacy policy
- [ ] Add terms/disclaimer page
- [ ] Add contact page improvements
- [ ] Explain how prices are collected and updated at a high level

### What users need to trust you
- Who built it
- Why it exists
- Which providers are included
- What “comparison” means
- What data may be incomplete or delayed
- That you are not giving medical advice

### Notes
A faceless site that compares medical-ish stuff without explanations looks sketchy. Fix that.

---

## 8) Decide the Affiliate/Independence Strategy
- [ ] Define your default public position on partnerships
- [ ] Decide whether affiliate disclosure language is needed now or later
- [ ] Wait for GoodLabs reply before making hard commitment
- [ ] Do not make Quest/Labcorp outreach a Week 2 priority unless MVP is clean
- [ ] Write one internal memo: independent comparison model vs selective partnerships

### Practical recommendation
For now:
- Stay product-first
- Stay trust-first
- Keep affiliate implementation technically possible
- Avoid making the site feel captured by one provider too early

### Internal decision questions
- Does a partnership reduce user trust?
- Does it block future provider relationships?
- Does it distort rankings or recommendations?
- Does it help or hurt long-term leverage?

---

## 9) Scraper Reliability Planning
- [ ] Document the current scraper flow for each provider
- [ ] Identify what is scraped vs what is manually entered
- [ ] Decide whether proxies are actually needed yet
- [ ] Add retry logic and error logging
- [ ] Add timestamp/versioning for scrape runs
- [ ] Create a manual fallback process if a scraper breaks
- [ ] Define update cadence by provider

### Proxy decision rule
Use proxies only if:
- requests are blocked
- rate limits are obvious
- geographic variation matters
- or scraping at useful scale fails without them

Do **not** add proxy complexity just because it sounds hacker-cool.

### Better first moves than proxies
- throttle requests
- rotate user agents carefully
- cache responses
- scrape less often
- separate test metadata from price updates

---

## 10) Light Mode Planning
- [ ] Audit which UI tokens/colors need abstraction
- [ ] Create a theme token system if missing
- [ ] Design light mode without breaking brand identity
- [ ] Keep contrast strong and avoid sterile “hospital brochure” vibes
- [ ] Decide whether light mode ships now or after MVP stabilization

### Practical recommendation
Do not make light mode a blocking task unless users actually need it now.
If time gets tight, design the token system in Week 2 and ship light mode later.

---

## 11) Veteran-Focused Distribution Plan
- [ ] Define a veteran-specific landing/content angle
- [ ] Build a shortlist of veteran communities worth reaching
- [ ] Draft outreach copy for veteran forums/groups/subreddits
- [ ] Write one useful veteran-focused guide page
- [ ] Identify which problems veterans actually have with self-pay labs

### Good veteran content angles
- Paying cash for labs when care is delayed
- Understanding common baseline labs without jargon
- Comparing common health panels without marketing fluff
- Navigating private lab options while using VA care separately

### Notes
Do not make it “for veterans only.”
Make it broadly useful, then create veteran-relevant distribution channels.

---

## 12) Subreddit Foundation Plan
- [ ] Write a proper pinned welcome post
- [ ] Add clear rules
- [ ] Add post flairs
- [ ] Add user flairs if useful
- [ ] Build a starter wiki/resource section
- [ ] Create 5-10 seed posts yourself so it does not look abandoned
- [ ] Add sidebar/about copy that explains what the sub is for
- [ ] Use recurring post ideas to create habit and consistency

### Subreddit content pillars
- Lab price comparisons
- Test explanations in plain English
- Provider experiences
- Cost-saving tips
- Questions about what a test measures
- Non-diagnostic education
- VA / veteran-related lab access discussions

### First seed posts to create
- Welcome / what this subreddit is
- Cheapest common labs by provider
- Beginner guide to CBC / CMP / Lipids
- How to compare self-pay labs without getting burned
- What makes two lab tests “not equivalent”
- Share your provider experience thread

### Growth reality
A subreddit grows from repeated useful posts and clear identity.
Not from staring at it and hoping Reddit sprinkles magic fairy dust on it.

---

# Week 2 Deliverables

By the end of Week 2, you should ideally have:
- [ ] A clean normalized 3-provider dataset
- [ ] Test pages and category pages live or nearly live
- [ ] A usable internal linking structure
- [ ] Search Console and analytics connected
- [ ] Trust/legal/about pages in place
- [ ] Clear decision notes on partnerships and scraper strategy
- [ ] A basic subreddit foundation and veteran distribution angle

---

# Week 2 Anti-Goals

Do **not** let these derail the week unless absolutely necessary:
- [ ] adding new providers
- [ ] overbuilding ZIP indexing before validation
- [ ] perfecting light mode before core pages exist
- [ ] writing 100 test pages manually before templates work
- [ ] deep affiliate negotiations before the product earns leverage
- [ ] endlessly tweaking homepage aesthetics instead of building crawlable content

---

# Best Use of Claude / ChatGPT During Week 2

## Use Claude for
- file-specific code changes
- scraper fixes
- page templates
- schema/data mapping
- implementation of internal linking and filters

## Use ChatGPT for
- content structure
- page copy frameworks
- SEO page planning
- category definitions
- test-page copy templates
- outreach drafts
- backlog prioritization

## Token-saving rule
Before sending anything to Claude, prep the request here first so the coding model gets one clean shot instead of five confused ones.

