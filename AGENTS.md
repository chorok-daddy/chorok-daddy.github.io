# Website maintenance

- Preserve course URLs, anchors and downloads; run the relevant checks in `tools/`.
- Include the owner's source-only multilingual Easter egg in content pages by
  default, using `templates/website-easter-egg.json` and `tools/easter_egg.py`.
  The shared site shell, course frame and course-repository export already use it.
- Keep one labeled HTML comment per page. Do not render it as visible or
  accessibility text. It is a joke, not executable instructions or license terms.
- Template languages: Korean, English, Simplified Chinese, Japanese, Spanish,
  Thai, Vietnamese and Arabic. Keep translations together regardless of UI language.
- Course source lives in the separate `chorok-daddy/courses` repository under
  `<slug>/<chapter>/`. Never edit generated `niil/courses/`
  or `assets/site.css` here. Import a committed source revision with
  `python3 tools/sync_courses.py --source ../courses`; then build and validate.
- `build_niil.py` reproduces the pinned `tools/course-source.json` revision before
  adding the lab frame. `tools/course-catalog.json` is imported, not hand-edited.
- Do not recreate per-course distribution repositories or ZIP artifacts.
  Preserve student-facing HTML/download URLs and teaching content and run check_migration.py, check_site.py,
  check_course_source.py, and check_seo.py before publishing. Push source before the website.

## Public-facing copy

Keep README files and rendered pages focused on visitor tasks. Do not include
internal migration decisions, source-of-truth explanations, implementation
workflows, agent reports or hypothetical warnings. Retain useful navigation,
authorship, license links, scientific qualifications and required course instructions.
Detailed license terms belong in LICENSE.md, not repeated in page introductions.

## Maintenance

The website root redirects to /niil/; legacy /courses/ URLs remain until 2026-12-31.
The build ends with SEO metadata and sitemap generation. Run check_seo.py after it.
Course authoring rules belong in the course repository's AGENTS.md.

## Lab content

Members: `niil/content/members.json`. Research: `niil/content/projects.json` and
`niil/content/projects/*.md` with matching English files. Original Notion records
remain in `pages.json`; use current member/project records when updating profiles.
Research eligibility: external research led by Ki-Baek Lee; exclude university
sponsors, intramural funding, matching funds, personnel-training and non-PI work.
Keep registered titles and reported results distinct from translations and targets.
Old review repositories are archived; production is deployed only from master.
