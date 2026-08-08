# Caption semantic segmentation

Build captions from the final audio and canonical text. Timing and language segmentation must share one ledger.

## Preferred unit

Use one complete spoken sentence as one timed cue when readable. Keep it visible until the final phoneme. A visual line wrap does not create a new timed cue: a long sentence may use two rows that enter and leave together.

For Chinese member videos, prefer roughly 8–22 Han characters per visual line, but treat this as layout guidance rather than permission to cut meaning. Reduce font slightly within the approved range or use two rows before creating a mid-sentence replacement.

## Allowed temporal boundaries

Split only at a real audible pause after:

- sentence-ending punctuation: `。！？`;
- a semicolon or colon that completes the preceding thought;
- a comma where both sides are independently understandable clauses;
- an enumerated item whose number, unit, and noun phrase remain together.

The cue end must align to the last audible phoneme of that sentence/clause; the next cue begins with its first audible word.

## Forbidden boundaries

Do not end a cue:

- after conjunctions or transitions such as `和、与、或、但、而、所以、因为、如果、虽然、以及、并且`;
- after prepositions or coverbs such as `把、被、对、向、从、由、为、在、通过、根据`;
- between a subject and predicate, verb and object, modifier and head noun, number and unit, name and title, or fixed term;
- inside paired structures such as `不是…而是…`、`不仅…而且…`、`如果…那么…`、`之所以…是因为…`;
- merely because half the estimated duration or half the character count has elapsed.

Avoid beginning a cue with an orphaned continuation such as `的、了、着、过、吗、呢、而且、但是、所以` unless the canonical sentence genuinely starts there.

## Workflow

1. Restore punctuation in the canonical transcript for segmentation even if terminal `。` is hidden visually.
2. Bind words/characters to measured speech timestamps.
3. Segment by sentence and clause boundaries.
4. Lay out each cue; use two visual rows inside the same cue when needed.
5. Run `scripts/validate_caption_semantics.py`.
6. Review every warning together with the previous and next cue while listening at normal speed.
7. Inspect the longest rendered cue and at least five consecutive cue transitions.

Automatic validation is triage. A clean report does not replace listening and semantic review.
