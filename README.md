# No Hands KDP

**Automate Amazon KDP and Draft2Digital book uploads using Chrome DevTools Protocol.**

Fill every field. Upload every file. Save as draft. Walk away.

> **95% automation, 5% human click.** Amazon's Publish button requires a human. Everything else is automated.

---

## What It Does

No Hands KDP connects to your Chrome browser via CDP (Chrome DevTools Protocol) and fills out the entire KDP book upload form — title, subtitle, series, author, description, keywords, categories, cover, manuscript, AI disclosure, pricing — then saves as draft. You click Publish.

It also supports Draft2Digital with full publish capability (D2D's submit button works programmatically).

### Feature Comparison

| Feature | No Hands KDP | Amazon-KDP-Automater | auto-kdp | Commercial Tools ($20-50/mo) |
|---------|:---:|:---:|:---:|:---:|
| KDP form fill (all fields) | Yes | Partial | Partial | Yes |
| Category cascade modal | Yes | No | No | Maybe |
| AI disclosure handling | Yes | No | No | Unknown |
| EPUB + cover upload | Yes | PDF only | PDF only | Yes |
| 13-marketplace pricing | Yes | No | No | Yes |
| Series modal (existing series) | Yes | No | No | Maybe |
| Draft2Digital integration | Yes | No | No | Rare |
| D2D full publish (no human click) | Yes | No | No | Rare |
| Batch multi-book upload | Yes | Via JSON | Via CSV | Yes |
| Open source | Yes | Yes | Yes | No |
| Price | Free | Free | Free | $20-50/mo |

---

## Quick Start

### Prerequisites

- Python 3.11+
- Chrome running with remote debugging:
  ```bash
  /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
  ```
- Logged into [kdp.amazon.com](https://kdp.amazon.com) in that Chrome window
- Python packages:
  ```bash
  pip install websockets httpx playwright
  playwright install chromium
  ```

### Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/chrismole310/no-hands-kdp.git
   cd no-hands-kdp
   ```

2. Create your book data file (`books.json`):
   ```json
   [
     {
       "title": "My Book Title",
       "subtitle": "A Thriller Novel",
       "series_name": "My Series",
       "series_number": "1",
       "author_first": "Jane",
       "author_last": "Author",
       "description": "Full book description for the product page...",
       "keywords": ["keyword one", "keyword two", "keyword three"],
       "price_usd": "4.99",
       "epub": "/absolute/path/to/book.epub",
       "cover": "/absolute/path/to/cover.jpg"
     }
   ]
   ```

3. Run:
   ```bash
   # Upload all books to KDP (saves as draft)
   python no_hands_kdp.py

   # Upload a single book by index
   python no_hands_kdp.py --book 1

   # Upload to Draft2Digital (full publish)
   python no_hands_d2d.py
   ```

4. Go to KDP bookshelf and click "Publish" on each draft.

---

## How It Works

No Hands KDP uses raw WebSocket connections to Chrome's DevTools Protocol. It doesn't use Selenium or browser drivers — it talks directly to your already-logged-in Chrome session.

### The Three KDP Tabs

**Tab 1: Details** (`/details`)
- Sets language, title, subtitle
- Opens series modal, selects existing series, sets volume number
- Fills author name (handles visible/hidden field duplicates)
- Fills description via CKEditor API
- Sets publishing rights, adult content
- Fills 7 keyword fields
- Navigates the category cascade modal (3-level dropdown + placement checkboxes)

**Tab 2: Content** (`/content`)
- Sets DRM to No
- Uploads EPUB via `DOM.setFileInputFiles`
- Uploads cover JPG (targets second file input)
- Waits for EPUB processing (polls until complete)
- Handles AI disclosure: custom `[role="radio"]` elements, dropdowns for text/images/translations, tool name fields matched by placeholder
- Clicks custom `[role="checkbox"]` confirmation

**Tab 3: Pricing** (`/pricing`)
- Enrolls in KDP Select (checkbox + terms modal)
- Sets 70% royalty
- Sets US price, waits for auto-calculation
- Re-enters all 13 international prices with correct formatting (fixes React state issues)
- Saves as draft

### Draft2Digital Flow

D2D uses Playwright (not raw CDP) because it's a React SPA:
- Creates new ebook, fills metadata
- Navigates BISAC category tree (filter → expand → select)
- Uploads cover via hidden `#upload-front-cover` input
- Uploads EPUB, fills description + short description
- Selects free D2D ISBN
- Clicks through Layout → Preview (custom checkbox approval) → Publish
- Sets price and submits — **D2D publish works programmatically!**

---

## The KDP Selector Map

This is the real value. Every field, every gotcha, documented from months of reverse engineering.

### Details Tab

| Field | Selector | Notes |
|-------|----------|-------|
| Title | `name="data[title]"` | |
| Subtitle | `name="data[subtitle]"` | Watch for publisher text leaking in |
| Author First | `name="data[primary_author][first_name]"` | Target visible fields only — KDP has hidden duplicates |
| Author Last | `name="data[primary_author][last_name]"` | Same |
| Series Number | `name="data[series_number]"` | Only appears after series is linked |
| Keywords 0-6 | `id="data-keywords-0"` through `6` | |
| Rights | `name="data-is-public-domain"` value `false` | NOT `non-public-domain` |
| Adult Content | `name="data[is_adult_content]-radio"` value `false` | Must be set BEFORE categories |
| Description | CKEditor API: `CKEDITOR.instances[key].setData()` | Not a regular textarea |

### Content Tab

| Field | Selector | Notes |
|-------|----------|-------|
| DRM | `name="data[is_drm]-radio"` value `false` | |
| Manuscript | `id="data-assets-interior-file-upload-AjaxInput"` | Use `DOM.setFileInputFiles` |
| Cover | Second `input[type="file"]` | Must be RGB, not CMYK |
| AI Text | `id="generative-ai-questionnaire-text"` | Dropdown |
| AI Images | `id="generative-ai-questionnaire-images"` | Dropdown |
| AI Translations | `id="generative-ai-questionnaire-translations"` | Dropdown |
| AI Tool (text) | `placeholder="e.g. ChatGPT"` | No id/name — match by placeholder |
| AI Tool (images) | `placeholder="e.g. DALL-E"` | Same |
| AI Confirmation | `[role="checkbox"]` | NOT `<input type="checkbox">` |
| AI Yes/No | `[role="radio"]` → child `<a>` | Click the `<a>` inside, not the radio |

### Pricing Tab

| Field | Selector |
|-------|----------|
| KDP Select | `id="data-is-select"` |
| Royalty | `name="data[digital][royalty_rate]-radio"` values: `35_PERCENT`, `70_PERCENT` |
| US Price | `name="data[digital][channels][amazon][US][price_vat_inclusive]"` |
| UK Price | `...amazon][UK][price_vat_inclusive]` |
| DE/FR/ES/IT/NL | `...amazon][XX][price_vat_inclusive]` |
| JP Price | Whole numbers only (no decimals) |
| IN Price | Whole numbers only |
| Save Draft | `#save-announce` |
| Publish | `#save-and-publish-announce` — **CANNOT be automated** |

### Categories — The Cascade

The category modal uses React components (`react-aui-modal-content-N`):

```javascript
// Level 0: Select top category
// Options have JSON values: {"level":0,"key":"Science Fiction & Fantasy","nodeId":"..."}
select.value = option.value;
select.dispatchEvent(new Event('change', {bubbles: true}));

// Level 1: Subcategory (appears after L0 selection)
// Match by: option.value.includes('"level":1')

// Level 2: Sub-subcategory
// Match by: option.value.includes('"level":2')

// Placement checkboxes appear after L2 selection
// e.g., "Space Fleet", "Space Marine"
```

**Critical:** The modal ID increments each time it opens (`react-aui-modal-content-1`, `-2`, `-3`...). Don't hardcode the number.

---

## Known Limitations

1. **KDP Publish button cannot be automated.** Amazon's `scripter-button` framework blocks all programmatic clicks. Every method fails (`.click()`, `dispatchEvent`, `Input.dispatchMouseEvent`, Playwright `force:true`, `form.submit()`). You must click it manually.

2. **KDP rate limits new titles.** After ~3-5 rapid submissions, KDP stops generating ASINs. Use 90-second cooldowns between books. The retry logic handles this.

3. **D2D daily submission limit.** D2D caps new titles at ~3-5 per day. The limit resets after 24 hours.

4. **Category cascade is fragile.** The React modal IDs increment, and the dropdown options are loaded dynamically. Works ~70% of the time on first try, ~90% with retry.

5. **React state vs DOM.** Setting input values via JavaScript doesn't always update React's internal state. Use `document.execCommand('insertText')` instead of `.value = ` for reliable React-compatible input.

6. **International price formatting.** Auto-calculated prices trigger validation errors. Must re-enter each price with `execCommand('insertText')` + blur event. IN and JP use whole numbers; all others use `X.XX` format.

---

## Architecture

```
Chrome (port 9222)          No Hands KDP
┌─────────────────┐         ┌──────────────────┐
│ kdp.amazon.com  │◄──CDP──►│ no_hands_kdp.py  │
│ (logged in)     │  WebSocket  │                  │
├─────────────────┤         │  - Tab navigation │
│ d2d.com         │◄──CDP──►│  - Field filling  │
│ (logged in)     │         │  - File upload    │
└─────────────────┘         │  - Error checking │
                            │  - Batch logic    │
                            └──────────────────┘
                                    │
                            books.json (your data)
```

No browser drivers. No Selenium. No headless mode. Just your real Chrome with your real login session.

---

## Tips

- **Use `execCommand('insertText')` for all text inputs.** It's the most reliable method for React-controlled fields.
- **Always `scrollIntoView({block: 'center'})` before interacting.** KDP forms are very long.
- **Set Adult Content before Categories.** The category modal won't open until adult content is answered.
- **90-second cooldown between books.** KDP throttles rapid title creation.
- **Don't take screenshots in automation loops.** Each full-page KDP screenshot is 400KB+. Use text-based DOM queries for validation.

---

## Contributing

PRs welcome. The selector map is the most valuable part — if Amazon changes their UI, the map needs updating. If you find new selectors or gotchas, please contribute.

---

## License

MIT

---

## Credits

Built by [Atlas Studios](https://github.com/chrismole310) while publishing a 20-novel military sci-fi series in 4 days.

*"I needed to upload 20 books to Amazon and D2D. Doing it manually would take 15 hours. No Hands did it in 45 minutes."*
