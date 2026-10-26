# NiiL website

Production home: https://chorok-daddy.github.io/niil/ (Korean). English: `/niil/en/`. Course materials live at `/niil/courses/`. `/` and `/niil/ko/` are compatibility redirects.

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

Preview `/niil/`. Pages work without JavaScript; JavaScript adds project filtering, publication and project search, and a document outline.

## Source and conversion decisions

Source: https://niilab.notion.site/NiiL-1af888a17b308042a68fe1de9ed500ee

Retrieved on 2026-10-23. Public site pages were fetched by URL because the active Notion integration cannot query the niilab workspace directly. Public browser views supplied the member, project, and course-row inventories. Duplicate linked database views were consolidated; empty layout wrapper pages and editor metadata are not visitor content.

All six course inventories were reconciled against the visible counts: Robot Basic Lab 32; Micro-Processor Applications 31; Control System 1 30; Control System 2 30; AI Applications 31; EE Seminar 20. Each inventory row has a local detail page. Course source content is preserved as an archive; the existing current AI Applications and Control 1 materials remain authoritative at `/niil/courses/`.

The original Publications page contained only a Google Scholar link; the local publication catalog now replaces that landing panel. Application guidance is maintained locally in `/niil/contact/#join`; submissions use the private Google Form response workflow. A typo in the displayed research tag (`Appied Intelligence`) is corrected in rendering while the source data is preserved. Current member status, affiliation and participation history are maintained separately in `content/members.json`; the original Notion member records remain archived in `pages.json`.

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

Korean is the default at `/niil/`; English home is `/niil/en/`. Former `/niil/ko/` detail URLs redirect to their Korean counterparts. The language switch is ordered 한국어 / EN. The persistent header language switch opens the corresponding page and retains search and filters. Explicit URLs select the language. Research summaries, navigation, member histories, contact and application guidance are bilingual. Original publication titles and archived teaching content retain their source language.

- `content/members.json`: current member records, affiliations and dated roles.
- `content/project-locales.json`: localized project titles and summaries.
- `content/projects/en/*.md`: English case studies corresponding to Korean case studies.
- `/niil/contact/`: one contact and application destination; participation guidance is the `#join` section.
- `content/join/application-{en,ko}.md`: internal application guidance, rendered in `/niil/contact/#join` and its English counterpart.

Contact provides one shared inquiry entry point linking to a bilingual Google Form with four required fields: inquiry type, name, reply email and message. Responses are held in a private Google Sheet. The public repository contains only the responder URL, never the form editor URL, response-sheet ID or response contents. Monitoring is maintained separately on the owner's Mac; it is not a website backend. Direct email remains a fallback.

Home participation links open the Contact page at `#join`. `/join/`, `/join/apply/` and the old recruitment URL redirect directly there. The clearly named inquiry/application form is directly accessible at the top and after guidance; neither link routes through another choice page. Inquiry categories are selected only in the form. Main navigation has five destinations: Research, Publications, People, Course, Contact. Detail pages return to their owning catalog.

## Production release (2026-10-26)

Owner authorized publication after mobile review. The builder writes the NiiL home under `/niil/` and allows indexing; root remains a routing-only alias. Primary navigation is always visible on mobile, without a menu-opening step. Research opens directly on filters and project results; theme cards remain on Home. Duplicate role labels and fallback email instructions are removed.

Review snapshot hosting remains separate in `chorok-daddy/niil-preview`; snapshot exports must retain noindex/nofollow and rewrite root/asset links for that deployment.

Language default: Korean at `/niil/`, English at `/niil/en/`; switches use 한국어 / EN. Course links directly to `/niil/courses/`; legacy Teaching URLs redirect there. Existing course materials and archived Notion course URLs are preserved.

## Canonical URL layout (2026-10-26)

- `/`: routing-only entry to `/niil/`.
- `/niil/`: Korean lab home and Korean details.
- `/niil/en/`: English home and English details.
- `/niil/courses/`: canonical editable course files. Course navigation uses one 메인 강의페이지 link to this directory.
- `/niil/ko/…`: compatibility redirects to the Korean canonical counterparts.
- `/courses/…`: temporary compatibility through the 2026-2 semester. All 66 HTML pages redirect to exact counterparts preserving queries/fragments. The 29 non-HTML files are byte-identical mirrors, because static Pages cannot issue binary-path redirects. Do not edit these mirrors.

`tools/course-compatibility.json` owns the old course URL inventory and original download hashes. `tools/build_compat_routes.py` regenerates aliases/mirrors from canonical content. `tools/check_migration.py` verifies every legacy URL, preserved anchor, file hash and navigation destination. The owner approved legacy course retirement on 2026-12-31. Remove only the listed legacy paths and course-mirror generation at retirement; preserve `/niil/courses/`. Root and former language aliases are independent of course retirement.

## Registered project titles (2026-10-26)

The catalog and detail headings use full Korean registered titles. Physical AI, adaptive consultation, sign language, swarm search, emotion assessment and sales assistance were matched against NTIS project search records (links in `content/projects.json`). The emotion project's NTIS title uses 디지털콘텐츠 and 상용화; original annual n-KURIS contract strings remain unchanged in history. Four collections retain an editorial grouping label and show their individual contract titles directly in the catalog.

`official_title_en` is populated only when supported by a source title field, now verified against NTIS project detail fields for Physical AI, adaptive consultation, sign language, swarm search and emotion assessment. Other English editions retain the Korean title instead of representing an editorial translation as an official English name. After authenticated NTIS review, five official English titles are confirmed. The sales-assistance NTIS English field is blank (its report also has no English title); other service contracts could not be matched to independent NTIS project records. Parent-project titles are not substituted for contract titles. Private proposal files and Drive IDs remain outside this repository.

## NTIS completion-report review (2026-10-26)

Adaptive consultation and sign-language case studies now use the completion-report results summaries displayed by NTIS (TRKO202200015384, p. 2; TRKO202100001466, p. 2). Consultation metrics are reported test results; sign-language figures are criteria reported as met, not exact final measurements. Full report texts were not inspected in this review. Swarm-search results were cross-checked with the NTIS Korean completion summary (TRKO201800003538, p. 3); its English summary retains earlier scope/target wording. Sales-assistance report metadata is available but its full text is non-public and no results abstract is shown. The 2025 emotion project's outcome list has no report category; existing final-evaluation evidence is retained. The ongoing Physical AI project has no registered outcomes.

Project metadata links are labeled NTIS 링크 / NTIS link and open in a new tab with noopener/noreferrer. Report citations use the same behavior. Both language editions and catalog summaries are maintained together.
