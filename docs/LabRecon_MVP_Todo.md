# LabRecon.io MVP To-Do List

Last updated: March 12, 2026

---

## Core Objective
Build a clean MVP that lets users compare self-pay lab prices across providers without confusion, while setting up the site so it can scale into SEO, affiliates, partnerships, and community growth.

---

## Priority Order

### Phase 1 - Finish the MVP data foundation first
- [ ] Finish adding the remaining GoodLabs data into the Python script
- [ ] Verify all manually scraped GoodLabs entries are normalized consistently
- [ ] Finalize Claude-assisted scraper progress for Labcorp and Quest
- [ ] Define one normalized internal schema for every test before adding more data
- [ ] Create a validation pass to catch duplicates, mismatched names, missing prices, and bad categories
- [ ] Decide the canonical fields for each test record

**Recommended canonical fields**
- Provider
- Provider test name
- Normalized test name
- Slug
- Category
- Biomarkers included
- Bundle or individual test
- Price
- Price last checked date
- URL to provider page
- Requires ZIP? yes/no
- ZIP/location notes
- Sample type if available
- Turnaround time if available
- Short plain-English description
- Clinical description
- SEO summary
- FAQ block

**Why this comes first**
If the data model is sloppy now, the site, scraper, SEO pages, filters, and future provider expansion all turn into a maintenance dumpster fire.

---

## Immediate Blockers

### 1) Finish GoodLabs integration
- [ ] Complete GoodLabs data entry in the Python script
- [ ] Cross-check every inserted row against your manual scrape source
- [ ] Standardize naming format before importing into the website
- [ ] Tag each item as either:
  - [ ] Individual test
  - [ ] Panel / bundle
- [ ] Add notes for "No Price Listed / Not Available" where needed

**Pro tip**
Do not keep "site display name" and "internal normalized name" as the same field. That gets ugly fast. Keep both.

Example:
- Display name: Testosterone, Total, LC/MS/MS
- Normalized internal name: testosterone-total
- Parent concept: testosterone

---

### 2) Fix the 19 labs vs 120+ labs design problem
- [ ] Redesign the test browser so the homepage does not try to dump 120+ items in the user's face
- [ ] Keep homepage focused on discovery, not full inventory
- [ ] Split content into user-friendly paths

**Recommended structure**
- Home
- Most Popular Tests
- Browse All Tests
- Categories
- Panels / Bundles
- Compare Providers
- About
- Contact

**Recommended homepage layout**
- Hero section
- ZIP code prompt if useful
- Search bar
- Most Popular Tests module
- Categories module
- Why LabRecon exists
- Running total / comparison tool
- Trust / transparency section

**Best MVP move**
Show only:
- Most popular tests
- Popular panels
- Category cards
- Search

Then let users drill down.

Do not make the homepage a giant warehouse shelf of lab tests. That's how you make people bounce.

---

## Data Architecture and Indexing

### 3) Build a proper indexing structure
- [ ] Create one master test index
- [ ] Create one category index
- [ ] Create one popular tests index
- [ ] Create provider-specific pages only where useful
- [ ] Create individual test pages using a reusable template
- [ ] Create bundle/panel pages using a separate reusable template

**Recommended URL structure**
- `/tests`
- `/tests/[slug]`
- `/categories`
- `/categories/[category-slug]`
- `/popular-tests`
- `/panels`
- `/providers`
- `/providers/goodlabs`
- `/providers/quest`
- `/providers/labcorp`
- `/about`
- `/compare`

**For each individual test page include**
- Test name
- Plain-English explanation
- What it measures
- Common biomarkers included
- Why someone might order it
- Typical use cases in normal language
- Provider comparison pricing
- Bundle overlap note
- FAQ
- Related tests
- Category link
- Date last updated

**Keep this line clear**
Explain what the test measures and why people commonly order it.
Do not tell people what they have.
Do not interpret their personal results.
Do not diagnose.

Good phrasing:
- "This test measures..."
- "People often order this test when..."
- "Abnormal results can have many causes and should be reviewed with a licensed clinician."

---

## ZIP Code Strategy

### 4) Figure out whether ZIP-based pricing matters
- [ ] Test the same labs across multiple ZIP codes for Quest, Labcorp, and GoodLabs
- [ ] Record whether price, availability, or physician fee changes
- [ ] Check if differences occur by ZIP, state, or collection site availability
- [ ] Decide whether ZIP should affect:
  - [ ] price
  - [ ] availability
  - [ ] redirect URL
  - [ ] collection site selection only

**Best MVP approach**
Do **not** architect for thousands of ZIP-specific indexes unless the data proves you have to.

Start with this logic:
- Global base price per provider/test
- Optional location override table only when needed

**Suggested model**
- `tests`
- `providers`
- `provider_test_prices`
- `location_overrides`

If ZIP changes nothing or very little, use ZIP only for:
- future local lab draw visibility
- availability filtering
- user personalization

If ZIP changes price materially, then build location overrides by region/state/metro first before going full ZIP-level insanity.

---

## Scraper Strategy

### 5) Build the scraper the smart way
- [ ] Decide source-by-source scraping method
- [ ] Separate scraper logic by provider
- [ ] Store raw scrape output separately from cleaned output
- [ ] Add logging and failure alerts
- [ ] Save last successful scrape date
- [ ] Add change detection for price deltas and broken selectors
- [ ] Create a manual review queue for weird rows

**Recommended scraper structure**
- `/scraper/goodlabs/`
- `/scraper/quest/`
- `/scraper/labcorp/`
- `/scraper/common/`
- `/data/raw/`
- `/data/normalized/`
- `/data/final/`
- `/logs/`

**Use this pipeline**
1. Scrape raw data
2. Normalize names
3. Map to categories
4. Detect bundles vs individual tests
5. Compare against existing database
6. Flag changed rows
7. Publish reviewed data

**Proxies?**
- [ ] Check whether basic scraping works without proxies first
- [ ] Add polite rate limiting and retries
- [ ] Rotate headers/user agents if needed
- [ ] Only add proxies if you're actually getting blocked

Do not start with expensive proxy nonsense unless the target sites force your hand.

---

## SEO Foundation

### 6) Build SEO correctly instead of wish-casting about "top of Google"
- [ ] Set up indexable page architecture
- [ ] Create unique titles and meta descriptions for all key pages
- [ ] Create internal linking between tests, categories, bundles, and providers
- [ ] Add a sitemap
- [ ] Review robots.txt
- [ ] Add canonical tags where needed
- [ ] Make sure pages are crawlable
- [ ] Make sure content is useful and not thin garbage
- [ ] Add structured data where appropriate
- [ ] Set up Google Search Console
- [ ] Track impressions, queries, CTR, and indexed pages

**Reality check**
You do not "meet all Google requirements and go to the top." That is not how this works. You build a technically clean site, publish genuinely useful pages, and earn trust over time.

**Most important SEO pages to build first**
- [ ] Home
- [ ] Popular tests hub
- [ ] Categories hub
- [ ] Individual high-intent test pages
- [ ] Comparison pages for common tests
- [ ] About page with real trust signals

**High-intent SEO targets to build first**
- CBC test cost
- Lipid panel cost
- Testosterone test cost
- CMP cost
- A1C cost
- Thyroid test cost
- Vitamin D test cost
- Ferritin test cost
- PSA test cost
- STD panel cost

**Page ingredients that actually help SEO**
- Clear H1
- Helpful plain-English summary
- Comparison table
- FAQ section
- Related test links
- Freshness / last updated date
- Clean URL slug
- Fast mobile experience

**Structured data ideas**
- Organization
- Breadcrumbs
- FAQ where appropriate

Do not spam markup everywhere like a clown. Use valid markup only where it fits the actual page.

---

## SEO Research Backlog

### 7) Research what it actually takes to rank
- [ ] Build keyword list by test, symptom intent, and cost intent
- [ ] Map one primary keyword and a few supporting keywords to each target page
- [ ] Research competitor content structure for each key test page
- [ ] Build a list of "Most Popular Tests" based on search demand and real user usefulness
- [ ] Create content briefs before writing pages at scale
- [ ] Track ranking progress in Notion

**Keyword buckets to research**
- Cost intent: "cbc test cost", "lipid panel price near me"
- Comparison intent: "quest vs labcorp testosterone test"
- Education intent: "what does ferritin test measure"
- Bundle intent: "best male hormone panel"
- Local intent: "blood test without insurance texas"
- Veteran intent: "cheap blood work for veterans"

---

## Website Content Architecture

### 8) Build the core indexed pages users actually need
- [ ] Most Popular Tests page
- [ ] Browse All Tests page
- [ ] Categories page
- [ ] Panels / Bundles page
- [ ] About page
- [ ] Contact page
- [ ] FAQ page
- [ ] Provider comparison intro page

**Recommended categories**
- General health
- Hormones
- Heart health
- Metabolic
- Thyroid
- Vitamins and nutrients
- Men's health
- Women's health
- Inflammation
- Liver and kidney
- Iron / anemia
- Diabetes
- Sexual health

**About page should include**
- Why you built it
- Why pricing is confusing
- Why consumers need better comparisons
- Transparency statement
- How pricing is gathered
- Affiliate disclosure if used
- "Not medical advice" line without sounding like a corporate robot

---

## Test Page Content Template

### 9) Standardize the content for each test page
- [ ] Plain-English definition
- [ ] Medical definition in simpler terms
- [ ] Biomarkers included
- [ ] Why people commonly order it
- [ ] What it can help monitor
- [ ] Price comparison table
- [ ] Related bundles/panels
- [ ] Related tests
- [ ] FAQ
- [ ] Last updated date

**Add these extra fields because they help users**
- Sample type: blood / urine / saliva if relevant
- Fasting needed: yes / no / sometimes
- Typical turnaround time if publicly available
- Whether it is usually sold alone or inside larger panels
- Whether a physician order is included by the provider
- Whether an in-person draw is required

That gives people actual buying context instead of vague health-blog fluff.

---

## Provider Strategy

### 10) Stay focused or expand?
- [ ] Decide whether MVP means 3-provider depth or more-provider breadth
- [ ] List candidate future providers
- [ ] Score them by pricing, affiliate potential, data accessibility, trust, and consumer value
- [ ] Do not add more providers until current data quality is solid unless a major partnership opportunity appears

**Recommendation**
Focus on making the first 3 providers work well before expanding.

Why:
- Better data quality
- Faster MVP launch
- Easier comparison logic
- Less scraper complexity
- Less SEO mess
- Better trust with users

A bigger broken database is not progress. It's just a larger mess.

---

## Affiliate / Partnership Decision

### 11) Decide whether to stay independent or partner
- [ ] Wait for Jeff at GoodLabs to respond before locking strategy
- [ ] Research whether Quest and Labcorp have affiliate or referral paths
- [ ] Decide whether affiliate links will affect trust positioning
- [ ] Write a public transparency statement before adding any affiliate monetization

**Best near-term move**
Stay *positioned* as independent even if you test affiliate monetization.

**Reason**
The brand should be:
- user-first
- transparent
- comparison-driven
- not obviously captured by one provider

**Practical strategy**
- Phase 1: stay comparison-first, neutral branding
- Phase 2: use affiliate links where available with disclosure
- Phase 3: if GoodLabs partnership becomes strong, keep public comparison integrity intact

Do **not** make LabRecon look like a disguised GoodLabs landing page unless you want to kneecap long-term trust.

---

## Analytics + Dashboard

### 12) Finish Notion setup and track real metrics
- [ ] Create Notion HQ dashboard
- [ ] Add project tracker database
- [ ] Add SEO tracker database
- [ ] Add provider outreach CRM
- [ ] Add scrape issues / bugs tracker
- [ ] Add metrics dashboard

**Metrics to track**
- Sessions
- Unique visitors
- Top landing pages
- Search queries
- Indexed pages
- Clicks to providers
- Conversion proxy events
- Most viewed tests
- Most searched tests
- Exit pages
- ZIP usage if implemented

**Traffic tools to wire up**
- [ ] Vercel Analytics
- [ ] Cloudflare Web Analytics
- [ ] Google Search Console

---

## Light Mode

### 13) Build light mode without wrecking the brand
- [ ] Keep same accent palette and brand feel
- [ ] Create light background surfaces that still feel premium
- [ ] Check contrast carefully
- [ ] Make sure cards, comparison tables, and CTA borders still look intentional
- [ ] Test mobile readability before launch

**Recommendation**
Do not make light mode a bright sterile hospital webpage. Keep it muted, premium, and readable.

---

## Veteran Growth Strategy

### 14) Put this in front of veterans without being spammy
- [ ] Create an about/mission section that explains the VA frustration angle honestly
- [ ] Create content relevant to veterans dealing with delayed care and self-pay testing
- [ ] Build subreddit resources for low-cost testing, common labs, and how to compare providers
- [ ] Reach out to veteran communities only after the MVP actually helps people
- [ ] Build trust with useful tools first, not affiliate pitches

**Good veteran-oriented page ideas**
- Cheap blood work options when the VA is slow
- Common labs veterans may end up paying for out of pocket
- Testosterone / hormone monitoring cost comparison
- Basic wellness lab starter guide

Keep it practical. Nobody wants another patriotic motivational poster pretending to be useful.

---

## Subreddit Growth Plan

### 15) Make the subreddit actually useful
- [ ] Write a sharp pinned welcome post
- [ ] Add clear rules
- [ ] Add posting templates
- [ ] Add FAQ / wiki structure
- [ ] Add resource links to LabRecon pages only when genuinely useful
- [ ] Start discussion threads that are useful even without your website
- [ ] Cross-post carefully from related communities when relevant and allowed
- [ ] Track what posts get engagement

**Pinned threads to create**
- Start here / what this sub is
- Cheapest places to get common labs
- How to compare panels without getting ripped off
- What test are you trying to find?
- Share price screenshots / provider changes
- Not medical advice: how to ask better questions about labs

**Posting templates**
- Looking for a test
- Comparing provider prices
- Understanding what a test includes
- Sharing price updates
- Sharing panel differences

**Goal for the subreddit**
Make it the best place to discuss:
- lab pricing
- provider differences
- test composition
- shopping strategy
- consumer education

Not diagnosis cosplay.

---

## Monetization Roadmap

### 16) Future steps once the MVP is working
- [ ] Add affiliate links where trust and disclosure are clear
- [ ] Track outbound provider clicks
- [ ] Track which tests drive the most intent
- [ ] Build provider-specific deal/discount visibility
- [ ] Add email capture only after clear user value exists
- [ ] Add optional saved lists / favorite labs later
- [ ] Explore B2B or referral partnerships only after consumer traction exists

**Likely monetization order**
1. Affiliate links
2. Featured provider placements with strict transparency
3. Data partnerships / referrals
4. Premium comparison tools or saved reports later

Do not force monetization before usefulness. That's how projects die wearing a tie.

---

## Suggested 2-Week Sprint Plan

### Week 1
- [ ] Finish GoodLabs import
- [ ] Normalize all current test names
- [ ] Finalize schema
- [ ] Fix homepage information architecture for 120+ tests
- [ ] Build Most Popular Tests page structure
- [ ] Test ZIP behavior manually across providers

### Week 2
- [ ] Build tests index page
- [ ] Build categories index page
- [ ] Create reusable individual test page template
- [ ] Add Vercel Analytics
- [ ] Add Cloudflare Web Analytics
- [ ] Add Google Search Console
- [ ] Finish Notion dashboard basics

---

## Recommended Decisions Right Now

### Highest priority decisions
- [ ] Finish current 3-provider MVP before adding more providers
- [ ] Keep brand publicly comparison-first and independent for now
- [ ] Use a normalized data model before scaling content
- [ ] Build hub pages and drill-down pages instead of dumping all tests on home
- [ ] Treat ZIP as an optional override layer unless data proves otherwise
- [ ] Use proxies only if scraping actually gets blocked

---

## Useful Official References

### Google SEO
- SEO Starter Guide: https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- Search Essentials: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Structured Data Gallery: https://developers.google.com/search/docs/appearance/structured-data/search-gallery
- Structured Data Guidelines: https://developers.google.com/search/docs/appearance/structured-data/sd-policies
- Search documentation updates: https://developers.google.com/search/updates

### Vercel Analytics
- Docs: https://vercel.com/docs/analytics
- Installation / enable flow: https://vercel.com/docs/agent/installation

### Cloudflare Web Analytics
- Overview: https://developers.cloudflare.com/web-analytics/
- Getting started: https://developers.cloudflare.com/web-analytics/get-started/
- Rules / path filtering: https://developers.cloudflare.com/web-analytics/configuration-options/rules/
- Pages setup: https://developers.cloudflare.com/pages/how-to/web-analytics/

### Reddit community growth / mod tools
- Growth tips: https://redditforcommunity.com/blog/5-tips-for-growing
- Mod Insights: https://support.reddithelp.com/hc/en-us/articles/15484468824980-Mod-Insights
- Rapid growth guidance: https://support.reddithelp.com/hc/en-us/articles/15484261845780-Dealing-with-rapid-growth
- Wiki guidance: https://support.reddithelp.com/hc/en-us/articles/15484271248788-Wiki-wisdom

---

## Final Notes

The smartest move is not chasing every shiny idea at once.

Right now the actual order is:
1. Finish data
2. Fix structure
3. Build indexable pages
4. Validate ZIP logic
5. Set up analytics
6. Build SEO foundation
7. Then push growth, affiliates, and partnerships

Everything else is just productive-looking procrastination in a nicer outfit.
