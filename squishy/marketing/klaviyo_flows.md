# Klaviyo flows (copy and triggers)

Sender name: Deskloaf. Reply-to: the store email. Footer on every email: physical address, unsubscribe, and "Our emails are for adults 18+." Plain layout: one product image, one line of copy, one button. Subject lines under 45 characters.

## 1. Welcome (trigger: subscribed to newsletter via pop-up; 10% code LOAF10)
- **Email 1, immediately.** Subject: "Your desk called. It wants a loaf." Body: Welcome to Deskloaf. Squishies for grown-up desks: curated three-packs, lab-tested, shipped free. Here's 10% off your first order: **LOAF10**. Button: Shop bundles.
- **Email 2, day 2.** Subject: "Taba 101 (why we skip foam)". Body: three lines on cast silicone vs foam, one GIF of the capybara rebounding. Button: Meet the tabas.
- **Email 3, day 5.** Subject: "Every squishy here has a certificate". Body: what a Children's Product Certificate is, why the 2026 recalls happened, why ours are tested. Button: Read Safety & Testing.
- **Email 4, day 8, only if no purchase.** Subject: "LOAF10 expires Sunday". Body: one bundle image, price, code. Button: Use LOAF10.

## 2. Abandoned checkout (trigger: started checkout, no order in 1 h)
- **1 h.** Subject: "You left a loaf behind". Body: cart contents, "ships free on every bundle". Button: Finish checkout.
- **24 h.** Subject: "Still here (and still squishy)". Body: one review quote once available, otherwise the certificate line. Button: Back to cart.
- **72 h, only if AOV over $30.** Subject: "Free sticker sheet if you finish today". Body: reminder that every order includes the sticker sheet anyway; no extra discount. Button: Finish checkout.

## 3. Browse abandonment (trigger: viewed product, no add to cart, 4 h)
- One email. Subject: "Still thinking about the {{ product name }}?". Body: product image, one line, "ships free from $29.99". Button: Take a look.

## 4. Post-purchase (trigger: placed order)
- **Immediately (transactional, from Shopify):** order confirmation, includes the choking-hazard line and "not for microwaves".
- **Day 3 (Klaviyo).** Subject: "How to keep a taba tacky". Body: care: rinse with water, air dry, keep out of direct sun, no oils or lotions; slow-rise foam: keep dry, don't cut open. Button: Care guide (Safety & Testing page).
- **Day 10.** Subject: "Which one did you grab first?" Body: ask for a review (Judge.me link) and a 10-second squeeze video for a chance to be reposted. Button: Leave a review.
- **Day 30.** Subject: "Your desk has room for one more". Body: add-on singles at add-on prices with the free-shipping threshold. Button: Add-ons.

## 5. Win-back (trigger: no order in 60 days after last order)
- **Day 60.** Subject: "New in: {{ latest product }}". Body: newest SKU or bundle. Button: See what's new.
- **Day 75.** Subject: "A loaf for your desk, 10% off". Code: LOAF10BACK (create in Shopify when the flow goes live). Button: Come back.

## 6. Back in stock (trigger: Klaviyo back-in-stock subscription)
- One email, immediately. Subject: "{{ product name }} is back". Body: product image, "limited restock, ships free from $29.99". Button: Grab it.

## Pop-up
Trigger: 8 seconds or 30% scroll, once per visitor, desktop and mobile. Headline: "10% off your first loaf". Sub: "Squishies for grown-up desks. Emails for adults 18+." Field: email only. Button: Send my code. Success: "Check your inbox for LOAF10."

## Segments to build on day one
- Engaged 90 days (opened or clicked in 90 days): the only list campaigns go to.
- Buyers, Non-buyers, VIP (2+ orders or $75+).
- Suppressed: anyone who reports as under 18 or asks to be removed.

## Campaign calendar (Q4)
- Late Oct: "The gift under $30 list" (one email).
- 20 Nov: BFCM preview to Engaged 90 (free add-on at $50, no percentage discount).
- 27–30 Nov: BFCM daily, one email a day, different bundle each day.
- 10 Dec: "Order by" shipping cut-off reminder.
- 26 Dec: "Treat yourself" post-holiday, add-ons.
