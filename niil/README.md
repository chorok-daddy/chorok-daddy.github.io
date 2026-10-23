# NiiL migration preview

Isolated NiiL site for review. The repository root `index.html`, existing `courses/`, and shared course styles remain unchanged. No link from the root index points to NiiL. Do not switch the main entry point before the owner's final review. NiiL pages carry `noindex,nofollow` during review.

## Content and editing

- `content/pages.json`: 224 public Notion content pages, including 174 course sessions/assignments, 16 members, 14 projects, 3 vision entries, 3 research areas, one notice, and 13 top-level pages.
- `content/assets.json`: 61 stable attachment references mapped to local files (60 images and one PDF).
- `content/routes.json`: original page ID to local URL mapping.
- `assets/media/`: preserved original attachments; rendering does not depend on expiring Notion attachment URLs.
- `assets/niil.css`, `assets/niil.js`: NiiL-only styling and interactions.
- `../tools/build_niil.py`: static HTML generator. Generated HTML should be rebuilt after editing content or templates. Requires Python 3.11+, Beautiful Soup 4, and Pandoc on PATH.

```sh
python3 tools/build_niil.py
python3 tools/check_site.py
python3 -m http.server 8974 --bind 127.0.0.1
```

Preview `/niil/`. Pages work without JavaScript; JavaScript adds project filtering, a mobile navigation toggle, and a document outline.

## Source and conversion decisions

Source: https://niilab.notion.site/NiiL-1af888a17b308042a68fe1de9ed500ee

Retrieved on 2026-10-23. Public site pages were fetched by URL because the active Notion integration cannot query the niilab workspace directly. Public browser views supplied the member, project, and course-row inventories. Duplicate linked database views were consolidated; empty layout wrapper pages and editor metadata are not visitor content.

All six course inventories were reconciled against the visible counts: Robot Basic Lab 32; Micro-Processor Applications 31; Control System 1 30; Control System 2 30; AI Applications 31; EE Seminar 20. Each inventory row has a local detail page. Course source content is preserved as an archive; the existing current AI Applications and Control 1 materials remain authoritative at `/courses/`.

The original Publications page contains a Google Scholar link, not a bibliography; the new page preserves that destination. Internship submissions remain with the original Notion application form; submitted responses are neither collected nor published here. A typo in the displayed research tag (`Appied Intelligence`) is corrected in rendering while the source data is preserved. Source member statuses are respected, including an inconsistent internship view that repeats a master's student; the consolidated people list uses each member's properties.

## Final review and later promotion

Review the design, member affiliations/statuses, project metadata, course archive wording, recruitment notice, and original application submission flow. Automated link checks validate local targets and anchors only; they do not certify Scholar, KLAS, Notion forms, or other external services.

After explicit final review, choose the new root routing, connect existing course materials beneath the NiiL home, and remove the temporary noindex directive. That promotion is intentionally not part of this change.
