# TubeGen AI "monetized in 9 days" tactic: research and replication plan

Date: 2026-09-21
Trigger: an X video post by Hurricane (@HurricaneCrypt0) captioned "THIS IS F**KING INSANE..." showing the TubeGen AI Niche Finder with these filters: Faceless Channels Only, Long Form, English, Median Views min 5000.

## 1. Who is Hurricane (@HurricaneCrypt0)

What could be verified from public search snippets (x.com itself is blocked from this environment, so follower count and pinned posts could not be read directly):

- **Handle and name.** Hurricane, @HurricaneCrypt0, blue-check account on X.
- **Bio.** "onchain enjoyoor • kol manager | creator". Search snippets also describe the account as a growth strategist and Spaces host who manages 100+ KOLs (key opinion leaders) for Web3 projects.
- **Content history.** The account's indexed posts are almost entirely crypto: DeFi, AI agents on-chain (GM Agents, Surf Copilot), airdrops, "good morning X" engagement posts. There is no indexed history of YouTube, faceless channels, or TubeGen before this post.
- **Related handles.** An Instagram @hurricanecryptooff and a Telegram presence are linked in snippets. Do not confuse with @CryptoHurricane, @HurricaneCrypto, or @Hurricane3788, which are different people.
- **Post reach.** The screenshot shows 41 replies, 766 reposts, 4.1K likes, 16-minute video.

**Assessment.** Hurricane is a paid-promotion professional (KOL manager) in crypto, not a YouTube operator with a track record. The post has the shape of an affiliate or sponsored piece: TubeGen runs a Referral Program (visible in the screenshot's nav bar) and pays affiliates through Tolt links. The "monetized in 9 days" claim could not be found anywhere outside this post. TubeGen's own testimonials claim 14 to 15 days, and no public source shows a 9-day case with channel name or analytics. Treat the 9-day figure as unverified marketing.

## 2. Where the tactic actually comes from

Hurricane's demo reproduces, filter for filter, a YouTube tutorial by Adavia Davis (@adav1a, 28.1K subs): "$101,415 in 90 days with AI YouTube Automation (just copy me)", published 2026-04-07, 492K views. Davis says in that video: "under the niche discovery section on TubeGen I search for faceless channels that are long form and English that average over 5,000 views made within the last 90 days."

Key facts about Davis and TubeGen (Fortune, 2025-12-30, syndicated by Yahoo Finance and AOL):

- Davis is a 22-year-old Mississippi State dropout running a faceless YouTube network.
- TubeGen was built by his business partner Eddie Eizner. Davis says on camera "TubeGen is not my software. My business partner actually made it." He promotes it with a referral link and sells a course at thebunker.group.
- Fortune reviewed his AdSense records: roughly $700K per year, $40K to $60K per month, about $6,500 per month in costs.
- Pipeline: scripts and visuals from Claude, narration from ElevenLabs, assembled into long-form videos up to six hours, as little as $60 per video.
- Most lucrative channel: "Boring History", six-hour "history to sleep to" documentaries. Portfolio also included kids' Minecraft, funny-animal compilations, prank videos, anime edits, Bollywood clips, celebrity gossip.
- Fortune's framing was explicitly "AI slop that people sleep through".

So the "tactic" is Davis's playbook, and TubeGen is the vendor tool that his partner owns. Hurricane is one more affiliate showing the same screen.

## 3. The playbook, step by step (from Davis's video transcript)

1. **Niche selection by outlier hunting.** Filter for faceless, long-form, English channels with median or average views above 5,000 that were created in the last 90 days. Look for channels whose first few videos flopped and then one video exploded. That video is the "outlier" and the signal that demand is validated and competition is low.
2. **Exclusions.** No kids content (low RPM and Made-for-Kids rules), no geopolitics, no sexual content.
3. **Shortlist 5 to 10 niches** in a doc. Score each on momentum, competition, and RPM. RPM is driven by audience age and wealth: finance, business, and older-audience topics (farming equipment, fishing, history) pay more than gaming or anime.
4. **"Niche bend".** Do not clone the outlier channel. Shift its format to an adjacent subject: cats to dogs, "your life as a gorilla" to "your life as every rank in the Italian Mafia".
5. **Channel setup.** Use an aged Google account, watch and comment in the niche for a while before uploading, set country, add channel keywords, Made-for-Kids off, auto-dubbing on, clips on, "let YouTube enhance quality" on.
6. **Production in TubeGen.** Create a "style" by pasting 3 to 4 reference videos from the outlier channel. TubeGen analyzes their scripts and produces a script in that voice at a chosen word count (he uses about 1,600 words), an ElevenLabs voiceover, per-scene images with optional consistent characters, animation on scenes longer than 4 seconds, soundtrack, thumbnail split tests, and a final export. He claims 17 minutes per video.
7. **Upload hygiene.** Title, keyword-rich three-sentence description with the title repeated at the top, competitor hashtags, end screens, Not Made for Kids.
8. **Scale by multiplying channels**, each one a small revenue stream.

## 4. What TubeGen actually is and costs

| Plan | Price per month | Credits | Script word cap | Animation per video |
|---|---|---|---|---|
| Starter | $149 | 33,000 | ~3,000 to 8,000 (sources disagree) | 1 min |
| Pro | $297 | 100,000 | ~10,000 to 20,000 | 10 min |
| Premium | $849 | 340,000 | 20,000 | unlimited |
| Niche Finder add-on | $33 | n/a | n/a | n/a |

Other facts: the Niche Finder is "Powered by TubeLab" (visible in the screenshot), a $29 per month research tool. Voiceover is ElevenLabs under the hood. No free trial. Refund policy is effectively none. Trustpilot sits between 2.8 and 4.0 depending on date. Recurring complaints: generic script output that needs editing, credit burn, thin support. The tubegen.ai site publishes "reviews" of competitors (Nexlev, TubeLab, 1of10) on its own domain, so treat those as marketing.

## 5. Can we replicate it? Yes, and mostly without TubeGen

Every component of the pipeline has an equivalent that is already connected to this workspace or cheap to add.

| Pipeline stage | TubeGen | What we already have |
|---|---|---|
| Niche finder | TubeLab data, $33/mo add-on | **Nexlev MCP** (connected). Same filters and more: faceless, monetized, language, created-after, min avg views, min RPM, outlier score, plus a faceless-outlier video feed and channel transcripts. |
| Outlier video feed | Manual scrolling | Nexlev `faceless_outliers_videos` and `search_viral_videos_small_channels` |
| Script in a proven style | Style template from 3 to 4 reference videos | Nexlev bulk transcripts of the outlier channel plus Claude API with those transcripts as style examples |
| Voiceover | ElevenLabs via credits | ElevenLabs direct (cheaper per character than credit markup), or Higgsfield `generate_audio` (connected) |
| Visuals and animation | Image gen plus auto motion | Higgsfield and Krea MCPs (connected): image batch, image-to-video, consistent characters |
| Assembly | Built-in editor, 30-minute export cap | ffmpeg or moviepy script; no length cap |
| Thumbnails | Style-matched generation | Nexlev `generate_thumbnail` / `get_similar_thumbnails`, or Higgsfield |
| Upload | Manual | YouTube Data API v3, or a CDP-driven browser flow like this repo's KDP uploader |

Estimated run cost per 15-minute video without TubeGen: roughly $3 to $8 (Claude script, ElevenLabs ~2,500 words, 40 to 60 images, a handful of short animations). TubeGen's Starter plan works out to about $15 to $25 per equivalent video once credit burn is accounted for, before the Niche Finder add-on.

Where TubeGen still wins: zero engineering, a single UI, and a 17-minute click-through for someone who will not run scripts. That is not our constraint.

## 6. Live niche scan (Nexlev, 2026-09-21)

I ran the Davis/Hurricane filter through Nexlev: faceless, monetized, English, average video length over 8 minutes, average views over 5,000, under 50K subscribers, created after 2025-10-01, outlier score 2 or higher. 823 channels matched. The 30 highest-revenue matches plus the 60 newest faceless outliers are in `docs/faceless-niche-shortlist-2026-09-21.csv`.

Standouts that fit the "new, small, exploding" profile:

| Channel | Created | Subs | Median views | Est. $/mo | RPM | Angle |
|---|---|---|---|---|---|---|
| Serious History Compilations | 2026-05 | 14.5K | 110K | 13,800 | 10.7 | 2-hour "history to fall asleep to" (Davis's own Boring History format), 9 videos |
| Process Insights 5.0 | 2025-11 | 17K | 56K | 10,700 | 1.8 | AI "inside the factory" process videos, 8.6M-view outlier |
| Nerd Dive | 2025-10 | 3.65K | 16K | 1,800 | 8.4 | Anime "iceberg explained", 7 videos, 313K outlier |
| Incident Files | 2026-08 | 2K | 8.4K | 1,500 | 3.4 | Bodycam incident narration, 19 videos in 7 weeks |
| America's Lost Brands | 2026-07 | 1.5K | 8.9K | 870 | 2.7 | AI-narrated dead-brand histories (Mr. Pibb, Jolt Cola) |
| Andpersands | 2025-12 | 4.2K | 21.5K | 1,040 | 3.5 | "2 hours of lost media to fall asleep to", 6 videos |
| Blue Coast Studio | 2026-04 | 7.2K | 9.4K | 1,000 | 7.5 | Full-length AI sci-fi audiobooks, 5-hour runtime |
| Lessons Of Movies | 2026-03 | 2K | 19K | 960 | 2.9 | Movie-villain psychology essays, 5 videos, 303K outlier |
| Paint Explains It | 2026-05 | 1.3K | 8.1K | 600 | 2.7 | "Last 24 hours before a supervolcano" disaster explainers, AI |
| Vermeidungsphilosophie | ~3 months | 4.9K | 7.7K | 400 | 4.0 | Attachment-style psychology (German); English niche-bend candidate |

Patterns across the 90 rows:

- **Sleep-length compilations** (history, lost media, audiobooks) have the best revenue-to-effort ratio because watch time is enormous and RPM is decent. This is exactly Davis's top earner.
- **Gaming and anime** dominate the outlier list but carry low RPM (2 to 4) and a young audience.
- **Explicitly AI-flagged channels** in the set earn between $0 and $2,700 per month. The high earners are marked as human-produced or hybrid. This matters for section 7.
- **Spanish and German faceless channels** are exploding with far less competition. An English niche-bend of a proven Spanish format is a low-risk play.

## 7. Risks that the promo leaves out

1. **YouTube's inauthentic content policy (July 15, 2025).** Mass-produced, templated, AI-narrated content with no original insight is ineligible for the Partner Program. In early 2026 thousands of faceless AI channels lost monetization, and 16 channels with 4.7B combined views were terminated. YouTube's stated line: if a viewer can tell each video differs in substance and reflects a human point of view, it is fine. Pure "paste a channel link, click generate" output is the profile they are targeting.
2. **Partner Program thresholds.** Ad revenue requires 1,000 subscribers plus 4,000 public watch hours in 12 months or 10M Shorts views in 90 days, then a review that takes days to weeks. Nine days from channel creation to approved monetization requires an outlier video in the first week plus a fast review. It has happened, but it is a lottery ticket, not a system. From 2027-02-01 new applicants need 8,000 watch hours or 20M Shorts views, doubling the bar.
3. **Aged accounts.** Davis recommends buying or reusing aged Google accounts. Buying accounts violates Google's terms and is a ban vector. Use your own old account or start fresh.
4. **Reference-video "styles".** Feeding competitors' scripts into a generator to reproduce their voice is close to derivative content and also the thing the inauthentic policy describes. Use transcripts for structure and pacing analysis, then write original scripts.
5. **Vendor lock and cost.** $149 to $849 per month, non-refundable, with credits that expire. Two months of Starter plus Niche Finder buys a full year of Nexlev and enough API credits for 50+ videos.
6. **Survivorship bias.** Every public number comes from the people selling the tool or the course. No independent case with channel analytics exists for the 9-day claim.

## 8. Recommended pilot (30 days, one channel)

Goal: test the niche-selection half of the playbook, which is the part with real signal, while producing content that clears the originality bar.

1. **Week 1: niche.** Re-run the Nexlev filter weekly. Pick one sleep-length or long-form explainer niche from the shortlist with RPM above 5 and an older audience. Niche-bend it (for example, "history to fall asleep to" bent toward maritime disasters, or "lost brands" bent toward failed tech hardware). Pull transcripts of the top 5 outlier videos and extract hook structure, segment length, and pacing, not wording.
2. **Week 1: pipeline.** Build `no_hands_yt.py` in this repo, mirroring the KDP uploader: JSON manifest per video (title, outline, voice, style refs), Claude for original research-backed script, ElevenLabs for narration, Higgsfield or Krea batch for scene images, ffmpeg assembly, YouTube Data API upload as private. Human reviews and publishes, the same 95/5 split this repo already uses for KDP.
3. **Weeks 2 to 4: publish.** 3 videos per week, 12 to 25 minutes each, one 2-hour compilation at the end of the month. Track views at 48 hours, average view duration, and subs per 1,000 views.
4. **Kill or scale rule.** If no video passes 5,000 views in 30 days, the niche is wrong, not the pipeline. Re-run the filter and bend again. If one video passes 20,000 views, that is the outlier signal and the channel gets a second month.
5. **Budget.** Under $100 per month in API costs. Skip TubeGen unless the pilot proves the niche and the bottleneck becomes clicking speed.

## 9. Sources

- Hurricane on X: https://x.com/HurricaneCrypt0
- Adavia Davis, "$101,415 in 90 days with AI YouTube Automation (just copy me)": https://www.youtube.com/watch?v=OINK1lURm4w
- Fortune profile of Davis and TubeGen (2025-12-30): https://www.fortune.com/2025/12/30/ai-slop-faceless-youtube-accounts-adavia-davis-user-generated-content
- Yahoo Finance syndication: https://finance.yahoo.com/news/22-old-college-dropout-making-145733283.html
- TubeGen pricing: https://www.tubegen.ai/pricing and https://outlierkit.com/resources/tubegen-pricing/
- TubeGen alternatives and Niche Finder breakdown: https://outlierkit.com/blog/tubegen-ai-alternatives-niche-finder
- TubeGen Trustpilot: https://www.trustpilot.com/review/tubegen.ai
- "TubeGen AI Actually Works" affiliate walkthrough (Ava Mitchell): https://www.youtube.com/watch?v=6vzQ7Vd3las
- YouTube inauthentic content policy coverage: https://fliki.ai/blog/youtube-monetization-policy-2025 and https://outlierkit.com/resources/youtube-ai-slop-crackdown-2026/
- YouTube Partner Program requirements 2026 and 2027 change: https://air.io/en/monetization/youtube-partner-program-requirements-2026-the-complete-guide and https://blog.youtube/news-and-events/youtube-partner-program-updates-2027-new-opportunities-earn/
- TubeLab faceless niche rankings: https://tubelab.net/blog/faceless-youtube-channel-niches
- Niche data: Nexlev MCP queries run 2026-09-21, exported to `docs/faceless-niche-shortlist-2026-09-21.csv`
