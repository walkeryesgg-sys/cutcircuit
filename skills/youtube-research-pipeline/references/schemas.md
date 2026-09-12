# Data schemas

## Candidate dataset

Store JSON as `{ "videos": [...] }`. Preserve unknown fields.

Required fields:

```json
{
  "id": "VIDEO_ID",
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "title": "...",
  "channelTitle": "...",
  "channelId": "...",
  "publishedAt": "YYYYMMDD or ISO-8601",
  "durationSeconds": 0,
  "height": 0,
  "subtitleStatus": "unknown|complete|partial|none|failed",
  "subtitleFiles": [".../<videoId>/en.srt"],
  "audioFingerprint": {
    "algorithm": "pcm-envelope-v1",
    "signature": "...",
    "sampleSeconds": 120,
    "createdAt": "ISO-8601"
  },
  "sourceRoute": "query|channel|seed",
  "sourceQuery": "...",
  "qualityScore": 0,
  "qualityStatus": "provisional|reviewed",
  "rejectionReasons": []
}
```

## Duplicate report

Each group contains:

```json
{
  "groupId": "DUP-0001",
  "canonicalId": "VIDEO_ID",
  "members": [
    {"id": "VIDEO_ID", "role": "canonical|mirror|clip|commentary", "signals": []}
  ]
}
```

Use `eventId` separately from duplicate groups. Two videos can cover one event without being byte/content duplicates.

## Source registry

Store verified upload origins separately from candidates. Exact channel IDs receive full provenance weight. Name-only matches require contextual title terms and receive reduced weight.

## Receipts

Write caption/download receipts incrementally with timestamp, command outcome, files, error class, and retry eligibility. Do not store cookies, API keys, or authentication material.
