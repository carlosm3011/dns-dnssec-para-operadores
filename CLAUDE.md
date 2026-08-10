# dnssec-for-operators

## Context
Part of Training. A course/workshop aimed at operators, covering DNSSEC from a practical, hands-on perspective — signing, validation, key management, and troubleshooting.

## Status
Written material complete. All 7 modules drafted: 01-Introduccion, 02-Registros, 03-Zonas-BIND, 04-Firmando-con-BIND-y-KASP, 05-Monitoreo-Troubleshooting, 06-Arquitectura-Hidden-Signer, 07-DNSSEC-Avanzado (NSEC3, full KASP rollover mechanics, algorithm rollover, CDS/CDNSKEY, multi-signer).

Slide decks complete: one `.pptx` per module in `_slides/`, built against the LACNIC template. Next: review pass across all modules (text + slides).

## Slide decks

- **Template**: `_templates/lacnic46.pptx` — LACNIC-branded Google Slides export. Layouts available: TITLE, TITLE_1, TITLE_AND_BODY, TITLE_AND_TWO_COLUMNS, TITLE_ONLY, ONE_COLUMN_TEXT, MAIN_POINT, SECTION_TITLE_AND_DESCRIPTION, CAPTION_ONLY, BIG_NUMBER, BLANK, plus a closing "¡Gracias!" slide. Brand red is `C53425`; body font is Arial (safe for LibreOffice-based QA rendering).
- **Output**: `_slides/01-Introduccion.pptx` through `_slides/07-DNSSEC-Avanzado.pptx`. Both `_slides/` and `_templates/` are gitignored (binaries, Drive-synced only — not committed).
- **Build tooling**: `scripts/slides/deck_helpers.py` has the reusable primitives (title/bullet placeholders, code blocks, native tables, box-and-arrow diagrams, closing-slide reordering) built with `python-pptx`. `scripts/slides/build_moduleNN.py` (one per module) each produce that module's deck from `lacnic46.pptx`. To rebuild: copy `_templates/lacnic46.pptx` next to the script and run `python3 build_moduleNN.py` — it writes `NN-...-wip.pptx`, which then gets copied into `_slides/`.
- Each deck mirrors its module's structure (intro/agenda, one section per heading, a closing summary table, "¡Gracias!"), varies layouts rather than defaulting to bullets (custom diagrams for anything that was a mermaid graph in the `.md`, native tables for reference/summary content, two-column layouts for compare/contrast), and was QA'd for template validation, leftover placeholder text, and visual overflow (LibreOffice render → inspected page by page).
- Module 7's deck is the longest (23 slides) — matches it being the densest module (NSEC3, rollover state machine, algorithm rollover, CDS/CDNSKEY, multi-signer).
