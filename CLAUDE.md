# dnssec-for-operators

## Context
Part of Training. A course/workshop aimed at operators, covering DNSSEC from a practical, hands-on perspective — signing, validation, key management, and troubleshooting.

## Status
Released. All 7 modules drafted: 01-Introduccion, 02-Registros, 03-Zonas-BIND, 04-Firmando-con-BIND-y-KASP, 05-Monitoreo-Troubleshooting, 06-Arquitectura-Hidden-Signer, 07-DNSSEC-Avanzado (NSEC3, full KASP rollover mechanics, algorithm rollover, CDS/CDNSKEY, multi-signer).

Slide decks complete: one `.pptx` per module in `_slides/`, built against the LACNIC template. Book PDF built via Quarto (`make book`) and released as v0.6.2 (tag pushed, GitHub release publishes `_book/*.pdf` automatically). Content, slides, and PDF are all in sync as of the v0.6.2 build.

## Slide decks

- **Template**: `_templates/lacnic46.pptx` — LACNIC-branded Google Slides export. Layouts available: TITLE, TITLE_1, TITLE_AND_BODY, TITLE_AND_TWO_COLUMNS, TITLE_ONLY, ONE_COLUMN_TEXT, MAIN_POINT, SECTION_TITLE_AND_DESCRIPTION, CAPTION_ONLY, BIG_NUMBER, BLANK, plus a closing "¡Gracias!" slide. Brand red is `C53425`; body font is Arial (safe for LibreOffice-based QA rendering).
- **Output**: `_slides/01-Introduccion.pptx` through `_slides/07-DNSSEC-Avanzado.pptx` — gitignored build output, not committed (regenerate with `make slides`). The template `_templates/lacnic46.pptx` itself **is** committed to git (unlike the outputs) — that's deliberate, so `make slides` works on any machine after a plain `git clone`, without depending on Google Drive sync state.
- **Build tooling**: `scripts/slides/deck_helpers.py` has the reusable primitives (title/bullet placeholders, code blocks, native tables, box-and-arrow diagrams, closing-slide reordering) built with `python-pptx`. `scripts/slides/build_moduleNN.py` (one per module) each produce that module's deck from `lacnic46.pptx`. Run `make slides` from the repo root to rebuild all 7 decks into `_slides/` in one go (see `make help`).
- Each deck mirrors its module's structure (intro/agenda, one section per heading, a closing summary table, "¡Gracias!"), varies layouts rather than defaulting to bullets (custom diagrams for anything that was a mermaid graph in the `.md`, native tables for reference/summary content, two-column layouts for compare/contrast), and was QA'd for template validation, leftover placeholder text, and visual overflow (LibreOffice render → inspected page by page).
- Module 7's deck is the longest (23 slides) — matches it being the densest module (NSEC3, rollover state machine, algorithm rollover, CDS/CDNSKEY, multi-signer).
