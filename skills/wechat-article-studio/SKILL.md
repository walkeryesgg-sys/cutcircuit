---
name: wechat-article-studio
description: "Create and self-audit complete WeChat content packages: evidence-based Chinese writing, low-AI-tone editing, headline candidates, final title, summary, concise 2.35:1 cover, new-account distribution assessment, WeChat Channels adaptation assessment, compliance gates, automatic revision, and Obsidian archiving. Use when asked to 写公众号文章、重写公众号、制作公众号或视频号系列、评估内容质量、生成标题摘要封面、整理微信发布资产，especially for the MuskKnowledgeLab vault."
---

# WeChat Article Studio

Produce a publishable article package, not a lone Markdown file.

## Fixed paths

Resolve `<your-vault>` from the user’s configured Obsidian vault or current project. Do not treat the placeholder as a literal path. The MuskKnowledgeLab rules below are an optional house profile; user instructions take precedence.

Create each article under:

`06 Articles/{master-column}/{topic}/{NN-chinese-title}/`

Use this structure:

```text
NN-chinese-title/
├── NN-chinese-title-正文.md
├── NN-chinese-title-发布信息.md
├── NN-chinese-title-内容自检.md
├── covers/
│   ├── NN-chinese-title-封面.png
│   └── prompts/
│       └── NN-chinese-title-封面提示词.md
├── sources/
└── exports/
```

Never store generated covers in the vault-wide attachment dump. Keep them beside
their article package. Preserve source files; copy rather than move unless the
user explicitly requests moving.

## MuskKnowledgeLab: SpaceX／火星的默认叙事定位

Unless the user explicitly asks for a technical explainer, do **not** write this
column as a professional aerospace account. The default reader is an
entrepreneur, product manager, business researcher, or a general reader who is
curious about Musk but does not need an aerospace lecture.

The central promise is: explain how a distant vision is turned into a customer,
cost structure, cash-flow source, organisational capability, and repeated
experiment. A rocket, engine, orbital refuelling, the Moon, or Mars may appear
only when it explains one of those business decisions.

Before drafting, state the article's single **business question**. It should be
one of the following, or equally concrete:

- who paid for the next attempt, and why;
- which cost or turnaround constraint the product changes;
- why the company made, bought, integrated, or delayed a capability;
- what a failure taught that was worth its time and capital cost;
- how an order, service revenue, manufacturing loop, or organisation created a
  new runway for the long-term goal.

### Business-first evidence and writing rules

- Open with a consequential decision, customer, order, cash constraint, failed
  attempt, or measurable cost—not with a technical definition or vehicle
  specification.
- Translate every necessary technical paragraph into its commercial consequence:
  cost, speed, reliability, customer value, capital requirement, or operational
  cadence. Delete the paragraph if it cannot answer one of these.
- Distinguish verified operating results from company targets, investor claims,
  long-range forecasts, and editorial inference. Never use valuation, promised
  unit cost, or a launch date as proof that a model has already worked.
- Keep ambition and the ledger in the same story: vision explains the risk;
  contracts, cost, timing, and failure explain why the company could continue.
- Do not turn Musk into either a hero myth or a settled fraud narrative. State
  the strongest verifiable fact, then show the decision, trade-off, and remaining
  uncertainty.
- For a technical-historical story, the current-event anchor must illuminate the
  business decision in the past. Do not use a generic launch or space headline
  merely to gain traffic.

### Opinion-led business narrative

For commercial or entrepreneur stories, use **two distinct layers**:

- **fact anchor**: a traceable scene, decision, number, contract, filing,
  interview, or dated operating result;
- **editorial judgment**: the account's explanation of the incentive, pressure,
  trade-off, or larger meaning behind those facts.

Evidence earns trust; judgment creates authorship, emotional force, and a reason
to share. Do not flatten the draft into source notes merely to sound safe. A
judgment may be sharp, vivid, or literary, but it must be recognisable as the
account's interpretation—not a secret motive, a source quotation, or a settled
fact. Where ambiguity matters, use natural framing such as “在我们看来”, “这更像是”,
or a surrounding fact-to-inference transition.

Use this narrative progression when it fits the source:

`concrete scene → abnormal detail → who benefits / pays / bears risk → business mechanism → harder constraint or consequence → reader's decision rule`

- Use a person, founder, or public controversy as the **carrier of system
  pressure**, not as a biography or gossip endpoint. Show how the person's
  choice is constrained by customers, capital, platform rules, supply chains,
  regulators, or public expectations.
- In the opening, place a scene or consequential action before context; follow
  it with one measurable or observable contradiction, then the article's real
  business question. Do not open with a sector overview.
- Each section must add one link to the incentive chain or test the article's
  central explanation. Do not file facts under generic headings such as
  “背景”“技术”“市场”“总结” when the later section does not change the reader's
  understanding of the earlier one.
- Translate one key mechanism into one memorable, accurate image or analogy,
  then support it with concrete evidence. Do not substitute a slogan or a
  metaphor for causality.
- End with an earned, shareable judgment rule—what a founder, operator, or
  researcher should look for next—rather than a generic inspirational lesson.

### Required package fields for this column

In the story/distribution contract and self-check, add:

1. `business_question`: the single reader question about a decision or model;
2. `business_mechanism`: the causal chain, such as order → runway → test →
   product → recurring service revenue;
3. `technical_minimum`: the technical fact needed to explain that chain, plus
   what has not yet been verified;
4. `share_use`: the specific founder, operator, or researcher who could use the
   article to explain a real business trade-off.
5. `editorial_judgment`: the account's one-sentence interpretation, the fact
   anchors that support it, and wording that makes clear it is interpretation.

For this column, a package cannot pass merely because its science is accurate.
It must let a non-aerospace reader retell one business mechanism or decision
rule after reading.

## Legal and platform compliance priority (user requirement, 2026-09-12)

Every article must comply with applicable Chinese laws and current WeChat Official Account rules. These requirements take priority over emotional tension, comparisons, clicks, comments, shares and revenue. Review the title, summary, body, quotations, cover text, inline-image text/captions and discussion prompts before delivery. Remove or rewrite prohibited content and expressions in context; do not use homophones, split characters, images or euphemisms to evade review. Do not invent a universal banned-keyword list or treat a word scan as sufficient: verify current authoritative rules when a topic raises a concrete compliance question, and assess meaning, context and factual support. If uncertainty cannot be resolved, revise the angle or hold the affected material and explain the issue. Never claim guaranteed platform approval. See the compliance gate and engagement reference for final checks.

## Engagement and revenue workflow (user feedback, 2026-09-12)

For every WeChat article, read [engagement-and-revenue-loop.md](references/engagement-and-revenue-loop.md) before choosing the angle and again at final review. Design an evidence-backed disagreement or consequential choice, a concrete emotional stake, and complementary title, opening, cover text and inline-image captions. Give readers a substantive reason to comment and a distinct reason to share. Use fair, task-specific comparisons when relevant; do not require national comparisons or manufacture hostility. Add the reference's fields to publish metadata and the self-check. After publication, assess comparable-window revenue, reading, sharing and comment quality separately; distinguish reported observations from causal hypotheses. Apply Humanizer to every new or rewritten article before final fact and image-caption verification.

## Workflow

1. Read the source material, relevant subtitles, existing series plan, the current account's available performance feedback, and a relevant **current-event anchor**. Do not invent an algorithm weight or diagnose a weak post as “limited” without evidence.
2. Verify the current-event anchor before using it: record its source, event date, and the precise causal question that connects it to the historical material. A hot topic may open the article only when the past event genuinely explains, complicates, or tests what is happening now; never use an unrelated hot topic as a click hook.
3. Define the platform, reader, one reader problem, one learning outcome, and one distribution action: **公众号** = click/read/save; **视频号** = stop/watch/share with a specific friend. Never treat one script as automatically native to both platforms.
4. Build a story and distribution contract before drafting. Read [story-contract.md](references/story-contract.md) and [viral-content-contract.md](references/viral-content-contract.md). Complete its **标题—首屏合同**: the reader's real question, the exact verifiable fact that earns the click, the first-120-character payoff, and the factual turn into the historical story. Then state the article's continuing question sequence, emotional recognition, and natural share use. If evidence cannot supply a protagonist, concrete goal, obstacle, consequential choice, and verified turn, do not disguise an observation essay as story; change angle or collect evidence.
   - For a commercial, entrepreneur, platform, or public-figure story, also read [creator-benchmark-playbook.md](references/creator-benchmark-playbook.md) and complete its pre-draft contract and paragraph ledger. This is required when the article asks readers to accept an account-level interpretation, not merely learn facts.
5. Write or revise `article.md` using [writing-style.md](references/writing-style.md). Treat the title and first screen as the article's primary click-and-retention unit, not a packaging task added after drafting. Use the model only for evidence and structure first; then perform a Chinese-native editorial pass before considering the draft publishable.
4. Generate five materially different headline candidates.
5. Select one final title using accuracy first, then curiosity and specificity.
6. Generate:
   - one 60–100 Chinese-character description;
   - one 4–10 Chinese-character cover line;
   - three keywords;
   - a recommended publish status and series position.
7. Write all choices and reasoning to `publish-metadata.md`.
8. Create the cover prompt before rendering. Follow
   [cover-rules.md](references/cover-rules.md).
9. Invoke `baoyu-cover-image` in quick mode with:
   - `--aspect 2.35:1`
   - `--lang zh`
   - `--text title-only`
   - exact cover line, not the full article title.
10. Save the prompt and bitmap with unique Chinese article names.
11. Update article frontmatter with the final metadata and relative cover path.
12. Run the content quality loop in [content-quality-gate.md](references/content-quality-gate.md):
   - perform the compliance gate first;
   - score the article and its new-account fit;
   - score its WeChat Channels adaptation potential separately;
   - write the evidence-backed scorecard to `NN-chinese-title-内容自检.md`.
13. If the compliance gate fails or the total is below 85, revise the weakest
    dimensions and rescore. Run at most three full revision rounds. Never change
    quotations, dates, numbers, source meaning, or evidentiary boundaries merely
    to improve a score.
14. Validate the package with `scripts/validate_package.py`. A package without a
    passing self-check is invalid.
15. Report paths, final score, revision count, remaining risks, and validation
result. Do not publish unless explicitly asked.

## Chinese-native editorial gate

Before scoring, read the complete text aloud and revise until it passes all of
the following:

- Lead with a person, scene, decision, price, or consequence—not a definition,
  framework, or “this article will explain” setup.
- Use natural Chinese subject–verb order. Delete translated connectors such as
  `事实上`、`值得注意的是`、`换句话说` when they merely simulate reasoning.
- Replace at least three abstract labels with observable actions, dialogue,
  objects, or consequences. Do not fabricate first-hand scenes.
- Keep only one main inference per section. Do not stack definition, evidence,
  caveat and generic advice into one long paragraph.
- Remove symmetrical slogans, lecture transitions, and template endings. A
  reader should be able to retell the story and its implication without using
  the phrase “第一性原理”.
- Read the title and first 120 Chinese characters as one unit. The title's
  concrete question, conflict, or cost must be answered by a verifiable fact
  in that screen; do not spend the opening on a topical overview, a definition,
  or an atmospheric preamble.
- For a person or company under real controversy, formulate the charged label
  as the reader's question, then state the strongest verifiable fact before
  any turn. Never make “骗局”“欺诈”“失言” or a similar allegation a settled
  conclusion unless the evidence proves that conclusion.

## Cover—title—opening hook chain

Treat the cover, title, and first screen as one progressively clarified promise,
not as three versions of a theme.

- **Cover line:** make the reader see one concrete abnormal action, cost, loss,
  deadline, or decision at thumbnail size. A thematic conclusion such as
  “现实客户” or “长期主义” is not a hook by itself.
- The cover must independently name the literal object under discussion. Reject
  pronoun-only or objectless lines such as “用完就扔？”: a reader must not need
  the title to learn what was used, lost, delayed, paid for, or changed.
- For MuskKnowledgeLab business stories, the cover's object and tension must be
  commercial: a customer, order, cash-flow source, cost allocation, pricing,
  outsourcing choice, capital risk, or repeatable service. Engineering action
  alone (for example, a rocket exploding or landing) is insufficient unless the
  line turns it into a business question.
- **Title:** name the actor and the reader's question; add the amount, time,
  consequence, or constraint that makes the cover action meaningful. It must
  remain factually defensible.
- **Opening:** within the first 120 Chinese characters, state the exact
  verifiable fact behind the action and the mechanism that prevents a false
  inference. Do not delay the answer with background, slogans, or a second
  abstract paraphrase.

Before rendering a cover, write this three-part chain in publish metadata and
audit it as a single mobile-feed unit. Reject the package when any link can be
swapped into an unrelated article without changing its meaning. Example of the
shape (not a reusable title template): cover “NASA先付钱” → title specifies an
unproven SpaceX and a $278m agreement → opening explains milestone-based rather
than one-time payment.

## Platform-specific packaging

For every package, write a short `distribution-note` in publish metadata.

- **公众号**: title must be clear in a feed and match the article's concrete
  question. The opening screen must pay off the title; use mobile-length
  paragraphs, a single reading promise, and a natural save/share reason.
- **视频号 adaptation**: define a 3–5 second visual/line hook, a single factual
  surprise, and the exact type of friend who would receive the share. Use a
  short title under 16 Chinese characters. Do not fabricate “traffic pools”,
  fixed completion-rate thresholds, or official metric weights.
- Separate official platform information, own-account evidence, and editorial
  inference. Update platform facts from current official sources before a
  recommendation is presented as a platform rule.

The user's request to use this workflow authorizes quick cover generation with
the fixed 2.35:1 ratio; do not pause to reconfirm routine cover dimensions.
Follow the selected image backend's own safety and generation requirements.

## Article frontmatter

Use:

```yaml
---
type: article
channel: wechat
status: draft
series: 系列名
episode: 1
title: 最终标题
description: 60—100字摘要
cover: covers/cover-2.35x1.png
cover_text: 4—10字封面文案
master_column: 马斯克原典精读
topic: 专题名
archive_id: FP-001
source_video_ids: []
tags: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Keep `title`, `description`, and `cover_text` semantically aligned but not
identical:

- `title`: earns the click without overstating the article.
- `description`: tells the reader what they will understand or be able to do.
- `cover_text`: one visual idea readable on a phone.

## Publish metadata

`publish-metadata.md` must contain:

- final title;
- five title candidates;
- description;
- cover text;
- three keywords;
- target reader;
- learning outcome;
- evidence used with video IDs and timestamps;
- cover design decisions;
- pre-publication checklist.
- final quality score and compliance status;
- WeChat Channels adaptation score, clearly labeled as a separate channel.

## Content self-check

Read [content-quality-gate.md](references/content-quality-gate.md) before scoring
or revising. Read [wechat-channels-new-account.md](references/wechat-channels-new-account.md)
when the package may be repurposed for 视频号 or when the user asks about a new
account, recommendation, growth, or platform rules.

Rules:

- Treat the score as an editorial diagnostic, never a guarantee of traffic.
- Cite concrete passages or package fields for every score; do not award points
  from impression alone.
- Keep WeChat Official Account and WeChat Channels scores separate.
- Label official platform statements, legal requirements, and operational
  inference separately.
- Revise content, title, summary and cover copy as needed, then rescore from
  scratch; do not merely edit the numeric score.
- Require `PASS` for compliance and at least `85/100` overall, with title and
  first-screen payoff at least `16/20`, learning value at least `16/20`, and
  evidence at least `16/20`.
- If three rounds still fail, stop and report the unresolved defect instead of
  claiming completion.

## Open-ended series identity

For recurring columns, use three visual levels:

- small master label: `马斯克原典精读`;
- large variable cover line: article-specific 4–10 characters;
- small topic sequence: `{topic} · {NN}`.

Never show a fixed total such as `01/05`. Numbering is open-ended so new
articles can continue as `06`, `07`, and so on. Reset numbering only when a new
topic begins. Keep internal `archive_id` stable even if public titles change.

## Quality gates

Do not call the package complete unless:

- the reader can state or perform one new thing after reading;
- important claims trace to source material;
- historical numbers include date and context;
- the opening presents a concrete tension within 120 Chinese characters;
- the body has one main promise, not several competing lessons;
- the article avoids repetitive “不是……而是……” constructions;
- title, description, and cover copy do not promise more than the article proves;
- cover, title, and opening form a concrete, progressively clarified hook chain;
- cover ratio is 2.35:1 and the main text remains legible at mobile thumbnail size;
- the cover keeps 40–60% negative space and has one focal anchor;
- all output lives inside the designated Obsidian article package.
- the self-check records compliance `PASS`, total score at least 85, and all
  critical-dimension floors;
- algorithm claims are not presented as official unless backed by a current
  official source;
- copyrighted clips, subtitles, images and quotations have a documented source
  and usage-risk note;
- materially AI-generated or AI-synthesized media has the required declaration.

## Supporting skills

- Use `baoyu-cover-image` to design and render the cover.
- Use `baoyu-post-to-wechat` only after the user explicitly asks to publish or
  save a WeChat draft.
- Use `baoyu-markdown-to-html` only when an HTML preview/export is requested.

## Humanizer final editorial pass (user preference, 2026-09-09)

For article polishing, read and apply `<installed-humanizer>/SKILL.md` after evidence and structure are settled. Use embedded mode, keep supported facts and author judgments, and recheck citations, quantities and scope after editing. Do not equate stylistic cleanup with fact checking or a guaranteed AI-detector result. Preserve the Chinese-native editorial gate and this package workflow.
