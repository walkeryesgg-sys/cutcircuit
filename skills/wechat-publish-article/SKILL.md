---
name: wechat-publish-article
description: Validate and deliver Markdown article packages to WeChat Official Accounts. Use when the user asks to save a 微信公众号 article as a draft, upload its title, summary, body, cover and inline images, check a package before publishing, or publish only after explicit final authorization.
---

# WeChat Publish Article

Deliver a finished article package to a WeChat Official Account with a safe, auditable workflow. Draft is always the default.

## Safety contract

- Treat “保存草稿 / 上传公众号 / 放进后台” as authorization for a draft only.
- Never click or invoke 群发、发表、发布 or scheduled publication unless the user explicitly authorizes public publication in the current turn.
- Before public publication, state the exact account, title and action, then obtain a separate confirmation.
- Never store cookies, credentials, account names, private profile paths or tokens in this skill.
- Do not create a second draft when the same content hash already has a successful receipt unless the user explicitly requests a duplicate.

Read [references/publishing-contract.md](references/publishing-contract.md) before performing an external write.

## Workflow

1. Resolve the Markdown article and its package root.
2. Run preflight:

   ```bash
   python3 scripts/preflight.py /absolute/path/article.md
   ```

3. Stop on errors. Surface warnings that materially affect the rendered article.
4. Check the package receipt directory for the returned content hash.
5. Resolve the cover returned by preflight. A draft without a verified cover is invalid.
6. Render or preview with the selected WeChat-compatible theme.
7. Deliver through the available WeChat posting integration:
   - Prefer browser automation when no official API credentials are configured.
   - Use API only when credentials are already configured and the user chose it.
   - For a draft, use the integration’s explicit draft/save option.
   - Browser delivery must pass `--cover` and complete: local upload → 2.35:1 crop confirmation → visible cover preview.
   - Use the bundled deterministic wrapper when the Baoyu integration is installed:

     ```bash
     python3 scripts/publish_draft.py ARTICLE.md --theme simple --color blue
     ```

8. Verify both the cover preview and the success signal from WeChat. A filled editor or uploaded library image alone is not success.
9. Write a receipt:

   ```bash
   python3 scripts/write_receipt.py ARTICLE.md \
     --content-hash HASH --method browser --status draft \
     --remote-id APPMSGID
   ```

10. Report the result and explicitly say whether it is only a draft or publicly visible.

## Update an existing draft

When the user supplies an existing WeChat editor URL, update that exact `appmsgid`; do not create another draft:

```bash
bun scripts/update_draft.ts \
  --url "WECHAT_EDITOR_URL" \
  --markdown ARTICLE.md \
  --theme simple --color blue --cdp-port 9223
```

The updater replaces title, summary and body, requires an already verified cover preview, saves the same draft, and verifies the returned `appmsgid`.

## Package convention

Keep each article self-contained:

```text
article-folder/
├── article.md
├── covers/
│   └── cover.png
├── images/
└── publish/
    └── wechat-HASH.json
```

Recommended frontmatter:

```yaml
---
title: Article title
description: 60–120 character summary
cover: covers/cover.png
author: Optional author
---
```

`description` and `summary` are interchangeable. Relative image paths resolve from the Markdown file.

## Quality checks

The preflight rejects missing title, summary, cover, local images, unresolved Obsidian embeds, TODO markers and private absolute paths in publishable content. It also returns a stable SHA-256 content hash for idempotency. Saving a draft must fail closed if cover upload or cover-preview verification fails.

Use [references/publishing-contract.md](references/publishing-contract.md) for channel behavior and receipt semantics.
