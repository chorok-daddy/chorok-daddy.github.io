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

The original Publications page contained only a Google Scholar link; the local publication catalog now replaces that landing panel. Internship submissions remain with the original Notion application form; submitted responses are neither collected nor published here. A typo in the displayed research tag (`Appied Intelligence`) is corrected in rendering while the source data is preserved. Current member status, affiliation and participation history are maintained separately in `content/members.json`; the original Notion member records remain archived in `pages.json`.

## Final review and later promotion

Review the design, member affiliations/statuses, project metadata, course archive wording, recruitment notice, and original application submission flow. Automated link checks validate local targets and anchors only; they do not certify Scholar, KLAS, Notion forms, or other external services.

After explicit final review, choose the new root routing, connect existing course materials beneath the NiiL home, and remove the temporary noindex directive. That promotion is intentionally not part of this change.

## Project-centered revision (2026-10-23)

`/niil/research/` combines Research and Projects. The former `/niil/projects/` and concept-area pages redirect to the catalog. Existing project detail URLs remain stable. Three themes organize **17 project families**; search, theme and status filters can be combined. The `?topic=robotics|vision|human` links select a theme.

- `content/projects.json` owns current project metadata, contract history and result highlights.
- `content/projects/*.md` owns the 17 editable case studies, rendered into semantic HTML. Snapshot-only project bodies are replaced by concise contributions, results and validation context. Original Notion JSON remains the source archive, not the current project editor.
- 79 n-KURIS records were screened. 30 eligible annual/contract records are each represented once, consolidated into 16 families. One documented KARI-linked 2016–2017 legacy project brings the total to 17.
- Include only external research with Ki-Baek Lee as the institutional principal investigator. Exclude non-PI participation, university-sponsored/intramural work, matching funds, manpower-training and administrative programs. A university acting as the performing institution does not count as a university sponsor.
- The 2015 microprocessor-board and 2016 dock-controller contracts form one related family; their different sponsors and contract periods remain visible. Separate contracts are not represented as continuous funding.
- Delivery-robot dates now follow registered contracts (2022–2024). Vehicle-loading history includes the 2025 contract. Physical AI retains its documented 2026–2031 overall plan and shows the registered first-year contract separately. The 2026 picking-vision entry is Ongoing, as confirmed by the project owner. Project status filters use only Ongoing and Completed.
- Outcome summaries use available reports and distinguish internal tests, reported formal tests, simulations, annual progress, project targets and consortium contributions. Unverified targets are not promoted to results. Some older projects currently have scope/design evidence only; those limits are stated on their pages.
- Private source reports, OCR intermediates, administrative IDs and the screening audit remain outside this public repository. No raw Drive proposal, private download link, payroll, bank information or unpublished source code is included.

Review `content/projects/*.md` for editorial approval. The KARI final report confirms PI and dates; it names NRF as the specialized agency, while the source archive identifies the KARI relationship. Figures from reports are not embedded as full-page screenshots.

## Publication catalog (2026-10-23)

`content/publications.json` contains 37 bibliographic records from the public Ki-Baek Lee Google Scholar profile, covering 2006–2026. All 37 detail records were read to recover full author names and venue metadata. The page renders the records statically and filters by title/author/venue text, year and publication type in the browser. JavaScript is optional for reading the full list. There is no runtime Scholar dependency or automatic synchronization; edit the JSON and rebuild to update the catalog.

Titles link to the individual source/publisher destinations recorded by Scholar. External link availability is not certified. The page omits citation metrics and abstracts. Journal/Conference/Book chapter types follow the bibliographic fields (Source entries ACS Nano and Biosensors and Bioelectronics are journals). One malformed source page range, `1921-718`, is omitted and recorded in that entry's note rather than guessed. This is the profile's listed bibliography, not a claim of exhaustive lab output. A source URL is retained per record for maintenance.

## English and Korean editions

English is the default at `/niil/`; Korean pages live under `/niil/ko/`. The persistent header language switch opens the corresponding page and retains search and filters. Explicit URLs select the language. Research summaries, navigation, member histories, contact and application guidance are bilingual. Original publication titles and archived teaching content retain their source language.

- `content/members.json`: current member records, affiliations and dated roles.
- `content/project-locales.json`: localized project titles and summaries.
- `content/projects/en/*.md`: English case studies corresponding to Korean case studies.
- `/niil/join/`: evergreen participation guidance; old recruitment routes redirect here.

Contact links to a bilingual Google Form with four required fields: inquiry type, name, reply email and message. Responses are held in a private Google Sheet. The public repository contains only the responder URL, never the form editor URL, response-sheet ID or response contents. Monitoring is maintained separately on the owner's Mac; it is not a website backend. Direct email remains a fallback.
