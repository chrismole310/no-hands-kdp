#!/usr/bin/env python3
"""
No Hands KDP — Automate Amazon KDP book uploads via Chrome DevTools Protocol.

Prerequisites:
    - Chrome running with --remote-debugging-port=9222
    - Logged into kdp.amazon.com
    - pip install websockets httpx

Usage:
    python no_hands_kdp.py                    # Upload all books from books.json
    python no_hands_kdp.py --book 1           # Upload book at index 1 only
    python no_hands_kdp.py --start 3 --end 7  # Upload books 3-7
"""

import asyncio, json, argparse, sys, os
import httpx, websockets

# ── CDP Session ───────────────────────────────────────────────────────────────

class CDP:
    """Chrome DevTools Protocol session over WebSocket."""
    def __init__(self, ws):
        self.ws = ws; self.msg_id = 0; self.pending = {}
    async def start(self):
        self._task = asyncio.create_task(self._listen())
    async def _listen(self):
        try:
            async for raw in self.ws:
                msg = json.loads(raw)
                mid = msg.get("id")
                if mid is not None and mid in self.pending:
                    self.pending[mid].set_result(msg)
        except: pass
    async def send(self, method, params=None, timeout=30):
        self.msg_id += 1; mid = self.msg_id
        payload = {"id": mid, "method": method}
        if params: payload["params"] = params
        fut = asyncio.get_event_loop().create_future()
        self.pending[mid] = fut
        await self.ws.send(json.dumps(payload))
        try: return await asyncio.wait_for(fut, timeout)
        finally: self.pending.pop(mid, None)
    async def js(self, expression, timeout=30):
        resp = await self.send("Runtime.evaluate", {
            "expression": expression, "returnByValue": True, "awaitPromise": True
        }, timeout)
        res = resp.get("result",{}).get("result",{})
        return None if res.get("type") == "undefined" else res.get("value", res)
    async def nav(self, url):
        await self.send("Page.navigate", {"url": url})
    async def url(self):
        return await self.js("window.location.href")
    async def set_file(self, selector, files):
        doc = await self.send("DOM.getDocument", {"depth": 0})
        root = doc["result"]["root"]["nodeId"]
        qr = await self.send("DOM.querySelector", {"nodeId": root, "selector": selector})
        nid = qr.get("result",{}).get("nodeId", 0)
        if nid == 0: return False
        await self.send("DOM.setFileInputFiles", {"files": files, "nodeId": nid})
        return True
    async def set_file_idx(self, selector, idx, files):
        doc = await self.send("DOM.getDocument", {"depth": 0})
        root = doc["result"]["root"]["nodeId"]
        qr = await self.send("DOM.querySelectorAll", {"nodeId": root, "selector": selector})
        ids = qr.get("result",{}).get("nodeIds", [])
        if len(ids) > idx:
            await self.send("DOM.setFileInputFiles", {"files": files, "nodeId": ids[idx]})
            return True
        return False
    async def fill(self, name, value, visible_only=False):
        vis = "if(inp.offsetParent===null)continue;" if visible_only else ""
        return await self.js(f"""(function(){{var inps=document.querySelectorAll('input[name="{name}"],textarea[name="{name}"]');for(var inp of inps){{{vis}inp.scrollIntoView({{block:'center'}});inp.focus();if(inp.select)inp.select();document.execCommand('delete');document.execCommand('insertText',false,{json.dumps(value)});inp.dispatchEvent(new Event('input',{{bubbles:true}}));inp.dispatchEvent(new Event('change',{{bubbles:true}}));inp.dispatchEvent(new Event('blur',{{bubbles:true}}));return inp.value;}}return false;}})()""")

W = asyncio.sleep

# ── Tab 1: Details ────────────────────────────────────────────────────────────

async def do_details(cdp, book):
    print(f"  [Details] Creating new title...")
    await cdp.nav("https://kdp.amazon.com/en_US/title-setup/kindle/new/details")
    await W(6)
    u = await cdp.url()
    if "signin" in str(u).lower(): print("  !! AUTH REQUIRED"); return False

    # Language
    await cdp.js("(function(){var s=document.querySelector('select');if(s){for(var o of s.options){if(o.value==='en'){s.value='en';s.dispatchEvent(new Event('change',{bubbles:true}));break;}}}})()")
    await W(2)

    # Title + Subtitle
    print(f"  [Details] {book['title']}")
    await cdp.fill("data[title]", book["title"]); await W(1)
    await cdp.fill("data[subtitle]", book.get("subtitle", "")); await W(1)

    # Series (if provided)
    if book.get("series_name"):
        print(f"  [Details] Series: {book['series_name']} #{book.get('series_number','')}")
        await cdp.js("(function(){var l=document.querySelectorAll('a,button,span');for(var x of l){if(x.textContent.trim().toLowerCase().includes('add to series')){x.click();return;}}})()")
        await W(3)
        await cdp.js("(function(){var l=document.querySelectorAll('a,button,div,span');for(var x of l){var t=x.textContent.trim().toLowerCase();if(t.includes('select series')||t.includes('existing series')){x.click();return;}}})()")
        await W(2)
        series_name = book["series_name"].lower()
        await cdp.js(f"(function(){{var l=document.querySelectorAll('a,button,div,span,li');for(var x of l){{var t=x.textContent.toLowerCase();if(t.includes('{series_name}')&&(t.includes('live')||t.includes('title'))){{x.click();return;}}}}}})()"); await W(2)
        if book.get("series_number"):
            await cdp.fill("data[series_number]", book["series_number"]); await W(1)

    # Author (visible fields only)
    await cdp.fill("data[primary_author][first_name]", book.get("author_first",""), visible_only=True); await W(1)
    await cdp.fill("data[primary_author][last_name]", book.get("author_last",""), visible_only=True); await W(1)

    # Description via CKEditor
    print(f"  [Details] Description + rights + adult")
    desc = json.dumps(book.get("description",""))
    await cdp.js(f"(function(){{if(typeof CKEDITOR!=='undefined'){{var k=Object.keys(CKEDITOR.instances);if(k.length>0)CKEDITOR.instances[k[0]].setData({desc});}}}})()"); await W(1)

    # Rights + Adult content
    await cdp.js('(function(){var r=document.querySelector(\'input[name="data-is-public-domain"][value="false"]\');if(r)r.click();})()'); await W(0.5)
    await cdp.js('(function(){var r=document.querySelector(\'input[name="data[is_adult_content]-radio"][value="false"]\');if(r)r.click();})()'); await W(0.5)

    # Keywords
    for i, kw in enumerate(book.get("keywords", [])[:7]):
        await cdp.js(f"(function(){{var inp=document.getElementById('data-keywords-{i}');if(inp){{inp.focus();if(inp.value){{inp.select();document.execCommand('delete');}}document.execCommand('insertText',false,{json.dumps(kw)});inp.dispatchEvent(new Event('blur',{{bubbles:true}}));}}}})()"); await W(0.3)

    # Categories cascade
    print(f"  [Details] Categories...")
    await cdp.js("(function(){var l=document.querySelectorAll('a,button,span');for(var x of l){if(x.textContent.trim()==='Choose categories'){x.scrollIntoView({block:'center'});x.click();return;}}})()")
    await W(3)
    # L0: Science Fiction & Fantasy
    await cdp.js("""(function(){var sels=document.querySelectorAll('select');for(var s of sels){for(var o of s.options){if(o.textContent.trim()==='Science Fiction & Fantasy'){s.value=o.value;s.dispatchEvent(new Event('change',{bubbles:true}));return;}}}})()"""); await W(2)
    # L1: Science Fiction
    await cdp.js("""(function(){var sels=document.querySelectorAll('select');for(var s of sels){for(var o of s.options){if(o.textContent.trim()==='Science Fiction'&&o.value.includes('"level":1')){s.value=o.value;s.dispatchEvent(new Event('change',{bubbles:true}));return;}}}})()"""); await W(2)
    # L2: Military
    await cdp.js("""(function(){var sels=document.querySelectorAll('select');for(var s of sels){for(var o of s.options){if(o.textContent.trim()==='Military'&&o.value.includes('"level":2')){s.value=o.value;s.dispatchEvent(new Event('change',{bubbles:true}));return;}}}})()"""); await W(2)
    # Placement checkboxes
    await cdp.js("""(function(){var cbs=document.querySelectorAll('input[type="checkbox"]');for(var cb of cbs){var l=cb.closest('label')||cb.parentElement;var t=l?l.textContent.trim():'';if((t.includes('Space')||t.includes('Military')||t.includes('Fleet')||t.includes('Marine'))&&!cb.checked)cb.click();}})()"""); await W(1)
    # Save categories
    await cdp.js("(function(){var b=document.querySelectorAll('button,span.a-button-text');for(var x of b){if(x.textContent.trim().toLowerCase()==='save categories'){x.click();return;}}})()")
    await W(3)

    # Pre-order: ready to release
    await cdp.js("(function(){var r=document.querySelectorAll('input[type=\"radio\"]');for(var x of r){var p=x.closest('label')||x.parentElement;if(p&&p.textContent.toLowerCase().includes('ready to release')){x.click();return;}}})()")
    await W(0.5)

    # Save and Continue
    print(f"  [Details] Save and Continue...")
    await cdp.js("(function(){var b=document.querySelectorAll('button,span.a-button-text');for(var x of b){if(x.textContent.trim().includes('Save and Continue')){x.click();return;}}})()")
    await W(10)
    u = await cdp.url()
    print(f"  -> {u}")
    return "content" in str(u)

# ── Tab 2: Content ────────────────────────────────────────────────────────────

async def do_content(cdp, book):
    print(f"  [Content] DRM=No, uploading files...")
    await cdp.js('(function(){var r=document.querySelector(\'input[name="data[is_drm]-radio"][value="false"]\');if(r)r.click();})()'); await W(1)

    # EPUB
    ok = await cdp.set_file('#data-assets-interior-file-upload-AjaxInput', [book["epub"]])
    if not ok: ok = await cdp.set_file('input[type="file"]', [book["epub"]])
    print(f"  [Content] EPUB: {'OK' if ok else 'FAIL'}")

    # Cover
    ok2 = await cdp.set_file_idx('input[type="file"]', 1, [book["cover"]])
    if not ok2: ok2 = await cdp.set_file('#data-assets-cover-file-upload-AjaxInput', [book["cover"]])
    print(f"  [Content] Cover: {'OK' if ok2 else 'FAIL'}")

    # Wait for processing
    print(f"  [Content] Processing...")
    for _ in range(12):
        await W(10)
        s = await cdp.js("(function(){var b=document.body.innerText;if(b.includes('Processing'))return'WAIT';if(b.includes('uploaded successfully')||b.includes('File processing complete'))return'DONE';return'CHECK';})()")
        if s != 'WAIT': break

    # AI disclosure
    ai_tool_text = book.get("ai_tool_text", "Claude (Anthropic)")
    ai_tool_images = book.get("ai_tool_images", "Flux 2 Dev (Black Forest Labs)")

    await cdp.js("(function(){var r=document.querySelectorAll('[role=\"radio\"]');if(r.length>0){var c=r[0].querySelector('a');if(c)c.click();else r[0].click();}})()")
    await W(2)
    await cdp.js("(function(){var s=document.getElementById('generative-ai-questionnaire-text');if(s){for(var o of s.options){if(o.textContent.toLowerCase().includes('extensive editing')){s.value=o.value;s.dispatchEvent(new Event('change',{bubbles:true}));return;}}}})()")
    await W(1)
    await cdp.js("(function(){var s=document.getElementById('generative-ai-questionnaire-images');if(s){for(var o of s.options){if(o.textContent.toLowerCase().includes('one or a few')){s.value=o.value;s.dispatchEvent(new Event('change',{bubbles:true}));return;}}}})()")
    await W(1)
    await cdp.js("(function(){var s=document.getElementById('generative-ai-questionnaire-translations');if(s){for(var o of s.options){if(o.textContent.trim()==='None'){s.value=o.value;s.dispatchEvent(new Event('change',{bubbles:true}));return;}}}})()")
    await W(1)
    await cdp.js(f"""(function(){{var inps=document.querySelectorAll('input[type="text"]');for(var i of inps){{if(i.placeholder&&i.placeholder.includes('ChatGPT')){{i.focus();i.select();document.execCommand('delete');document.execCommand('insertText',false,{json.dumps(ai_tool_text)});i.dispatchEvent(new Event('blur',{{bubbles:true}}));}}if(i.placeholder&&i.placeholder.includes('DALL-E')){{i.focus();i.select();document.execCommand('delete');document.execCommand('insertText',false,{json.dumps(ai_tool_images)});i.dispatchEvent(new Event('blur',{{bubbles:true}}));}}}}}})()""")
    await W(1)
    await cdp.js("(function(){var c=document.querySelector('[role=\"checkbox\"]');if(c)c.click();})()")
    await W(1)
    print(f"  [Content] AI disclosure done")

    # Save and Continue
    await cdp.js("(function(){var b=document.querySelectorAll('button,span.a-button-text');for(var x of b){if(x.textContent.trim().includes('Save and Continue')){x.click();return;}}})()")
    await W(10)
    u = await cdp.url()
    print(f"  -> {u}")
    return "pricing" in str(u)

# ── Tab 3: Pricing ────────────────────────────────────────────────────────────

async def do_pricing(cdp, book):
    price = book.get("price_usd", "4.99")
    print(f"  [Pricing] KDP Select + 70% + ${price}")

    # KDP Select
    await cdp.js("(function(){var c=document.querySelector('#data-is-select');if(c&&!c.checked)c.click();})()")
    await W(2)
    await cdp.js("(function(){var b=document.querySelectorAll('button');for(var x of b){if(x.textContent.trim().toLowerCase().includes('enroll')){x.click();return;}}})()")
    await W(2)

    # 70% royalty
    await cdp.js('(function(){var r=document.querySelector(\'input[name="data[digital][royalty_rate]-radio"][value="70_PERCENT"]\');if(r)r.click();})()'); await W(2)

    # US price
    await cdp.js(f"(function(){{var i=document.querySelector('input[name*=\"US\"][name*=\"price_vat\"]');if(i){{i.focus();i.select();document.execCommand('delete');document.execCommand('insertText',false,'{price}');i.dispatchEvent(new Event('blur',{{bubbles:true}}));}}}})()"); await W(3)

    # International prices (auto-calc fix)
    for c, p in {"IN":"449","UK":"3.76","DE":"4.33","FR":"4.33","ES":"4.33","IT":"4.33","NL":"4.33","JP":"800","BR":"24.99","CA":"6.93","MX":"90.40","AU":"7.26"}.items():
        await cdp.js(f"(function(){{var i=document.querySelector('input[name*=\"{c}\"][name*=\"price_vat\"]');if(i){{i.focus();i.select();document.execCommand('delete');document.execCommand('insertText',false,'{p}');i.dispatchEvent(new Event('blur',{{bubbles:true}}));}}}})()"); await W(0.2)

    # Save as Draft
    await cdp.js("(function(){var b=document.querySelector('#save-announce');if(b)b.click();})()")
    await W(5)
    print(f"  [Pricing] SAVED AS DRAFT")
    return True

# ── Main ──────────────────────────────────────────────────────────────────────

async def main():
    parser = argparse.ArgumentParser(description="No Hands KDP — Automated book uploads")
    parser.add_argument("--books", default="books.json", help="Path to books JSON file")
    parser.add_argument("--book", type=int, help="Upload single book by index (0-based)")
    parser.add_argument("--start", type=int, default=0, help="Start index")
    parser.add_argument("--end", type=int, default=None, help="End index")
    parser.add_argument("--cooldown", type=int, default=90, help="Seconds between books (default: 90)")
    args = parser.parse_args()

    with open(args.books) as f:
        books = json.load(f)

    if args.book is not None:
        books = [books[args.book]]
    else:
        books = books[args.start:args.end]

    if not books:
        print("No books to upload!"); return

    print(f"No Hands KDP — {len(books)} books")
    for i, b in enumerate(books):
        print(f"  {i}: {b['title']}")

    # Connect to Chrome
    tabs = httpx.get("http://localhost:9222/json").json()
    kdp_tabs = [t for t in tabs if 'kdp.amazon.com' in t.get('url','')]
    if not kdp_tabs:
        print("No KDP tab found! Open kdp.amazon.com in Chrome (--remote-debugging-port=9222)")
        return

    async with websockets.connect(kdp_tabs[0]['webSocketDebuggerUrl'], max_size=50*1024*1024) as ws:
        cdp = CDP(ws); await cdp.start()
        results = []
        for i, book in enumerate(books):
            if i > 0:
                print(f"\n  [Cooldown {args.cooldown}s]")
                await W(args.cooldown)
            print(f"\n{'='*50}\nBook {i+1}/{len(books)}: {book['title']}\n{'='*50}")
            ok1 = await do_details(cdp, book)
            if not ok1:
                print("  !! Details FAILED, retrying...")
                await W(60)
                ok1 = await do_details(cdp, book)
            if not ok1: results.append((book, False)); continue
            ok2 = await do_content(cdp, book)
            if not ok2: results.append((book, False)); continue
            ok3 = await do_pricing(cdp, book)
            results.append((book, ok3))

    print(f"\n{'='*50}\nSUMMARY\n{'='*50}")
    for b, ok in results:
        print(f"  {b['title']} — {'DRAFT SAVED' if ok else 'FAILED'}")
    s = sum(1 for _,ok in results if ok)
    print(f"\n{s}/{len(results)} saved as draft. Go to KDP bookshelf and click Publish.")

if __name__ == "__main__":
    asyncio.run(main())
