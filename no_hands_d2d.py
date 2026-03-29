#!/usr/bin/env python3
"""
No Hands D2D — Automate Draft2Digital ebook uploads via Playwright + CDP.
Unlike KDP, D2D's publish button CAN be automated — full hands-free publishing.

Prerequisites:
    - Chrome running with --remote-debugging-port=9222
    - Logged into draft2digital.com
    - pip install playwright httpx
    - playwright install chromium

Usage:
    python no_hands_d2d.py                    # Upload all books from books.json
    python no_hands_d2d.py --book 1           # Upload book at index 1
    python no_hands_d2d.py --start 3 --end 7  # Upload books 3-7
"""
import asyncio, json, os, sys, re, argparse
from playwright.async_api import async_playwright

W = asyncio.sleep

async def upload(pg, bk, i, n):
    print(f"\n{'='*50}\nD2D {i}/{n}: {bk['title']}\n{'='*50}")

    # === METADATA PAGE ===
    await pg.goto("https://draft2digital.com/book/m/new", timeout=30000)
    await W(5)

    # Click Start Ebook link
    try:
        link = pg.locator('a[href*="ebook"]').first
        href = await link.get_attribute('href')
        if href:
            full = f"https://draft2digital.com{href}" if href.startswith('/') else href
            await pg.goto(full, timeout=30000)
        else:
            await link.click()
    except:
        await pg.get_by_text("Start Ebook", exact=False).first.click()
    await W(5)

    try: await pg.locator('#title').wait_for(timeout=10000)
    except: print(f"  !! Page didn't load"); return False

    # Title
    await pg.locator('#title').fill(bk['title'])
    print(f"  Title: {bk['title']}")

    # Series
    if bk.get("series_name"):
        try:
            els = await pg.get_by_text(bk["series_name"], exact=True).all()
            for el in els:
                box = await el.bounding_box()
                if box and 200 < box['y'] < 600:
                    await el.click(); break
            await W(1)
            print(f"  Series: {bk['series_name']}")
        except: pass

    # Volume
    if bk.get("series_number"):
        await pg.evaluate(f"var v=document.getElementById('volumeNumber');if(v){{v.removeAttribute('disabled');v.value='{bk['series_number']}';v.dispatchEvent(new Event('input',{{bubbles:true}}));}}")

    # Keywords
    kw = bk.get("keywords", [])
    if isinstance(kw, list): kw = ", ".join(kw)
    await pg.locator('#searchTerms').fill(kw)

    # Cover
    try:
        await pg.get_by_text("I have front cover art").click(timeout=3000)
        await W(2)
        await pg.locator('#upload-front-cover').set_input_files(bk['cover'])
        await W(5)
        print(f"  Cover: uploaded")
    except Exception as e: print(f"  Cover: {e}")

    # Audience
    try: await pg.get_by_text("does NOT contain content inappropriate").click(timeout=3000)
    except: pass

    # BISAC — filter then tree navigate
    await pg.locator('#filter-bisacs').fill('military')
    await W(2)
    body = await pg.inner_text('body')
    m = re.search(r'FICTION\(\d+\)', body)
    if m:
        try: await pg.locator(f'text={m.group()}').click(); await W(1)
        except: pass
    body = await pg.inner_text('body')
    m = re.search(r'Science Fiction\(\d+\)', body)
    if m:
        try: await pg.locator(f'text={m.group()}').click(); await W(1)
        except: pass
    try: await pg.locator('.bisac-category:has-text("Military")').first.click(); await W(0.5)
    except:
        try: await pg.locator('text=Military').first.click()
        except: pass
    try: await pg.locator('text=War & Military').click(timeout=2000)
    except: pass
    print(f"  BISAC: Science Fiction/Military")

    # START EBOOK
    try:
        await pg.locator('#start-ebook-button').click(timeout=10000)
        print(f"  START EBOOK")
    except Exception as e: print(f"  !! START failed: {e}"); return False
    await W(8)

    # === DETAILS PAGE ===
    # EPUB
    try:
        await pg.locator('input[type="file"]').first.set_input_files(bk['epub'])
        print(f"  EPUB: uploaded")
        await W(10)
    except Exception as e: print(f"  EPUB: {e}")

    # Description
    try:
        eds = await pg.locator('[contenteditable="true"]').all()
        if eds: await eds[0].fill(bk.get('description',''))
        print(f"  Description: OK")
    except: pass

    # Short description
    short = bk.get('short_description', bk.get('description','')[:345])
    if len(short) > 395: short = short[:395] + "..."
    try: await pg.locator('#short-description-editor').fill(short)
    except: pass

    # ISBN
    try:
        await pg.get_by_text("Give me a free Draft2Digital ISBN").first.click(timeout=3000)
        print(f"  ISBN: free D2D")
        await W(1)
    except: print(f"  ISBN: not found")

    # Save & Continue
    try:
        await pg.get_by_role("button", name="Save & Continue").click(timeout=15000)
        print(f"  Details: saved")
    except:
        try: await pg.locator('.submit-button').click(timeout=10000)
        except: print(f"  !! Details save FAILED"); return False
    await W(8)

    # === LAYOUT ===
    try:
        await pg.get_by_role("button", name="Save & Continue").click(timeout=15000)
        print(f"  Layout: saved")
        await W(8)
    except: pass

    # === PREVIEW ===
    body = await pg.inner_text('body')
    if 'reviewed' in body.lower():
        await pg.evaluate("""(function(){var ds=document.querySelectorAll('div');for(var d of ds){var s=window.getComputedStyle(d);if(s.cursor==='pointer'&&d.offsetWidth<50&&d.offsetHeight<50){var n=d.nextElementSibling;if(n&&n.textContent.includes('I have reviewed')){d.click();return;}}}})()""")
        await W(2)
        try:
            await pg.locator('.submit-button').click(timeout=15000)
            print(f"  Preview: approved")
            await W(5)
        except: print(f"  !! Preview FAILED"); return False

    # === PUBLISH ===
    if 'publish' not in pg.url:
        print(f"  !! Not on publish: {pg.url}"); return False

    price = bk.get('price', bk.get('price_usd', '4.99'))
    pi = pg.locator('#id_bookprice')
    await pi.click(click_count=3)
    await W(0.3)
    await pg.keyboard.type(price, delay=50)
    await pg.keyboard.press("Tab")
    await W(2)

    btn = pg.locator('#publish_submit_button')
    dis = await btn.get_attribute('disabled')
    if dis is None:
        await btn.click()
        print(f"  PUBLISHED!")
        await W(5)
        return True
    else:
        print(f"  !! Submit disabled")
        return False

async def main():
    parser = argparse.ArgumentParser(description="No Hands D2D — Automated D2D publishing")
    parser.add_argument("--books", default="books.json", help="Path to books JSON file")
    parser.add_argument("--book", type=int, help="Upload single book by index")
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--end", type=int, default=None)
    parser.add_argument("--cooldown", type=int, default=30)
    args = parser.parse_args()

    with open(args.books) as f: books = json.load(f)
    if args.book is not None: books = [books[args.book]]
    else: books = books[args.start:args.end]
    if not books: print("No books!"); return

    print(f"No Hands D2D — {len(books)} books")

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        d2d = None
        for ctx in browser.contexts:
            for pg in ctx.pages:
                if 'draft2digital' in pg.url: d2d = pg; break
        if not d2d: print("No D2D tab!"); return

        results = []
        for i, bk in enumerate(books):
            if i > 0: print(f"\n  [Cooldown {args.cooldown}s]"); await W(args.cooldown)
            try: ok = await upload(d2d, bk, i+1, len(books))
            except Exception as e: print(f"  !! ERROR: {str(e)[:100]}"); ok = False
            results.append((bk, ok))

    print(f"\n{'='*50}\nD2D SUMMARY\n{'='*50}")
    for b, ok in results:
        print(f"  {b['title']} — {'PUBLISHED' if ok else 'FAILED'}")
    print(f"\n{sum(1 for _,ok in results if ok)}/{len(results)} published on D2D")

if __name__ == "__main__":
    asyncio.run(main())
