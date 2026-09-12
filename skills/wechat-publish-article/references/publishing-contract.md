# Publishing contract

## Action levels

1. `validate`: local read-only inspection.
2. `preview`: local rendering or opening an editor without saving.
3. `draft`: external write to the WeChat draft box. This requires user authorization.
4. `publish`: publicly visible publication. This always requires a separate, explicit confirmation in the current turn.

Authorization for level 3 never implies level 4.

## Successful draft

A draft is successful only when the integration reports a positive save result from WeChat. Merely populating the editor is not success. Record any returned `appmsgid` or other remote identifier.

## Idempotency

The content hash is computed from the title, summary, Markdown body and cover bytes. Before creating a draft, look for `publish/wechat-{hash}.json`. If it records `draft` or `published` with `result: success`, stop and report the existing receipt unless the user explicitly asks for a duplicate.

## Receipts

Receipts contain no secrets. They record the time, content hash, delivery method, status, result and optional remote identifier. Keep them beside the article package so that moving the whole package preserves its history.
